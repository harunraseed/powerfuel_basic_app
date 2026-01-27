# Vercel Deployment Checklist

Before deploying to Vercel, ensure you've completed all steps:

## ✅ Pre-Deployment Checklist

### 1. Code Preparation
- [ ] All code is committed to Git
- [ ] `.env` file is in `.gitignore` (already done ✓)
- [ ] No hardcoded credentials in code
- [ ] All dependencies are in `requirements.txt`

### 2. Vercel Configuration Files
- [ ] `vercel.json` exists (already created ✓)
- [ ] `api/index.py` exists (already created ✓)
- [ ] `runtime.txt` exists (already created ✓)

### 3. Environment Variables Ready
Have these values ready to paste into Vercel:

| Variable | Value | Where to Find |
|----------|-------|---------------|
| `SUPABASE_URL` | `https://pomdphnkookwogmiwvvu.supabase.co` | Already have ✓ |
| `SUPABASE_KEY` | Your anon key | Check your .env file |
| `EMAIL_USER` | `powerfuel.thenutritionhub@gmail.com` | Already have ✓ |
| `EMAIL_PASSWORD` | Your Gmail app password | Check your .env file |

### 4. Database Setup
- [ ] Supabase table `body_assessments` exists
- [ ] Table permissions are granted (run SQL from `database_schema.sql`)
- [ ] Test connection works locally

### 5. Email Setup
- [ ] Gmail account has 2-Step Verification enabled
- [ ] App Password generated (not regular password)
- [ ] Test email sending works locally

## 🚀 Deployment Steps

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to: https://vercel.com/dashboard
   - Click: "Add New Project"
   - Select: Your GitHub repository
   - Framework: Other
   - Click: "Deploy"

3. **Add Environment Variables**
   - Go to: Project Settings → Environment Variables
   - Add all 4 variables listed above
   - Apply to: Production, Preview, Development

4. **Redeploy**
   - Go to: Deployments
   - Click: "Redeploy"

### Option B: Deploy via CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd d:\Harun\Projects\powerfuel_final
vercel

# Add environment variables
vercel env add SUPABASE_URL production
vercel env add SUPABASE_KEY production
vercel env add EMAIL_USER production
vercel env add EMAIL_PASSWORD production

# Deploy to production
vercel --prod
```

## ✅ Post-Deployment Checklist

### Test Your Deployment

1. **Homepage Test**
   - [ ] Visit `https://your-project.vercel.app/`
   - [ ] Form loads correctly
   - [ ] All fields are visible

2. **Save Assessment Test**
   - [ ] Fill out form
   - [ ] Click "Save Assessment"
   - [ ] Check success message
   - [ ] Verify data saved in Supabase

3. **PDF Generation Test**
   - [ ] Click "Generate PDF"
   - [ ] PDF downloads successfully
   - [ ] Check inference section is present
   - [ ] Check muscle distribution table is present

4. **Email Test**
   - [ ] Click "Send Email"
   - [ ] Check email arrives
   - [ ] PDF is attached
   - [ ] Formatting looks good

5. **Dashboard Test**
   - [ ] Visit `https://your-project.vercel.app/dashboard`
   - [ ] All assessments load
   - [ ] Search functionality works
   - [ ] View inference modal opens
   - [ ] Muscle distribution table shows

## 🐛 Troubleshooting

### Build Fails
**Check**: Vercel deployment logs
**Common Fix**: 
- Verify `requirements.txt` has all dependencies
- Check Python version in `runtime.txt`

### 500 Internal Server Error
**Check**: Vercel function logs
**Common Fix**:
- Environment variables not set
- Check variable names match exactly (case-sensitive)

### Database Connection Error
**Check**: Supabase credentials
**Common Fix**:
- Copy exact values from Supabase dashboard
- Ensure no extra spaces in environment variables

### Email Not Sending
**Check**: Gmail app password
**Common Fix**:
- Use App Password, not regular password
- Enable 2-Step Verification first
- Generate new App Password

### PDF Generation Timeout
**Check**: Vercel function execution time
**Note**: Free tier has 10-second limit
**Solution**: Optimize PDF generation or upgrade to Pro

## 📊 Monitoring

### View Logs
```bash
vercel logs <your-project-url>
```

Or in Vercel Dashboard:
- Go to: Project → Logs
- Filter by: Function, Time, Status

### Check Function Stats
- Go to: Project → Analytics (Pro plan)
- View: Execution time, Memory usage, Invocations

## 🔄 Update Process

```bash
# Make changes
git add .
git commit -m "Description of changes"
git push

# Vercel auto-deploys on push to main branch
```

## 🌐 Custom Domain (Optional)

1. Go to: Project Settings → Domains
2. Add domain: `your-domain.com`
3. Follow DNS instructions
4. SSL: Automatic

## 💡 Tips

- **Always test locally first**: `python app.py`
- **Check logs frequently**: Especially after first deployment
- **Use Preview Deployments**: Push to a branch to test before production
- **Monitor Usage**: Check Vercel dashboard for bandwidth and function usage

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Vercel Support**: support@vercel.com
- **Project Support**: powerfuel.thenutritionhub@gmail.com

---

## ✅ Final Check

Before marking deployment complete:

- [ ] App is live and accessible
- [ ] All features work (form, save, PDF, email, dashboard)
- [ ] No errors in Vercel logs
- [ ] Email notifications work
- [ ] PDFs generate correctly
- [ ] Dashboard loads and displays data
- [ ] Search functionality works
- [ ] Inference modal shows correct data

**Status**: 🟢 Ready for Production | 🟡 Needs Testing | 🔴 Issues Found

---

**Congratulations! Your app is deployed! 🎉**
