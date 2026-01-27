# Deploying Body Composition Assessment App to Vercel

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional): Install via npm
   ```bash
   npm install -g vercel
   ```
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)

## Project Structure for Vercel

The app has been configured for Vercel deployment with the following structure:

```
powerfuel_final/
├── api/
│   └── index.py          # Vercel serverless entry point
├── templates/
│   ├── index.html
│   └── dashboard.html
├── static/              # (create if you have CSS/JS files)
├── app.py              # Main Flask application
├── config.py           # Configuration
├── pdf_generator.py    # PDF generation
├── email_service.py    # Email service
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel configuration
├── .env                # Local environment variables (DO NOT COMMIT)
└── .gitignore          # Git ignore file
```

## Step-by-Step Deployment

### 1. Prepare Environment Variables

You need to set up the following environment variables in Vercel:

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon/public key
- `EMAIL_USER` - Gmail address for sending emails
- `EMAIL_PASSWORD` - Gmail app password

### 2. Update .gitignore

Make sure your `.gitignore` includes:

```
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.venv
*.pdf
*.log
.DS_Store
```

### 3. Deploy via Vercel Dashboard (Easiest Method)

#### Step 3.1: Push to Git Repository

```bash
git init
git add .
git commit -m "Initial commit for Vercel deployment"
git remote add origin <your-git-repo-url>
git push -u origin main
```

#### Step 3.2: Import Project to Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your Git repository
4. Vercel will auto-detect it as a Python project

#### Step 3.3: Configure Environment Variables

1. In the project settings, go to **"Environment Variables"**
2. Add each variable:
   - Name: `SUPABASE_URL`, Value: `your-supabase-url`
   - Name: `SUPABASE_KEY`, Value: `your-supabase-key`
   - Name: `EMAIL_USER`, Value: `your-email@gmail.com`
   - Name: `EMAIL_PASSWORD`, Value: `your-app-password`
3. Apply to: **Production, Preview, and Development**

#### Step 3.4: Deploy

1. Click **"Deploy"**
2. Wait for the build to complete (2-3 minutes)
3. Your app will be live at `https://your-project-name.vercel.app`

### 4. Deploy via Vercel CLI (Alternative Method)

```bash
# Login to Vercel
vercel login

# Navigate to your project directory
cd d:\Harun\Projects\powerfuel_final

# Deploy to Vercel
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? powerfuel-app (or your choice)
# - Directory? ./
# - Override settings? No

# Add environment variables
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
vercel env add EMAIL_USER
vercel env add EMAIL_PASSWORD

# Deploy to production
vercel --prod
```

## Configuration Files Explained

### vercel.json

This file configures how Vercel handles your Flask app:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

- **builds**: Specifies the serverless function entry point
- **routes**: Routes all requests to the Flask app

### api/index.py

This is the Vercel serverless entry point that imports your Flask app:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
application = app
```

## Important Notes

### 1. **Serverless Limitations**

- **Execution Time**: Vercel free tier has a 10-second execution limit
- **File System**: `/tmp` is the only writable directory
- **Memory**: Limited to 1024 MB on free tier

### 2. **PDF Generation**

PDFs are generated in-memory and sent directly to the client or email. If you encounter issues:

- PDFs are stored temporarily in `/tmp` on Vercel
- Files in `/tmp` are not persistent across invocations
- Consider using cloud storage (S3, Cloudinary) for large files

### 3. **Static Files**

If you add CSS/JS files, create a `static/` folder:

```
static/
├── css/
│   └── style.css
└── js/
    └── script.js
```

Reference in templates:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

### 4. **Database Connection**

Supabase works perfectly with Vercel serverless functions. Connection pooling is handled automatically by the Supabase client.

## Testing the Deployment

1. **Homepage**: `https://your-app.vercel.app/`
2. **Dashboard**: `https://your-app.vercel.app/dashboard`
3. **API Endpoints**:
   - POST `/api/save-assessment`
   - GET `/api/assessments`
   - GET `/api/generate-pdf/<id>`
   - POST `/api/send-email/<id>`

## Troubleshooting

### Build Fails

**Check logs in Vercel dashboard**:
- Go to Deployments → Select failed deployment → View logs
- Common issues: Missing dependencies, Python version mismatch

**Solution**: Ensure `requirements.txt` is complete

### Module Not Found Errors

**Issue**: `ModuleNotFoundError: No module named 'xyz'`

**Solution**: Add the missing module to `requirements.txt`

### Environment Variable Issues

**Issue**: App can't connect to Supabase or send emails

**Solution**: 
1. Verify environment variables are set in Vercel dashboard
2. Redeploy after adding variables
3. Check variable names match exactly (case-sensitive)

### PDF Generation Fails

**Issue**: PDF generation times out or fails

**Solution**:
1. Optimize PDF generation code
2. Reduce image sizes if any
3. Consider upgrading to Vercel Pro for longer execution time

### Email Sending Fails

**Issue**: Emails not being sent

**Solution**:
1. Verify Gmail app password is correct
2. Check Gmail security settings
3. Ensure "Less secure app access" is enabled OR use App Password
4. Test with a different SMTP provider if needed

## Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain (e.g., `powerfuel.yourdomain.com`)
3. Follow DNS configuration instructions
4. SSL certificate is automatic

## Monitoring & Logs

1. **View Logs**: Vercel Dashboard → Project → Logs
2. **Analytics**: Available in Pro plan
3. **Error Tracking**: Consider integrating Sentry

## Updating the App

```bash
# Make changes to your code
git add .
git commit -m "Update description"
git push origin main

# Vercel automatically redeploys on push
```

Or with CLI:
```bash
vercel --prod
```

## Cost Considerations

**Vercel Free Tier Includes**:
- 100 GB bandwidth per month
- Unlimited projects
- Serverless function executions
- Automatic SSL

**Pro Plan** (if needed):
- $20/month per user
- 1 TB bandwidth
- Longer serverless execution time (60s)
- Advanced analytics

## Security Checklist

- ✅ Environment variables stored securely in Vercel
- ✅ `.env` file in `.gitignore`
- ✅ No hardcoded secrets in code
- ✅ HTTPS enabled by default
- ✅ CORS configured if needed
- ✅ Input validation in place

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)

## Quick Deploy Button (Optional)

Add this to your README.md for one-click deployment:

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/powerfuel-app)
```

---

**Your app is now ready for Vercel deployment! 🚀**

Follow the steps above, and your Body Composition Assessment app will be live on the internet in minutes.
