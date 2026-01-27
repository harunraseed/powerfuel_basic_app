# Quick Start Guide - Vercel Deployment

## ⚡ 5-Minute Deployment

### Step 1: Push to GitHub (2 minutes)

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Vercel deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/yourusername/powerfuel-app.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Vercel (3 minutes)

1. **Go to Vercel**: https://vercel.com/dashboard
2. **Click**: "Add New Project"
3. **Import**: Your GitHub repository
4. **Configure**: 
   - Framework Preset: Other
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

5. **Add Environment Variables**:
   ```
   SUPABASE_URL = https://pomdphnkookwogmiwvvu.supabase.co
   SUPABASE_KEY = your-anon-key
   EMAIL_USER = powerfuel.thenutritionhub@gmail.com
   EMAIL_PASSWORD = your-app-password
   ```

6. **Click**: "Deploy"

7. **Done!** Your app is live at: `https://your-project.vercel.app`

## 🔗 Access Your App

- **Homepage**: `https://your-project.vercel.app/`
- **Dashboard**: `https://your-project.vercel.app/dashboard`

## 🔄 Update Deployment

Every time you push to GitHub, Vercel automatically redeploys:

```bash
git add .
git commit -m "Your changes"
git push
```

## ⚙️ Environment Variables You Need

| Variable | Where to Get It |
|----------|----------------|
| `SUPABASE_URL` | Supabase Dashboard → Settings → API → Project URL |
| `SUPABASE_KEY` | Supabase Dashboard → Settings → API → anon/public key |
| `EMAIL_USER` | Your Gmail address |
| `EMAIL_PASSWORD` | Gmail → Security → 2-Step Verification → App Passwords |

## 🐛 Troubleshooting

**Build fails?**
- Check Vercel deployment logs
- Ensure all dependencies are in `requirements.txt`

**Can't send emails?**
- Verify Gmail App Password is correct
- Check environment variables are set

**Database errors?**
- Verify Supabase credentials
- Check table permissions (see database_schema.sql)

## 📚 Full Documentation

See **[VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)** for complete instructions.
