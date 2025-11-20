"""PDF report generation for contracts."""

import logging
from datetime import datetime
from pathlib import Path
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from lexguard.config import settings
from lexguard.models.contract import Contract
from lexguard.models.risk import ClauseRisk

logger = logging.getLogger(__name__)


def generate_pdf_report(
    contract: Contract, risks: List[ClauseRisk], summary: str, output_path: Path = None
) -> Path:
    """
    Generate a professional PDF risk report.

    Args:
        contract: Contract to report on
        risks: List of clause risk assessments
        summary: Contract summary text
        output_path: Optional output path (defaults to data/reports/)

    Returns:
        Path to generated PDF
    """
    if output_path is None:
        reports_dir = settings.data_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        output_path = reports_dir / f"report_{contract.id}.pdf"

    logger.info(f"Generating PDF report: {output_path}")

    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    # Build content
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=30,
        alignment=1,  # Center
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=colors.HexColor("#2c5aa0"),
        spaceAfter=12,
        spaceBefore=12,
    )

    # Title page
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("LexGuard Contract Risk Report", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # Contract info
    info_data = [
        ["Contract:", contract.title],
        ["File:", contract.original_filename],
        ["Analyzed:", datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")],
        ["Clauses:", str(len(contract.clauses))],
    ]

    info_table = Table(info_data, colWidths=[2 * inch, 4 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 10),
                ("FONT", (1, 0), (1, -1), "Helvetica", 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#333333")),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(info_table)
    story.append(PageBreak())

    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    for para in summary.split("\n\n"):
        if para.strip():
            story.append(Paragraph(para.replace("\n", "<br/>"), styles["BodyText"]))
            story.append(Spacer(1, 0.15 * inch))

    story.append(Spacer(1, 0.3 * inch))

    # Risk Overview
    story.append(Paragraph("Risk Overview", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    risk_counts = {"high": 0, "medium": 0, "low": 0}
    for risk in risks:
        if risk.level in risk_counts:
            risk_counts[risk.level] += 1

    risk_data = [
        ["Risk Level", "Count", "Percentage"],
        [
            "🔴 High",
            str(risk_counts["high"]),
            f"{risk_counts['high'] / len(risks) * 100:.1f}%" if risks else "0%",
        ],
        [
            "🟡 Medium",
            str(risk_counts["medium"]),
            f"{risk_counts['medium'] / len(risks) * 100:.1f}%" if risks else "0%",
        ],
        [
            "🟢 Low",
            str(risk_counts["low"]),
            f"{risk_counts['low'] / len(risks) * 100:.1f}%" if risks else "0%",
        ],
    ]

    risk_table = Table(risk_data, colWidths=[2 * inch, 1 * inch, 1.5 * inch])
    risk_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5aa0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ]
        )
    )
    story.append(risk_table)
    story.append(PageBreak())

    # Detailed Clause Analysis
    story.append(Paragraph("Detailed Clause Analysis", heading_style))
    story.append(Spacer(1, 0.2 * inch))

    # Sort by risk level
    sorted_risks = sorted(
        risks, key=lambda r: {"high": 0, "medium": 1, "low": 2}.get(r.level, 3)
    )

    for i, risk in enumerate(sorted_risks, 1):
        # Find corresponding clause
        clause = next((c for c in contract.clauses if c.id == risk.clause_id), None)
        if not clause:
            continue

        # Risk level indicator
        level_colors = {
            "high": "#dc3545",
            "medium": "#ffc107",
            "low": "#28a745",
        }
        level_text = risk.level.upper()
        level_color = level_colors.get(risk.level, "#6c757d")

        # Clause header
        if hasattr(clause.clause_type, "value"):
            type_str = clause.clause_type.value
        else:
            type_str = str(clause.clause_type)
            
        clause_title = f"Clause {i}: {type_str.replace('_', ' ').title()}"
        story.append(
            Paragraph(
                f'<font color="{level_color}">● </font><b>{clause_title}</b> '
                f'<font color="{level_color}">[{level_text}]</font>',
                styles["Heading3"],
            )
        )
        story.append(Spacer(1, 0.1 * inch))

        # Clause text (truncated)
        clause_text = clause.text[:300] + "..." if len(clause.text) > 300 else clause.text
        story.append(Paragraph(f"<i>{clause_text}</i>", styles["BodyText"]))
        story.append(Spacer(1, 0.1 * inch))

        # Risk reasons
        if risk.reasons:
            story.append(Paragraph("<b>Risk Factors:</b>", styles["BodyText"]))
            for reason in risk.reasons[:3]:  # Limit to top 3
                story.append(Paragraph(f"  • {reason}", styles["BodyText"]))
            story.append(Spacer(1, 0.1 * inch))

        # Recommendations
        if risk.recommendations:
            story.append(Paragraph("<b>Recommendations:</b>", styles["BodyText"]))
            for rec in risk.recommendations[:3]:  # Limit to top 3
                story.append(Paragraph(f"  • {rec}", styles["BodyText"]))

        story.append(Spacer(1, 0.25 * inch))

    # Build PDF
    doc.build(story)
    logger.info(f"PDF report generated: {output_path}")

    return output_path


