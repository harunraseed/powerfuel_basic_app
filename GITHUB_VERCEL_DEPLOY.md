# Deploy to GitHub and Vercel - Step by Step

## Part 1: Upload to GitHub

### Step 1: Initialize Git and Add Files

Open PowerShell in your project folder and run:

```powershell
cd d:\Harun\Projects\powerfuel_final

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Body Composition Assessment App"
```

### Step 2: Connect to Your GitHub Repository

```powershell
# Add your GitHub repo as remote
git remote add origin https://github.com/harunraseed/powerfuel_basic_app.git

# Set branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**If you get an error about existing content:**
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

**If you need to force push (only if repo is empty):**
```powershell
git push -u origin main --force
```

---

## Part 2: Deploy to Vercel

### Method 1: Via Vercel Dashboard (Easiest)

#### Step 1: Go to Vercel
1. Visit: https://vercel.com/login
2. Sign in with GitHub account
3. Authorize Vercel to access your repositories

#### Step 2: Import Project
1. Click **"Add New Project"** or **"Import Project"**
2. Find and select: `harunraseed/powerfuel_basic_app`
3. Click **"Import"**

#### Step 3: Configure Project
- **Framework Preset**: Select "Other"
- **Root Directory**: `./` (leave as is)
- **Build Command**: Leave empty
- **Output Directory**: Leave empty
- **Install Command**: Leave default

#### Step 4: Add Environment Variables

Click **"Environment Variables"** and add these 4 variables:

| Name | Value |
|------|-------|
| `SUPABASE_URL` | Your Supabase URL from .env file |
| `SUPABASE_KEY` | Your Supabase anon key from .env file |
| `EMAIL_USER` | `powerfuel.thenutritionhub@gmail.com` |
| `EMAIL_PASSWORD` | Your Gmail app password from .env file |

**Important**: Copy values from your `.env` file!

#### Step 5: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for build to complete
3. Your app will be live at: `https://your-project-name.vercel.app`

---

### Method 2: Via Vercel CLI

#### Install Vercel CLI:
```powershell
npm install -g vercel
```

#### Login and Deploy:
```powershell
cd d:\Harun\Projects\powerfuel_final

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Link to existing project? No
# - Project name: powerfuel-app (or your choice)
# - Directory: ./ (press Enter)

# Add environment variables
vercel env add SUPABASE_URL production
vercel env add SUPABASE_KEY production
vercel env add EMAIL_USER production
vercel env add EMAIL_PASSWORD production

# Deploy to production
vercel --prod
```

---

## Part 3: Update Database (Important!)

Before testing, run this SQL in Supabase:

```sql
-- Add email tracking columns
ALTER TABLE body_assessments 
ADD COLUMN IF NOT EXISTS email_sent BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS email_sent_at TIMESTAMP WITH TIME ZONE;
```

1. Go to Supabase Dashboard
2. Click **SQL Editor**
3. Paste the SQL above
4. Click **Run**

---

## Part 4: Test Your Deployment

### Test Homepage (Dashboard)
Visit: `https://your-project.vercel.app/`
- Should show dashboard

### Test New Assessment Form
Visit: `https://your-project.vercel.app/form`
- Fill out form and save
- Should see "Assessment Saved Successfully!" popup

### Test PDF Generation
- Click "📄 PDF" button
- Should download PDF with inference and muscle distribution

### Test Email
- Click "📧 Email" button
- Should see "Email Sent Successfully!" popup
- Check email inbox

### Test Delete
- Click "🗑️ Delete" button
- Confirm deletion
- Should see "Assessment Deleted Successfully!" popup

---

## Troubleshooting

### Build Fails on Vercel

**Check logs**: Go to Vercel Dashboard → Deployments → Click failed deployment → View logs

**Common fixes**:
1. Ensure `vercel.json` exists in root
2. Ensure `api/index.py` exists
3. Ensure `runtime.txt` exists
4. Check `requirements.txt` has all dependencies

### Database Connection Error

1. Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
2. Check there are no extra spaces in environment variables
3. Ensure table `body_assessments` exists
4. Run the database migration SQL above

### Email Not Sending

1. Verify `EMAIL_PASSWORD` is the **App Password** (not regular Gmail password)
2. Ensure Gmail has 2-Step Verification enabled
3. Generate new App Password if needed:
   - Gmail → Settings → Security → 2-Step Verification → App Passwords

### 404 Not Found

- Vercel may take 1-2 minutes to fully deploy
- Try hard refresh: `Ctrl + Shift + R`
- Check deployment status in Vercel dashboard

---

## Update Your App Later

Whenever you make changes:

```powershell
cd d:\Harun\Projects\powerfuel_final

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push

# Vercel automatically redeploys!
```

---

## Your Live URLs

After deployment:

- **Dashboard**: `https://your-project.vercel.app/`
- **New Assessment**: `https://your-project.vercel.app/form`
- **GitHub Repo**: https://github.com/harunraseed/powerfuel_basic_app

---

## Quick Reference Commands

```powershell
# Initialize and push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/harunraseed/powerfuel_basic_app.git
git branch -M main
git push -u origin main

# Later updates
git add .
git commit -m "Your changes"
git push
```

---

## Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **GitHub Docs**: https://docs.github.com
- **Check Vercel Logs**: Dashboard → Deployments → View Function Logs

---

**You're ready to deploy! Start with Part 1 above.** 🚀
