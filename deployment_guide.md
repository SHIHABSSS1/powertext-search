# Deploy PowerText Search Engine on Render

## Prerequisites
1. A GitHub account
2. Your project files in a GitHub repository
3. A Render account (sign up at render.com)

## Step 1: Prepare Your Project

1. Make sure your project has these files:
   - app.py
   - requirements.txt
   - wsgi.py
   - templates/index.html
   - data.xlsx
   - Procfile

2. Create a new file called `wsgi.py` with this content:
   ```python
   from app import app

   if __name__ == "__main__":
       app.run()
   ```

3. Create a `Procfile` with this content:
   ```
   web: gunicorn wsgi:app
   ```

4. Update your `requirements.txt` to include:
   ```
   flask==2.0.1
   pandas==1.3.3
   openpyxl==3.0.9
   gunicorn==20.1.0
   whitenoise==5.3.0
   ```

## Step 2: Deploy on Render

1. Go to render.com and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure your service:
   - Name: powertext-search (or your preferred name)
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Plan: Free

5. Add these environment variables:
   - `SECRET_KEY`: (generate a random string)
   - `DEBUG`: False

6. Click "Create Web Service"

## Step 3: Configure Domain

1. Once deployed, go to your service settings
2. Under "Custom Domains":
   - Add your custom domain if you have one
   - Or use the provided render.com subdomain

## Important Notes

1. **Data Persistence**:
   - The free tier has ephemeral storage
   - Search history will reset when the service restarts
   - Consider using a database for persistent storage

2. **File Storage**:
   - Make sure your data.xlsx file is in the repository
   - Or use a cloud storage service for the Excel file

3. **Performance**:
   - Free tier has limitations on CPU and memory
   - Service may sleep after inactivity
   - First request after sleep may be slow

4. **Security**:
   - Your app will have HTTPS enabled automatically
   - Environment variables are encrypted

## Troubleshooting

1. If deployment fails:
   - Check the build logs
   - Verify all required files are present
   - Ensure requirements.txt is correct

2. If app crashes:
   - Check the logs in Render dashboard
   - Verify environment variables are set
   - Ensure data.xlsx is accessible

3. If search doesn't work:
   - Verify data.xlsx is in the correct location
   - Check file permissions
   - Review error logs

## Maintenance

1. Regular updates:
   - Keep dependencies updated
   - Monitor Render dashboard for issues
   - Check logs periodically

2. Backup:
   - Keep a local copy of your data
   - Export search history regularly if needed 