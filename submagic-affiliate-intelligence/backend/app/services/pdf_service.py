import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, Any
from datetime import datetime


class PDFService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#6366F1')
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
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#374151')
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            leading=14
        ))
        
        self.styles.add(ParagraphStyle(
            name='ScoreText',
            parent=self.styles['Normal'],
            fontSize=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#059669')
        ))
    
    async def generate_report_pdf(self, report_id: str, report_data: Dict[str, Any] = None) -> str:
        """Generate a PDF report for a creator"""
        if not report_data:
            report_data = await self._get_report_data(report_id)
        
        output_dir = tempfile.gettempdir()
        output_path = os.path.join(output_dir, f"report_{report_id}.pdf")
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        story.extend(self._build_header(report_data))
        story.extend(self._build_profile_summary(report_data))
        story.extend(self._build_score_card(report_data))
        story.extend(self._build_recommendations(report_data))
        story.extend(self._build_footer())
        
        doc.build(story)
        return output_path
    
    def _build_header(self, report_data: Dict[str, Any]) -> list:
        """Build the PDF header section"""
        elements = []
        
        elements.append(Paragraph(
            "Submagic Affiliate Intelligence",
            self.styles['MainTitle']
        ))
        
        elements.append(Spacer(1, 20))
        
        username = report_data.get('creator_username', 'Unknown Creator')
        platform = report_data.get('creator_platform', 'Social Media')
        
        elements.append(Paragraph(
            f"Creator Analysis Report",
            self.styles['SectionHeader']
        ))
        
        elements.append(Paragraph(
            f"<b>Creator:</b> @{username} ({platform.title()})",
            self.styles['BodyText']
        ))
        
        elements.append(Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p EST')}",
            self.styles['BodyText']
        ))
        
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _build_profile_summary(self, report_data: Dict[str, Any]) -> list:
        """Build the profile summary section"""
        elements = []
        
        elements.append(Paragraph(
            "Creator Profile Summary",
            self.styles['SectionHeader']
        ))
        
        profile = report_data.get('profile_summary', {})
        
        summary_data = [
            ['Metric', 'Value'],
            ['Platform', profile.get('platform', 'N/A').title()],
            ['Username', f"@{profile.get('username', 'N/A')}"],
            ['Follower Count', f"{profile.get('follower_count', 'N/A'):,}" if isinstance(profile.get('follower_count'), int) else str(profile.get('follower_count', 'N/A'))],
            ['Engagement Rate', f"{profile.get('engagement_estimate', 'N/A')}%"],
            ['Audience Match', profile.get('audience_overlap_with_submagic', 'N/A')]
        ]
        
        table = Table(summary_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366F1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        elements.append(PageBreak())
        
        return elements
    
    def _build_score_card(self, report_data: Dict[str, Any]) -> list:
        """Build the campaign score card section"""
        elements = []
        
        elements.append(Paragraph(
            "Campaign Score Card",
            self.styles['SectionHeader']
        ))
        
        score_card = report_data.get('score_card', {})
        
        scores = [
            ['Score Type', 'Value', 'Rating'],
            ['Audience Match', f"{score_card.get('audience_match_score', 0)}/100", self._get_rating(score_card.get('audience_match_score', 0))],
            ['Content Fit', f"{score_card.get('content_fit_score', 0)}/100", self._get_rating(score_card.get('content_fit_score', 0))],
            ['Conversion Potential', f"{score_card.get('conversion_potential_score', 0)}/100", self._get_rating(score_card.get('conversion_potential_score', 0))],
            ['OVERALL', f"{score_card.get('overall_score', 0)}/100", self._get_rating(score_card.get('overall_score', 0))]
        ]
        
        table = Table(scores, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#6366F1')),
            ('TEXTCOLOR', (0, 4), (-1, 4), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        reasoning = score_card.get('reasoning', {})
        if reasoning:
            elements.append(Paragraph(
                "<b>Score Explanations:</b>",
                self.styles['SubHeader']
            ))
            for key, value in reasoning.items():
                score_name = key.replace('_', ' ').title()
                elements.append(Paragraph(
                    f"<b>{score_name}:</b> {value}",
                    self.styles['BodyText']
                ))
        
        elements.append(PageBreak())
        return elements
    
    def _build_recommendations(self, report_data: Dict[str, Any]) -> list:
        """Build the recommendations section"""
        elements = []
        
        elements.append(Paragraph(
            "Recommended Affiliate Materials",
            self.styles['SectionHeader']
        ))
        
        recommendations = report_data.get('recommendations', [])
        
        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(
                f"<b>Recommendation #{i}: {rec.get('material_name', 'N/A')}</b>",
                self.styles['SubHeader']
            ))
            
            rec_data = [
                ['Detail', 'Value'],
                ['Platform', rec.get('platform', 'N/A').title()],
                ['Content Type', rec.get('content_type', 'N/A').replace('_', ' ').title()],
                ['Match Score', f"{rec.get('match_score', 0)}%"]
            ]
            
            table = Table(rec_data, colWidths=[1.5*inch, 4.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 10))
            
            elements.append(Paragraph(
                f"<b>Why This Works:</b> {rec.get('reasoning', 'No reasoning provided')}",
                self.styles['BodyText']
            ))
            
            if rec.get('suggested_posting_times'):
                times = ', '.join(rec.get('suggested_posting_times', []))
                elements.append(Paragraph(
                    f"<b>Best Posting Times:</b> {times}",
                    self.styles['BodyText']
                ))
            
            if rec.get('tips_for_maximum_engagement'):
                elements.append(Spacer(1, 5))
                elements.append(Paragraph(
                    "<b>Tips for Maximum Engagement:</b>",
                    self.styles['BodyText']
                ))
                for tip in rec.get('tips_for_maximum_engagement', []):
                    elements.append(Paragraph(
                        f"• {tip}",
                        self.styles['BodyText']
                    ))
            
            elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_footer(self) -> list:
        """Build the PDF footer"""
        elements = []
        
        elements.append(Spacer(1, 40))
        elements.append(Paragraph(
            "Executive Summary",
            self.styles['SectionHeader']
        ))
        
        elements.append(Paragraph(
            "This report was generated by Submagic's AI-powered Affiliate Intelligence Platform. "
            "The recommendations are based on analysis of the creator's profile, content style, "
            "audience demographics, and historical performance data of similar affiliate campaigns.",
            self.styles['BodyText']
        ))
        
        elements.append(Spacer(1, 30))
        
        footer_data = [
            ['Generated by', 'Submagic Affiliate Intelligence Platform'],
            ['Platform', 'submagic-affiliate-intelligence'],
            ['Version', '1.0.0']
        ]
        
        table = Table(footer_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _get_rating(self, score: int) -> str:
        """Convert score to rating text"""
        if score >= 90:
            return "⭐ Exceptional"
        elif score >= 75:
            return "✅ Excellent"
        elif score >= 60:
            return "👍 Good"
        elif score >= 40:
            return "⚠️ Fair"
        else:
            return "❌ Needs Work"
    
    async def _get_report_data(self, report_id: str) -> Dict[str, Any]:
        """Get report data by ID (placeholder - connect to database)"""
        return {
            "creator_username": "sample_creator",
            "creator_platform": "instagram",
            "profile_summary": {
                "username": "sample_creator",
                "platform": "instagram",
                "follower_count": 45000,
                "engagement_estimate": 3.2,
                "audience_overlap_with_submagic": "High"
            },
            "score_card": {
                "audience_match_score": 85,
                "content_fit_score": 78,
                "conversion_potential_score": 72,
                "overall_score": 78,
                "reasoning": {
                    "audience_match": "Strong alignment with content creators and businesses.",
                    "content_fit": "Content style aligns well with Submagic's brand.",
                    "conversion": "Good engagement rate suggests high conversion potential."
                }
            },
            "recommendations": [
                {
                    "material_name": "Instagram Reels Tutorial",
                    "platform": "instagram",
                    "content_type": "tutorial",
                    "match_score": 92,
                    "reasoning": "Perfect match for your content style.",
                    "suggested_posting_times": ["9 AM EST", "12 PM EST"],
                    "tips_for_maximum_engagement": ["Show clear UI", "Use trending audio"]
                }
            ],
            "executive_summary": "This creator shows strong potential for Submagic affiliate partnerships."
        }
