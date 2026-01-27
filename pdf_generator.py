from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

def generate_body_composition_pdf(assessment):
    """Generate a professional PDF report for body composition assessment"""
    
    # Use /tmp directory for serverless environments (Vercel)
    reports_dir = '/tmp'
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate filename
    filename = f"{reports_dir}/body_assessment_{assessment['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    
    # Title
    title = Paragraph("BODY COMPOSITION ASSESSMENT REPORT", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Date
    date_text = Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", normal_style)
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Personal Information Section
    elements.append(Paragraph("PERSONAL INFORMATION", heading_style))
    
    personal_data = [
        ['Name:', assessment['name']],
        ['Age:', f"{assessment['age']} years"],
        ['Gender:', assessment['gender'].capitalize()],
        ['Height:', f"{assessment['height_cm']} cm"],
        ['Mobile:', assessment['mobile']],
        ['Email:', assessment['email']],
    ]
    
    personal_table = Table(personal_data, colWidths=[2*inch, 4*inch])
    personal_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(personal_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Body Composition Measurements Section
    elements.append(Paragraph("BODY COMPOSITION MEASUREMENTS", heading_style))
    
    measurements_data = [
        ['Measurement', 'Value', 'Unit'],
        ['Weight', f"{assessment['weight_kg']}", 'kg'],
        ['BMI', f"{assessment['bmi']}", 'kg/m²'],
        ['Body Fat', f"{assessment['body_fat_percent']}", '%'],
        ['Visceral Fat', f"{assessment['visceral_fat_percent']}", '%'],
        ['Resting Metabolism', f"{assessment['resting_metabolism']}", 'kcal'],
        ['Metabolic Age', f"{assessment['metabolic_age']}", 'years'],
    ]
    
    measurements_table = Table(measurements_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    measurements_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
    ]))
    elements.append(measurements_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Subcutaneous Fat vs Muscle Mass Section
    elements.append(Paragraph("SUBCUTANEOUS FAT VS MUSCLE MASS DISTRIBUTION", heading_style))
    
    distribution_data = [
        ['Body Part', 'Subcutaneous Fat (%)', 'Muscle Mass (%)'],
        ['Whole Body', f"{assessment['whole_body_subcutaneous']}", f"{assessment['whole_body_muscle']}"],
        ['Trunk', f"{assessment['trunk_subcutaneous']}", f"{assessment['trunk_muscle']}"],
        ['Arms', f"{assessment['arms_subcutaneous']}", f"{assessment['arms_muscle']}"],
        ['Legs', f"{assessment['legs_subcutaneous']}", f"{assessment['legs_muscle']}"],
    ]
    
    distribution_table = Table(distribution_data, colWidths=[2*inch, 2*inch, 2*inch])
    distribution_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
    ]))
    elements.append(distribution_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Additional Calculations and Inferences
    height_m = assessment['height_cm'] / 100
    gender = assessment['gender'].lower()
    age = assessment['age']
    bmi = assessment['bmi']
    body_fat = assessment['body_fat_percent']
    visceral_fat = assessment['visceral_fat_percent']
    metabolic_age = assessment['metabolic_age']
    
    # BMI Category (Asian-Pacific Classification)
    if age >= 18:
        if bmi < 18.5:
            bmi_category = "Underweight"
            bmi_inference = "Below optimal range - may indicate insufficient energy for endurance training"
        elif bmi < 23.0:
            bmi_category = "Normal"
            bmi_inference = "Optimal range for endurance athletes"
        elif bmi < 25.0:
            bmi_category = "Overweight"
            bmi_inference = "Slightly elevated - monitor weight management"
        elif bmi < 30.0:
            bmi_category = "Obese I"
            bmi_inference = "Weight management recommended to improve performance"
        else:
            bmi_category = "Obese II"
            bmi_inference = "Significant weight management needed"
    else:
        bmi_category = "N/A"
        bmi_inference = "BMI classification not applicable for under 18 years"
    
    # Body Fat Status (Lohman 1986 & Nagamine 1972)
    if gender == 'male':
        if body_fat < 10:
            bf_status = "Low - Below normal range (Lohman 1986)"
        elif body_fat <= 20:
            bf_status = "Normal - Healthy range (Lohman 1986)"
        elif body_fat <= 25:
            bf_status = "High - Above normal (Lohman 1986)"
        else:
            bf_status = "Very High - Action needed (Lohman 1986)"
    else:
        if body_fat < 20:
            bf_status = "Low - Below normal range (Lohman 1986)"
        elif body_fat <= 30:
            bf_status = "Normal - Healthy range (Lohman 1986)"
        elif body_fat <= 35:
            bf_status = "High - Above normal (Lohman 1986)"
        else:
            bf_status = "Very High - Action needed (Lohman 1986)"
    
    # Visceral Fat Inference (OMRON Healthcare)
    if visceral_fat <= 9.5:
        vf_status = "Normal - Healthy level (OMRON Healthcare)"
        vf_inference = "Excellent visceral fat level - optimal for cardiovascular endurance"
    elif visceral_fat <= 14.5:
        vf_status = "High - Monitor and take action (OMRON Healthcare)"
        vf_inference = "Elevated visceral fat may impact performance - reduction recommended"
    else:
        vf_status = "Very High - Immediate action required (OMRON Healthcare)"
        vf_inference = "High visceral fat impacts cardiovascular performance - immediate action needed"
    
    elements.append(Paragraph("INFERENCE & ANALYSIS FOR RUNNERS", heading_style))
    
    # BMI Category Section
    inference_data = [
        ['Assessment', 'Result', 'Status/Inference'],
        ['BMI Category\n(Asian-Pacific)', f"{bmi} kg/m\u00b2\n{bmi_category}", bmi_inference],
        ['Body Fat %\n(Lohman 1986)', f"{body_fat}%", bf_status],
        ['Visceral Fat\n(OMRON)', f"{visceral_fat}", f"{vf_status}\n{vf_inference}"],
    ]
    
    inference_table = Table(inference_data, colWidths=[2*inch, 1.8*inch, 2.7*inch])
    inference_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(inference_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Muscle Mass Distribution Analysis
    elements.append(Paragraph("MUSCLE MASS DISTRIBUTION ANALYSIS", heading_style))
    
    def get_ratio_analysis(subcutaneous, muscle):
        if muscle == 0 or subcutaneous == 0:
            return "N/A", "Insufficient data"
        ratio_text = f"1:{muscle/subcutaneous:.1f}"
        ratio = subcutaneous / muscle
        if ratio <= 0.33:
            status = "Excellent (Optimal for athletes)"
        elif ratio <= 0.5:
            status = "Good (Healthy ratio)"
        elif ratio <= 0.7:
            status = "Fair (Room for improvement)"
        elif ratio <= 1.0:
            status = "Average (Consider muscle gain)"
        else:
            status = "Below optimal (Focus needed)"
        return ratio_text, status
    
    wb_ratio, wb_status = get_ratio_analysis(assessment['whole_body_subcutaneous'], assessment['whole_body_muscle'])
    trunk_ratio, trunk_status = get_ratio_analysis(assessment['trunk_subcutaneous'], assessment['trunk_muscle'])
    arms_ratio, arms_status = get_ratio_analysis(assessment['arms_subcutaneous'], assessment['arms_muscle'])
    legs_ratio, legs_status = get_ratio_analysis(assessment['legs_subcutaneous'], assessment['legs_muscle'])
    
    muscle_data = [
        ['Body Part', 'Fat %', 'Muscle %', 'Ratio (Fat:Muscle)'],
        ['Whole Body', f"{assessment['whole_body_subcutaneous']}", f"{assessment['whole_body_muscle']}", wb_ratio],
        ['Trunk', f"{assessment['trunk_subcutaneous']}", f"{assessment['trunk_muscle']}", trunk_ratio],
        ['Arms', f"{assessment['arms_subcutaneous']}", f"{assessment['arms_muscle']}", arms_ratio],
        ['Legs', f"{assessment['legs_subcutaneous']}", f"{assessment['legs_muscle']}", legs_ratio],
    ]
    
    muscle_table = Table(muscle_data, colWidths=[1.8*inch, 1.2*inch, 1.2*inch, 2.3*inch])
    muscle_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(muscle_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Ratio explanation
    ratio_note = Paragraph(
        "<b>Ratio Guide:</b> Optimal ratio for athletes is 1:2 to 1:3 (more muscle than fat). "
        "Example: 1:2.5 means 1 part fat to 2.5 parts muscle.",
        ParagraphStyle('RatioNote', parent=styles['Normal'], fontSize=8, 
                      textColor=colors.HexColor('#7F8C8D'), leftIndent=10)
    )
    elements.append(ratio_note)
    elements.append(Spacer(1, 0.3*inch))
    
    # Performance Notes for Runners
    perf_notes = []
    perf_notes.append("<bullet>\u2022</bullet> BMI Reference (Asian-Pacific): <18.5 Underweight | 18.5-22.9 Normal | 23-24.9 Overweight | 25-29.9 Obese I | \u226530 Obese II")
    perf_notes.append(f"<bullet>\u2022</bullet> Metabolic Age: {metabolic_age} years vs Actual Age: {age} years")
    
    if metabolic_age < age:
        perf_notes.append("<bullet>\u2022</bullet> \u2713 Excellent! Metabolic age is better than chronological age - indicates good fitness level")
    elif metabolic_age > age:
        perf_notes.append("<bullet>\u2022</bullet> \u26a0 Metabolic age is higher - focus on improving metabolic health through training and nutrition")
    
    perf_notes.append("<bullet>\u2022</bullet> Visceral Fat (OMRON Healthcare): 0-9.5 Normal | 10-14.5 High | 15-30 Very High")
    
    if gender == 'male':
        if body_fat <= 13:
            perf_notes.append("<bullet>\u2022</bullet> \u2713 Body composition optimal for competitive marathon running")
        elif body_fat <= 17:
            perf_notes.append("<bullet>\u2022</bullet> Good body composition for recreational running")
        else:
            perf_notes.append("<bullet>\u2022</bullet> \u26a0 Body fat reduction may improve running performance and reduce injury risk")
    else:
        if body_fat <= 20:
            perf_notes.append("<bullet>\u2022</bullet> \u2713 Body composition optimal for competitive marathon running")
        elif body_fat <= 24:
            perf_notes.append("<bullet>\u2022</bullet> Good body composition for recreational running")
        else:
            perf_notes.append("<bullet>\u2022</bullet> \u26a0 Body fat reduction may improve running performance and reduce injury risk")
    
    notes_text = "<br/>".join(perf_notes)
    performance_notes = Paragraph(
        f"<b>\ud83c\udfc3\u200d\u2642\ufe0f Performance Notes for Runners/Marathon Athletes:</b><br/><br/>{notes_text}",
        ParagraphStyle('Performance', parent=styles['Normal'], fontSize=9, 
                      leading=16, leftIndent=10, rightIndent=10, spaceAfter=8)
    )
    elements.append(performance_notes)
    elements.append(Spacer(1, 0.4*inch))
    
    # Footer/Notes
    notes_style = ParagraphStyle(
        'Notes',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7F8C8D'),
        alignment=TA_LEFT
    )
    
    notes = Paragraph(
        "<b>Notes:</b> This body composition assessment provides valuable insights into your current fitness level. "
        "For marathon runners and athletes, maintaining optimal body composition is crucial for performance. "
        "Please consult with a qualified nutritionist or fitness professional for personalized recommendations.",
        notes_style
    )
    elements.append(notes)
    elements.append(Spacer(1, 0.2*inch))
    
    # PowerFuel branding
    branding = Paragraph(
        "<i>Generated by PowerFuel - The Nutrition Hub</i>",
        ParagraphStyle('Branding', parent=styles['Normal'], fontSize=8, 
                      textColor=colors.HexColor('#95A5A6'), alignment=TA_CENTER)
    )
    elements.append(branding)
    
    # Build PDF
    doc.build(elements)
    
    return filename
