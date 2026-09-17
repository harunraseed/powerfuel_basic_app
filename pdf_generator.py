from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, PageTemplate, Frame
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os
import shutil

# Get the absolute path to the logo file
# This works both locally and on Vercel
def get_logo_path():
    """Get the logo file path, works in both local and Vercel environments"""
    logo_filename = 'logo_transparent.png'
    
    # Try multiple possible locations with detailed logging
    possible_paths = [
        # Local development
        os.path.join(os.path.dirname(__file__), 'static', 'images', logo_filename),
        os.path.join(os.getcwd(), 'static', 'images', logo_filename),
        
        # Vercel serverless - various possible locations
        os.path.join('/var/task', 'static', 'images', logo_filename),
        os.path.join('/var/task/api', '..', 'static', 'images', logo_filename),
        
        # Relative to this file's parent directory
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', logo_filename),
    ]
    
    print(f"\n🔍 Searching for logo: {logo_filename}")
    print(f"📂 Current working directory: {os.getcwd()}")
    print(f"📄 This file location: {__file__}")
    
    for i, path in enumerate(possible_paths, 1):
        abs_path = os.path.abspath(path)
        exists = os.path.exists(abs_path)
        print(f"  [{i}] {'✓' if exists else '✗'} {abs_path}")
        if exists:
            print(f"\n✅ Logo found at: {abs_path}\n")
            return abs_path
    
    # Debug: List actual directory contents
    print("\n⚠️ Logo not found. Checking directory contents:")
    check_dirs = ['/var/task', os.getcwd(), os.path.dirname(__file__)]
    for check_dir in check_dirs:
        if os.path.exists(check_dir):
            print(f"\n📁 Contents of {check_dir}:")
            try:
                for item in os.listdir(check_dir)[:10]:  # First 10 items
                    item_path = os.path.join(check_dir, item)
                    print(f"  - {item} {'[DIR]' if os.path.isdir(item_path) else ''}")
            except Exception as e:
                print(f"  Error listing: {e}")
    
    print(f"\n❌ Logo not found in any location\n")
    return None

class WatermarkCanvas(canvas.Canvas):
    """Custom canvas class to add watermark and logo on every page"""
    
    def __init__(self, *args, **kwargs):
        self.logo_path = kwargs.pop('logo_path', None)
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
    
    def showPage(self):
        self.draw_watermark()
        self.draw_header_logo()
        canvas.Canvas.showPage(self)
    
    def draw_watermark(self):
        """Draw watermark logo in the center background of every page"""
        if self.logo_path:
            try:
                # Save the current state
                self.saveState()
                
                # Get page dimensions
                page_width, page_height = A4
                
                # Draw watermark in center with transparency
                watermark_size = 4 * inch  # Larger watermark
                x = (page_width - watermark_size) / 2
                y = (page_height - watermark_size) / 2
                
                # Set transparency (0.08 = 8% opacity)
                self.setFillAlpha(0.08)
                
                # Draw the watermark image (logo_path is temp file path)
                self.drawImage(self.logo_path, x, y, 
                              width=watermark_size, height=watermark_size,
                              mask='auto', preserveAspectRatio=True)
                
                # Restore the state
                self.restoreState()
            except Exception as e:
                print(f"Watermark error: {e}")
                import traceback
                traceback.print_exc()
                self.restoreState()
    
    def draw_header_logo(self):
        """Draw small logo in top right corner of every page"""
        if self.logo_path:
            try:
                # Save the current state
                self.saveState()
                
                # Get page dimensions
                page_width, page_height = A4
                
                # Small logo in top right corner
                logo_size = 0.8 * inch
                x = page_width - logo_size - 0.5 * inch  # 0.5 inch from right edge
                y = page_height - logo_size - 0.5 * inch  # 0.5 inch from top edge
                
                # Draw the logo (fully opaque) - logo_path is temp file path
                self.setFillAlpha(1.0)
                self.drawImage(self.logo_path, x, y, 
                              width=logo_size, height=logo_size,
                              mask='auto', preserveAspectRatio=True)
                
                # Restore the state
                self.restoreState()
            except Exception as e:
                print(f"Header logo error: {e}")
                import traceback
                traceback.print_exc()
                self.restoreState()

def generate_body_composition_pdf(assessment):
    """Generate a professional PDF report for body composition analysis"""
    
    # Use /tmp directory for serverless environments (Vercel)
    reports_dir = '/tmp'
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate filename
    filename = f"{reports_dir}/body_assessment_{assessment['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Get logo path directly from static folder
    logo_image = get_logo_path()
    if logo_image:
        print(f"✓ Using logo from: {logo_image}")
    else:
        print(f"✗ Logo not found - PDF will be generated without logo")
    
    # Create PDF document with custom canvas
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Set custom canvas with watermark
    doc.canvasmaker = lambda *args, **kwargs: WatermarkCanvas(*args, logo_path=logo_image, **kwargs)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=15,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    
    # Title (logo is now in header, not in content flow)
    title = Paragraph("BODY COMPOSITION ANALYSIS REPORT", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.1*inch))
    
    # Date
    date_text = Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", normal_style)
    elements.append(date_text)
    elements.append(Spacer(1, 0.15*inch))
    
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
    elements.append(Spacer(1, 0.15*inch))
    
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
    elements.append(Spacer(1, 0.15*inch))
    
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
    elements.append(Spacer(1, 0.15*inch))
    
    # Add page break before inference section
    elements.append(PageBreak())
    
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
    
    # Body Fat Status
    if gender == 'male':
        if body_fat < 10:
            bf_status = "Low - Below normal range"
        elif body_fat <= 20:
            bf_status = "Normal - Healthy range"
        elif body_fat <= 25:
            bf_status = "High - Above normal"
        else:
            bf_status = "Very High - Action needed"
    else:
        if body_fat < 20:
            bf_status = "Low - Below normal range"
        elif body_fat <= 30:
            bf_status = "Normal - Healthy range"
        elif body_fat <= 35:
            bf_status = "High - Above normal"
        else:
            bf_status = "Very High - Action needed"
    
    # Visceral Fat Inference
    if visceral_fat <= 9.5:
        vf_status = "Normal - Healthy level"
        vf_inference = "Excellent visceral fat level - optimal for cardiovascular endurance"
    elif visceral_fat <= 14.5:
        vf_status = "High - Monitor and take action"
        vf_inference = "Elevated visceral fat may impact performance - reduction recommended"
    else:
        vf_status = "Very High - Immediate action required"
        vf_inference = "High visceral fat impacts cardiovascular performance - immediate action needed"
    
    elements.append(Paragraph("INFERENCE & ANALYSIS FOR RUNNERS", heading_style))
    
    # BMI Category Section
    inference_data = [
        ['Assessment', 'Result', 'Status/Inference'],
        ['BMI Category\n(Asian-Pacific)', f"{bmi} kg/m\u00b2\n{bmi_category}", bmi_inference],
        ['Body Fat %', f"{body_fat}%", bf_status],
        ['Visceral Fat', f"{visceral_fat}", f"{vf_status}\n{vf_inference}"],
    ]
    
    # Use Paragraph for text wrapping in the last column
    wrapped_inference_data = [inference_data[0]]  # Keep header as is
    cell_style = ParagraphStyle('CellStyle', parent=styles['Normal'], fontSize=8, leading=10)
    
    for row in inference_data[1:]:
        wrapped_row = [
            row[0],
            row[1],
            Paragraph(row[2], cell_style) if isinstance(row[2], str) else row[2]
        ]
        wrapped_inference_data.append(wrapped_row)
    
    inference_table = Table(wrapped_inference_data, colWidths=[1.5*inch, 1.3*inch, 3.7*inch])
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
        ['Body Part', 'Fat %', 'Muscle %', 'Ratio', 'Suggestions'],
        ['Whole Body', f"{assessment['whole_body_subcutaneous']}", f"{assessment['whole_body_muscle']}", wb_ratio, wb_status],
        ['Trunk', f"{assessment['trunk_subcutaneous']}", f"{assessment['trunk_muscle']}", trunk_ratio, trunk_status],
        ['Arms', f"{assessment['arms_subcutaneous']}", f"{assessment['arms_muscle']}", arms_ratio, arms_status],
        ['Legs', f"{assessment['legs_subcutaneous']}", f"{assessment['legs_muscle']}", legs_ratio, legs_status],
    ]
    
    muscle_table = Table(muscle_data, colWidths=[1.2*inch, 0.8*inch, 0.9*inch, 1*inch, 2.6*inch])
    muscle_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (3, -1), 'CENTER'),
        ('ALIGN', (4, 1), (4, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
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
    perf_notes.append("\u2022 BMI Reference (Asian-Pacific): <18.5 Underweight | 18.5-22.9 Normal | 23-24.9 Overweight | 25-29.9 Obese I | \u226530 Obese II")
    perf_notes.append(f"\u2022 Metabolic Age: {metabolic_age} years vs Actual Age: {age} years")
    
    if metabolic_age < age:
        perf_notes.append("\u2022 \u2713 Excellent! Metabolic age is better than chronological age - indicates good fitness level")
    elif metabolic_age > age:
        perf_notes.append("\u2022 \u26a0 Metabolic age is higher - focus on improving metabolic health through training and nutrition")
    
    perf_notes.append("\u2022 Visceral Fat (OMRON Healthcare): 0-9.5 Normal | 10-14.5 High | 15-30 Very High")
    
    if gender == 'male':
        if body_fat <= 13:
            perf_notes.append("\u2022 \u2713 Body composition optimal for competitive marathon running")
        elif body_fat <= 17:
            perf_notes.append("\u2022 Good body composition for recreational running")
        else:
            perf_notes.append("\u2022 \u26a0 Body fat reduction may improve running performance and reduce injury risk")
    else:
        if body_fat <= 20:
            perf_notes.append("\u2022 \u2713 Body composition optimal for competitive marathon running")
        elif body_fat <= 24:
            perf_notes.append("\u2022 Good body composition for recreational running")
        else:
            perf_notes.append("\u2022 \u26a0 Body fat reduction may improve running performance and reduce injury risk")
    
    notes_text = "<br/>".join(perf_notes)
    
    # Create vibrant performance notes section
    perf_heading_style = ParagraphStyle(
        'PerfHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#E74C3C'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    perf_heading = Paragraph("🏃‍♂️ 💪 Performance Notes for Runners/Marathon Athletes:", perf_heading_style)
    elements.append(perf_heading)
    
    performance_notes = Paragraph(
        notes_text,
        ParagraphStyle('Performance', parent=styles['Normal'], fontSize=9, 
                      leading=16, leftIndent=15, rightIndent=10, spaceAfter=8,
                      textColor=colors.HexColor('#2C3E50'))
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
        "Book a consultation with us by call or message at +91-7397442544 to improve your performance and achieve your goals through a scientific, evidence-based approach.",
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


def generate_general_consultation_pdf(assessment):
    """Generate a simple, easy-to-understand PDF report for the general basic consultation.
    Written for a general audience - no athlete/marathon-specific language."""

    reports_dir = '/tmp'
    os.makedirs(reports_dir, exist_ok=True)

    filename = f"{reports_dir}/general_consultation_{assessment['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    logo_image = get_logo_path()

    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    doc.canvasmaker = lambda *args, **kwargs: WatermarkCanvas(*args, logo_path=logo_image, **kwargs)

    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'GeneralTitle', parent=styles['Heading1'], fontSize=22,
        textColor=colors.HexColor('#2C3E50'), spaceAfter=15,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    heading_style = ParagraphStyle(
        'GeneralHeading', parent=styles['Heading2'], fontSize=14,
        textColor=colors.HexColor('#34495E'), spaceAfter=8, spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    normal_style = styles['Normal']

    elements.append(Paragraph("GENERAL HEALTH & WELLNESS REPORT", title_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", normal_style))
    elements.append(Spacer(1, 0.15*inch))

    # Personal Information
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
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(personal_table)
    elements.append(Spacer(1, 0.15*inch))

    # Key Health Numbers (simple, everyday language)
    elements.append(Paragraph("YOUR KEY HEALTH NUMBERS", heading_style))
    measurements_data = [
        ['Measurement', 'Your Value', 'Unit'],
        ['Weight', f"{assessment['weight_kg']}", 'kg'],
        ['BMI (Body Mass Index)', f"{assessment['bmi']}", 'kg/m²'],
        ['Body Fat', f"{assessment['body_fat_percent']}", '%'],
        ['Visceral Fat', f"{assessment['visceral_fat_percent']}", '%'],
        ['Calories Burnt at Rest', f"{assessment['resting_metabolism']}", 'kcal/day'],
        ['Body\'s Metabolic Age', f"{assessment['metabolic_age']}", 'years'],
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
    elements.append(Spacer(1, 0.15*inch))

    # Body Fat & Muscle spread across the body, plain language
    elements.append(Paragraph("HOW FAT & MUSCLE ARE SPREAD ACROSS YOUR BODY", heading_style))
    distribution_data = [
        ['Body Area', 'Subcutaneous Fat (%)', 'Muscle Mass (%)'],
        ['Whole Body', f"{assessment['whole_body_subcutaneous']}", f"{assessment['whole_body_muscle']}"],
        ['Trunk (Core)', f"{assessment['trunk_subcutaneous']}", f"{assessment['trunk_muscle']}"],
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
    elements.append(Spacer(1, 0.15*inch))

    elements.append(PageBreak())

    gender = assessment['gender'].lower()
    age = assessment['age']
    bmi = assessment['bmi']
    body_fat = assessment['body_fat_percent']
    visceral_fat = assessment['visceral_fat_percent']
    metabolic_age = assessment['metabolic_age']

    if age >= 18:
        if bmi < 18.5:
            bmi_category = "Underweight"
            bmi_inference = "A little below the healthy range - a nutrient-rich diet can help you reach a healthier weight."
        elif bmi < 23.0:
            bmi_category = "Normal"
            bmi_inference = "Great news - your weight is in a healthy range for your height."
        elif bmi < 25.0:
            bmi_category = "Overweight"
            bmi_inference = "Slightly above the healthy range - small daily changes can help bring this down."
        elif bmi < 30.0:
            bmi_category = "Obese I"
            bmi_inference = "Higher than the healthy range - a structured plan for diet and activity is recommended."
        else:
            bmi_category = "Obese II"
            bmi_inference = "Well above the healthy range - please consider professional guidance for weight management."
    else:
        bmi_category = "N/A"
        bmi_inference = "BMI categories shown here apply to adults (18 years and above)."

    if gender == 'male':
        if body_fat < 10:
            bf_status = "Low - below the typical healthy range"
        elif body_fat <= 20:
            bf_status = "Healthy range"
        elif body_fat <= 25:
            bf_status = "Above healthy range"
        else:
            bf_status = "High - lifestyle changes recommended"
    else:
        if body_fat < 20:
            bf_status = "Low - below the typical healthy range"
        elif body_fat <= 30:
            bf_status = "Healthy range"
        elif body_fat <= 35:
            bf_status = "Above healthy range"
        else:
            bf_status = "High - lifestyle changes recommended"

    if visceral_fat <= 9.5:
        vf_status = "Healthy level"
        vf_inference = "Your belly fat level is healthy - good for long-term heart health."
    elif visceral_fat <= 14.5:
        vf_status = "Slightly high"
        vf_inference = "A bit on the higher side - regular activity and mindful eating can help."
    else:
        vf_status = "High"
        vf_inference = "On the higher side - we recommend focusing on this with diet and lifestyle changes."

    elements.append(Paragraph("WHAT YOUR NUMBERS MEAN", heading_style))

    inference_data = [
        ['Measurement', 'Result', 'What It Means'],
        ['BMI', f"{bmi} kg/m\u00b2\n{bmi_category}", bmi_inference],
        ['Body Fat %', f"{body_fat}%", bf_status],
        ['Belly Fat', f"{visceral_fat}", f"{vf_status} - {vf_inference}"],
    ]

    wrapped_inference_data = [inference_data[0]]
    cell_style = ParagraphStyle('GeneralCellStyle', parent=styles['Normal'], fontSize=8, leading=10)
    for row in inference_data[1:]:
        wrapped_row = [row[0], row[1], Paragraph(row[2], cell_style)]
        wrapped_inference_data.append(wrapped_row)

    inference_table = Table(wrapped_inference_data, colWidths=[1.5*inch, 1.3*inch, 3.7*inch])
    inference_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
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

    # Simple wellness tips (no athlete language)
    tips = []
    tips.append(f"\u2022 Your body's metabolic age is {metabolic_age} years, compared to your actual age of {age} years.")
    if metabolic_age < age:
        tips.append("\u2022 \u2713 Great sign - your body is functioning like someone younger. Keep up the good habits!")
    elif metabolic_age > age:
        tips.append("\u2022 Regular physical activity, better sleep, and balanced nutrition can help improve this over time.")
    else:
        tips.append("\u2022 Your metabolic age matches your actual age.")

    tips.append("\u2022 Aim for at least 30 minutes of physical activity most days of the week.")
    tips.append("\u2022 Include more fruits, vegetables, whole grains, and lean protein in your daily meals.")
    tips.append("\u2022 Stay hydrated and aim for 7-8 hours of restful sleep every night.")
    tips.append("\u2022 Small, consistent lifestyle changes lead to lasting health improvements.")

    tips_text = "<br/>".join(tips)

    tips_heading_style = ParagraphStyle(
        'GeneralTipsHeading', parent=styles['Heading2'], fontSize=13,
        textColor=colors.HexColor('#27AE60'), spaceAfter=10, spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph("💡 🌿 Simple Tips for a Healthier You:", tips_heading_style))
    elements.append(Paragraph(
        tips_text,
        ParagraphStyle('GeneralTips', parent=styles['Normal'], fontSize=9,
                      leading=16, leftIndent=15, rightIndent=10, spaceAfter=8,
                      textColor=colors.HexColor('#2C3E50'))
    ))
    elements.append(Spacer(1, 0.4*inch))

    notes_style = ParagraphStyle(
        'GeneralNotes', parent=styles['Normal'], fontSize=9,
        textColor=colors.HexColor('#7F8C8D'), alignment=TA_LEFT
    )
    elements.append(Paragraph(
        "<b>Note:</b> This report gives you a simple snapshot of your current health and body composition. "
        "It is not a medical diagnosis. For a personalized nutrition and wellness plan, feel free to reach out "
        "to us by call or WhatsApp at +91-7397442544.",
        notes_style
    ))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph(
        "<i>Generated by PowerFuel - The Nutrition Hub</i>",
        ParagraphStyle('GeneralBranding', parent=styles['Normal'], fontSize=8,
                      textColor=colors.HexColor('#95A5A6'), alignment=TA_CENTER)
    ))

    doc.build(elements)

    return filename
