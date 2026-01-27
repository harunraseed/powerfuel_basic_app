# PowerFuel Body Composition Assessment

A Python Flask web application for body composition assessment designed for marathon runners and athletes. This application captures detailed body measurements, saves them to Supabase, generates professional PDF reports with inference analysis, and emails them to clients.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/powerfuel-app)

> **🚀 Ready to Deploy?** See [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) for a quick overview, or jump to [QUICKSTART_VERCEL.md](QUICKSTART_VERCEL.md) for 5-minute deployment!

## 🏃‍♂️ Features

- **Comprehensive Assessment Form**: Capture personal details and body composition measurements
- **Automatic Calculations**: BMI auto-calculation and muscle-to-fat ratio analysis
- **Database Storage**: Save assessments to Supabase PostgreSQL database
- **PDF Generation**: Professional PDF reports with inference section and muscle distribution analysis
- **Dashboard**: View all assessments with search functionality and detailed inference modal
- **Email Integration**: Send assessment reports directly to clients via Gmail
- **Athlete-Focused**: Designed specifically for marathon runners with performance insights
- **Standards-Based**: Uses Asian-Pacific BMI classification and Indian body fat standards

## 📋 Measurements Captured

### Personal Information
- Name, Age, Height, Gender
- Mobile, Email

### Body Composition Measurements
- Height (cm), Weight (kg)
- BMI (kg/m²)
- Body Fat (%)
- Visceral Fat (%)
- Resting Metabolism (kcal)
- Body Metabolic Age (years)

### Subcutaneous Fat vs Muscle Mass
- Whole Body, Trunk, Arms, Legs
- Subcutaneous fat percentage
- Muscle mass percentage

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
cd d:\Harun\Projects\powerfuel_final
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Your `.env` file is already set up with Supabase and email credentials.

### 4. Set Up Supabase Database

1. Go to your Supabase project: https://pomdphnkookwogmiwvvu.supabase.co
2. Navigate to **SQL Editor**
3. Copy and paste the contents of `database_schema.sql`
4. Run the SQL script to create the `body_assessments` table

### 5. Run the Application

```bash
python app.py
```

The application will be available at: http://localhost:5000

## 📁 Project Structure

```
powerfuel_final/
├── app.py                  # Main Flask application
├── config.py              # Configuration management
├── pdf_generator.py       # PDF generation logic
├── email_service.py       # Email sending functionality
├── database_schema.sql    # Supabase database schema
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (configured)
├── templates/
│   └── index.html        # Main web interface
└── reports/              # Generated PDF reports (auto-created)
```

## 🎯 Usage

1. **Fill in Client Details**: Enter personal information and body measurements
2. **Save Assessment**: Click "Save Assessment" to store data in Supabase
3. **Generate PDF**: Download a professional PDF report
4. **Send to Client**: Email the report directly to the client

## 📊 Additional Calculations

The application automatically calculates:
- BMI (Body Mass Index)
- Lean Body Mass
- Fat Mass
- Body Fat Category (Athletes, Fitness, Average, etc.)

## 🔐 Security

- Environment variables for sensitive data
- Supabase Row Level Security enabled
- Email credentials securely stored

## 📧 Email Configuration

The application is configured to send emails using:
- Gmail SMTP
- Sender: powerfuel.thenutritionhub@gmail.com
- Professional HTML email templates with attached PDF reports

## 🛠️ Technologies Used

- **Backend**: Python 3.x, Flask
- **Database**: Supabase (PostgreSQL)
- **PDF Generation**: ReportLab
- **Email**: SMTP (Gmail)
- **Frontend**: HTML5, CSS3, JavaScript

## 📝 Notes for Event Use

- Perfect for marathon and athletic events
- Quick data entry and report generation
- Professional reports for athletes
- Email delivery for easy distribution

## 🐛 Troubleshooting

### Database Connection Issues
- Verify Supabase credentials in `.env`
- Ensure database schema is created
- Check internet connection

### Email Sending Issues
- Verify Gmail app password is correct
- Check SMTP settings
- Ensure "Less secure app access" is enabled (if needed)

### PDF Generation Issues
- Ensure `reports/` directory exists (auto-created)
- Check file permissions

## 🚀 Deployment

### Deploy to Vercel

This app is configured for deployment on Vercel. See **[VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)** for detailed deployment instructions.

**Quick Deploy**:
1. Push code to GitHub
2. Import project to Vercel
3. Add environment variables
4. Deploy!

Your app will be live at `https://your-project.vercel.app`

### Environment Variables for Production

Set these in Vercel dashboard:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `EMAIL_USER`
- `EMAIL_PASSWORD`

## 📞 Support

For issues or questions:
- Email: powerfuel.thenutritionhub@gmail.com

## 📄 License

This project is proprietary to PowerFuel - The Nutrition Hub.

---

**PowerFuel - The Nutrition Hub** | Optimizing Performance Through Nutrition
