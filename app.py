from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import os
import re
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "data_search_secret_key"  # Required for session

# File to store search history
HISTORY_FILE = "search_history.json"

# Load the Excel file
def load_data():
    try:
        df = pd.read_excel('data.xlsx')
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

# Load search history
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
    return {"searches": []}

# Save search history
def save_history(history):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)
    except Exception as e:
        print(f"Error saving history: {e}")

# Initialize data
data_df = load_data()

@app.route('/')
def home():
    # Initialize session history if not present
    if 'search_history' not in session:
        session['search_history'] = []
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    
    if query:
        # Find rows that match the query
        mask = data_df.apply(lambda x: x.astype(str).str.lower().str.contains(query, na=False)).any(axis=1)
        results = data_df[mask].copy()
        
        # Convert results to list of dictionaries
        search_results = []
        for _, row in results.iterrows():
            # Find which columns contain the keyword
            keyword_columns = []
            for col_name, value in row.items():
                if pd.notna(value) and query in str(value).lower():
                    keyword_columns.append(col_name)
            
            # Create a filtered row by excluding columns with the keyword
            filtered_row = row.drop(keyword_columns)
            
            # Combine only the columns that don't contain the keyword
            filtered_data = ' '.join(str(val) for val in filtered_row if pd.notna(val))
            
            # Clean up any extra spaces
            filtered_data = re.sub(r'\s+', ' ', filtered_data).strip()
            
            # Only add non-empty results
            if filtered_data:
                search_results.append({'data': filtered_data})
        
        # Save to session history
        if 'search_history' not in session:
            session['search_history'] = []
        
        # Add to session history (limit to 10 recent searches)
        search_entry = {
            'query': query,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'results_count': len(search_results)
        }
        session['search_history'] = [search_entry] + session['search_history'][:9]
        session.modified = True
        
        # Save to persistent storage
        history = load_history()
        history["searches"].insert(0, search_entry)
        history["searches"] = history["searches"][:50]  # Limit to 50 searches
        save_history(history)
        
        return jsonify(search_results)
    return jsonify([])

@app.route('/history')
def history():
    # Get history from session or load from file
    session_history = session.get('search_history', [])
    file_history = load_history()
    
    # Combine histories (prioritize session history)
    combined_history = session_history
    
    # Add file history items not in session
    for item in file_history["searches"]:
        if item not in combined_history:
            combined_history.append(item)
    
    # Return top 50 history items
    return jsonify(combined_history[:50])

@app.route('/minute-calculator')
def minute_calculator():
    return render_template('minute_calculator.html')

if __name__ == '__main__':
    app.run(debug=True) 