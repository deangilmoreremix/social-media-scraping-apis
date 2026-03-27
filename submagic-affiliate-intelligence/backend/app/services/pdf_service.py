from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from typing import Dict, Any
import io


class PDFService:
    """Service for generating PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#4F46E5')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#1F2937')
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            leading=14
        ))
    
    async def generate_report(self, report_data: Dict[str, Any]) -> bytes:
        """
        Generate PDF report from analysis data.
        Returns PDF as bytes.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Title
        story.append(Paragraph("Submagic Affiliate Intelligence Report", self.styles['MainTitle']))
        story.append(Spacer(1, 20))
        
        # Creator Info
        creator = report_data.get('creator', {})
        story.append(Paragraph(f"<b>Creator:</b> @{creator.get('username', 'N/A')}", self.styles['BodyText']))
        story.append(Paragraph(f"<b>Platform:</b> {creator.get('platform', 'N/A')}", self.styles['BodyText']))
        story.append(Paragraph(f"<b>Followers:</b> {creator.get('followers', 0):,}", self.styles['BodyText']))
        story.append(Paragraph(f"<b>Engagement Rate:</b> {creator.get('engagement_rate', 0)}%", self.styles['BodyText']))
        story.append(Spacer(1, 30))
        
        # Campaign Score Card
        analysis = report_data.get('analysis', {})
        story.append(Paragraph("Campaign Score Card", self.styles['SectionHeader']))
        
        scores = [
            ['Metric', 'Score', 'Assessment'],
            ['Audience Match', f"{analysis.get('audience_match', 0)}/100", self._get_assessment(analysis.get('audience_match', 0))],
            ['Content Fit', f"{analysis.get('content_fit', 0)}/100", self._get_assessment(analysis.get('content_fit', 0))],
            ['Conversion Potential', f"{analysis.get('conversion_potential', 0)}/100", self._get_assessment(analysis.get('conversion_potential', 0))]
        ]
        
        table = Table(scores, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 30))
        
        # Recommendations
        story.append(Paragraph("Recommended Materials", self.styles['SectionHeader']))
        
        materials = analysis.get('recommended_materials', [])
        for i, mat in enumerate(materials, 1):
            story.append(Paragraph(f"<b>{i}. {mat.get('material', 'N/A')} (Match: {mat.get('score', 0)}%)</b>", self.styles['BodyText']))
            story.append(Paragraph(mat.get('reasoning', ''), self.styles['BodyText']))
            story.append(Spacer(1, 10))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _get_assessment(self, score: int) -> str:
        """Get assessment text based on score"""
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Needs Work"
