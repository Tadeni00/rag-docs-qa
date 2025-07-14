from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
import tempfile
import os
import re


def export_answer_to_pdf(answer, query, filename="answer.pdf"):
    temp_path = os.path.join(tempfile.gettempdir(), filename)

    doc = SimpleDocTemplate(temp_path, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='QueryTitle', fontSize=14, leading=18, spaceAfter=12, spaceBefore=12, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name='AnswerText', fontSize=12, leading=16))

    story = []

    story.append(Paragraph("Question:", styles['QueryTitle']))
    story.append(Paragraph(query, styles['AnswerText']))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("Answer:", styles['QueryTitle']))
    story.append(Paragraph(answer.replace("\n", "<br />"), styles['AnswerText']))  # preserve newlines
    story.append(Spacer(1, 0.3 * inch))

    doc.build(story)

    return temp_path



def clean_collection_name(name: str) -> str:
    name = name.strip().replace(" ", "-")
    name = re.sub(r"[^a-zA-Z0-9._-]", "", name)
    name = re.sub(r"^[^a-zA-Z]+", "", name)
    name = re.sub(r"[^a-zA-Z0-9]+$", "", name)
    return name if len(name) >= 3 else f"col-{name}"

def clean_pycache():
    pycache_path = os.path.join(os.path.dirname(__file__), "__pycache__")
    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path, ignore_errors=True)
