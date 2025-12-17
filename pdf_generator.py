
import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage
import requests
from flask import current_app

class PortfolioPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        styles = {}
        
        # Title style
        styles['CustomTitle'] = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c5aa0')
        )
        
        # Subtitle style
        styles['CustomSubtitle'] = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#1f4788')
        )
        
        # Body style
        styles['CustomBody'] = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=14
        )
        
        # Feature list style
        styles['FeatureList'] = ParagraphStyle(
            'FeatureList',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leftIndent=20,
            bulletIndent=10
        )
        
        return styles
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(colors.HexColor('#2c5aa0'))
        canvas.drawString(50, letter[1] - 50, "BizzPulse Portfolio")
        
        # Footer
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(50, 30, f"Generated on {datetime.now().strftime('%B %d, %Y')}")
        canvas.drawRightString(letter[0] - 50, 30, f"Page {doc.page}")
        
        canvas.restoreState()
    
    def _process_image(self, image_path, max_width=4*inch, max_height=3*inch):
        """Process and resize image for PDF"""
        try:
            if os.path.exists(image_path):
                # Local file
                pil_img = PILImage.open(image_path)
            else:
                # Assume it's a URL or create a placeholder
                return self._create_placeholder_image(max_width, max_height)
            
            # Calculate new dimensions maintaining aspect ratio
            width, height = pil_img.size
            aspect_ratio = width / height
            
            if width > height:
                new_width = min(max_width, width)
                new_height = new_width / aspect_ratio
                if new_height > max_height:
                    new_height = max_height
                    new_width = new_height * aspect_ratio
            else:
                new_height = min(max_height, height)
                new_width = new_height * aspect_ratio
                if new_width > max_width:
                    new_width = max_width
                    new_height = new_width / aspect_ratio
            
            return Image(image_path, width=new_width, height=new_height)
            
        except Exception as e:
            current_app.logger.warning(f"Could not process image {image_path}: {str(e)}")
            return self._create_placeholder_image(max_width, max_height)
    
    def _create_placeholder_image(self, width, height):
        """Create a placeholder image when actual image is not available"""
        from reportlab.graphics.shapes import Drawing, Rect, String
        from reportlab.graphics import renderPDF
        
        # Create a simple placeholder rectangle
        placeholder = Drawing(width, height)
        placeholder.add(Rect(0, 0, width, height, fillColor=colors.lightgrey, strokeColor=colors.grey))
        placeholder.add(String(width/2, height/2, "Portfolio Image", textAnchor="middle", fontSize=12))
        
        return placeholder
    
    def generate_portfolio_pdf(self, portfolio_data):
        """Generate a comprehensive portfolio PDF"""
        buffer = io.BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=80,
            bottomMargin=50
        )
        
        # Build story (content)
        story = []
        
        # Title Page
        story.append(Paragraph("Portfolio Details", self.custom_styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Project Badge and Meta Information
        meta_data = [
            ['Project Type:', portfolio_data.get('project_type', 'UX/UI Design')],
            ['Date:', portfolio_data.get('date', 'September 2024')],
            ['Client:', portfolio_data.get('client', 'DigitalCraft Solutions')],
            ['Website:', portfolio_data.get('website', 'projectwebsite.example.com')]
        ]
        
        meta_table = Table(meta_data, colWidths=[1.5*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c5aa0')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 30))
        
        # Project Title
        story.append(Paragraph(
            portfolio_data.get('title', 'Innovative Financial Dashboard App'),
            self.custom_styles['CustomTitle']
        ))
        story.append(Spacer(1, 20))
        
        # Main Project Images
        story.append(Paragraph("Project Screenshots", self.custom_styles['CustomSubtitle']))
        story.append(Spacer(1, 10))
        
        # Add main portfolio images
        main_images = [
            'static/img/portfolio/portfolio-5.webp',
            'static/img/portfolio/portfolio-7.webp',
            'static/img/portfolio/portfolio-8.webp'
        ]
        
        for img_path in main_images:
            if os.path.exists(img_path):
                img = self._process_image(img_path, max_width=5*inch, max_height=3.5*inch)
                story.append(img)
                story.append(Spacer(1, 15))
        
        # Project Overview
        story.append(Paragraph("Project Overview", self.custom_styles['CustomSubtitle']))
        overview_text = portfolio_data.get('overview', 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas varius "
            "tortor nibh, sit amet tempor nibh finibus et. Aenean eu enim justo. "
            "Vestibulum aliquam hendrerit molestie. Cras ultricies ligula sed magna "
            "dictum porta. Nulla quis lorem ut libero malesuada feugiat."
        )
        story.append(Paragraph(overview_text, self.custom_styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # The Challenge
        story.append(Paragraph("The Challenge", self.custom_styles['CustomSubtitle']))
        challenge_text = portfolio_data.get('challenge',
            "Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Vivamus "
            "suscipit tortor eget felis porttitor volutpat. Curabitur aliquet quam "
            "id dui posuere blandit. Praesent sapien massa, convallis a pellentesque "
            "nec, egestas non nisi."
        )
        story.append(Paragraph(challenge_text, self.custom_styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # The Solution
        story.append(Paragraph("The Solution", self.custom_styles['CustomSubtitle']))
        solution_text = portfolio_data.get('solution',
            "Donec sollicitudin molestie malesuada. Curabitur arcu erat, accumsan id "
            "imperdiet et, porttitor at sem. Vestibulum ante ipsum primis in faucibus "
            "orci luctus et ultrices posuere cubilia Curae; Donec velit neque, auctor "
            "sit amet aliquam vel, ullamcorper sit amet ligula."
        )
        story.append(Paragraph(solution_text, self.custom_styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Key Features
        story.append(Paragraph("Key Features", self.custom_styles['CustomSubtitle']))
        features = portfolio_data.get('features', [
            "Real-time Data Visualization",
            "User Role Management", 
            "Secure Authentication",
            "Customizable Dashboards",
            "Data Export Options",
            "Multi-device Support"
        ])
        
        for feature in features:
            story.append(Paragraph(f"• {feature}", self.custom_styles['FeatureList']))
        
        story.append(Spacer(1, 20))
        
        # Technology Stack
        story.append(Paragraph("Technology Stack", self.custom_styles['CustomSubtitle']))
        tech_stack = portfolio_data.get('tech_stack', [
            'Angular', 'Express.js', 'PostgreSQL', 'GraphQL', 'Firebase'
        ])
        
        tech_text = ", ".join(tech_stack)
        story.append(Paragraph(tech_text, self.custom_styles['CustomBody']))
        story.append(Spacer(1, 30))
        
        # Gallery Images (if any)
        gallery_images = [
            'static/img/portfolio/portfolio-4.webp',
            'static/img/portfolio/portfolio-6.webp',
            'static/img/portfolio/portfolio-11.webp',
            'static/img/portfolio/portfolio-12.webp'
        ]
        
        story.append(Paragraph("Additional Screenshots", self.custom_styles['CustomSubtitle']))
        story.append(Spacer(1, 10))
        
        # Create a 2x2 grid of smaller images
        for i in range(0, len(gallery_images), 2):
            row_images = []
            for j in range(2):
                if i + j < len(gallery_images):
                    img_path = gallery_images[i + j]
                    if os.path.exists(img_path):
                        img = self._process_image(img_path, max_width=2.5*inch, max_height=2*inch)
                        row_images.append(img)
                    else:
                        row_images.append(self._create_placeholder_image(2.5*inch, 2*inch))
            
            if len(row_images) == 2:
                img_table = Table([row_images], colWidths=[2.8*inch, 2.8*inch])
                img_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ]))
                story.append(img_table)
                story.append(Spacer(1, 15))
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        buffer.seek(0)
        return buffer

    def generate_simple_pdf(self):
        """Generate a simple portfolio PDF with default data"""
        default_data = {
            'project_type': 'UX/UI Design',
            'date': 'September 2024',
            'client': 'DigitalCraft Solutions',
            'website': 'projectwebsite.example.com',
            'title': 'Innovative Financial Dashboard App',
            'overview': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas varius tortor nibh, sit amet tempor nibh finibus et. Aenean eu enim justo. Vestibulum aliquam hendrerit molestie.',
            'challenge': 'Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Vivamus suscipit tortor eget felis porttitor volutpat.',
            'solution': 'Donec sollicitudin molestie malesuada. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem.',
            'features': [
                'Real-time Data Visualization',
                'User Role Management',
                'Secure Authentication',
                'Customizable Dashboards',
                'Data Export Options',
                'Multi-device Support'
            ],
            'tech_stack': ['Angular', 'Express.js', 'PostgreSQL', 'GraphQL', 'Firebase']
        }
        
        return self.generate_portfolio_pdf(default_data)
