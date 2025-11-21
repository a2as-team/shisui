import os
import json
import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime
import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from html.parser import HTMLParser

# Create reports directory
REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

class HTMLToReportLab(HTMLParser):
    """Simple HTML parser to convert HTML to ReportLab flowables"""
    
    def __init__(self, styles):
        super().__init__()
        self.styles = styles
        self.story = []
        self.current_text = []
        self.current_style = 'Normal'
        self.in_list = False
        self.list_items = []
        self.table_data = []
        self.in_table = False
        self.current_row = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.current_style = 'Heading1'
        elif tag == 'h2':
            self.current_style = 'Heading2'
        elif tag == 'h3':
            self.current_style = 'Heading3'
        elif tag in ['ul', 'ol']:
            self.in_list = True
            self.list_items = []
        elif tag == 'table':
            self.in_table = True
            self.table_data = []
        elif tag == 'tr':
            self.current_row = []
        elif tag == 'strong':
            self.current_text.append('<b>')
        elif tag == 'em':
            self.current_text.append('<i>')
            
    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'p']:
            if self.current_text:
                text = ''.join(self.current_text).strip()
                if text:
                    self.story.append(Paragraph(text, self.styles[self.current_style]))
                    self.story.append(Spacer(1, 0.1*inch))
                self.current_text = []
            self.current_style = 'Normal'
        elif tag in ['ul', 'ol']:
            if self.list_items:
                for item in self.list_items:
                    self.story.append(Paragraph(f"• {item}", self.styles['Normal']))
                self.story.append(Spacer(1, 0.1*inch))
            self.in_list = False
            self.list_items = []
        elif tag == 'li':
            if self.current_text:
                self.list_items.append(''.join(self.current_text).strip())
                self.current_text = []
        elif tag == 'table':
            if self.table_data:
                # Calculate available width (letter size minus margins)
                available_width = letter[0] - 144  # 72pt margins on each side
                
                # Calculate column widths based on number of columns
                num_cols = len(self.table_data[0]) if self.table_data else 1
                col_width = available_width / num_cols
                
                # Wrap text in cells with Paragraph for better formatting
                wrapped_data = []
                for row in self.table_data:
                    wrapped_row = []
                    for cell in row:
                        # Use smaller font for table cells to fit more content
                        wrapped_row.append(Paragraph(str(cell), self.styles['Normal']))
                    wrapped_data.append(wrapped_row)
                
                t = Table(wrapped_data, colWidths=[col_width] * num_cols)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D3E1C4')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#00311e')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('FONTSIZE', (0, 1), (-1, -1), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
                ]))
                self.story.append(t)
                self.story.append(Spacer(1, 0.2*inch))
            self.in_table = False
            self.table_data = []
        elif tag == 'tr':
            if self.current_row:
                self.table_data.append(self.current_row)
                self.current_row = []
        elif tag in ['td', 'th']:
            if self.current_text:
                self.current_row.append(''.join(self.current_text).strip())
                self.current_text = []
        elif tag == 'strong':
            self.current_text.append('</b>')
        elif tag == 'em':
            self.current_text.append('</i>')
        elif tag == 'hr':
            self.story.append(Spacer(1, 0.2*inch))
            
    def handle_data(self, data):
        if data.strip():
            self.current_text.append(data)


def _generate_pdf_report(content: str, title: str = "Exam") -> str:
    """
    Generate a professional PDF report from markdown content.
    Returns the download URL.
    """
    try:
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"exam_{timestamp}.pdf"
        filepath = os.path.join(REPORTS_DIR, filename)
        
        # Clean up markdown content
        cleaned_content = content.replace('|\\', '|').replace('\\\n', '\n')
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(cleaned_content, extras=['tables', 'fenced-code-blocks'])
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=72)
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#00311e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Build story
        story = []
        
        # Add header
        story.append(Paragraph(f"📝 {title}", styles['CustomTitle']))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            ParagraphStyle('DateStyle', parent=styles['Normal'], 
                          alignment=TA_CENTER, textColor=colors.grey, fontSize=10)
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # Parse HTML and add to story
        parser = HTMLToReportLab(styles)
        parser.feed(html_content)
        story.extend(parser.story)
        
        # Add footer
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            "<i>Generated by Shisui Learning Assistant</i>",
            ParagraphStyle('FooterStyle', parent=styles['Normal'],
                          alignment=TA_CENTER, textColor=colors.grey, fontSize=9)
        ))
        
        # Build PDF
        doc.build(story)
        
        # Get the base URL from environment or use default
        base_url = os.environ.get('API_BASE_URL', 'http://localhost:8000')
        
        return f"{base_url}/reports/{filename}"
    
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return ""

def _get_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def generate_test(topic: str, difficulty: str = "medium", num_questions: int = 5) -> Dict[str, Any]:
    """
    Generates a test on a specific topic and creates a PDF.
    
    Args:
        topic: The subject matter to test
        difficulty: Difficulty level (easy, medium, hard)
        num_questions: Number of questions to generate
        
    Returns:
        Dictionary containing the test questions and PDF URL
    """
    model = _get_model()
    
    prompt = f"""
    Generate a {num_questions}-question test on "{topic}" with {difficulty} difficulty.
    Return ONLY a JSON object with this structure:
    {{
        "title": "Test Title",
        "questions": [
            {{
                "id": 1,
                "question": "Question text",
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct_answer": "A) Option 1",
                "explanation": "Why it is correct"
            }}
        ]
    }}
    """
    
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        test_data = json.loads(response.text)
        
        # Convert test data to Markdown for PDF
        markdown_content = f"# {test_data.get('title', 'Exam')}\n\n"
        markdown_content += f"**Topic:** {topic} | **Difficulty:** {difficulty}\n\n"
        markdown_content += "---\n\n"
        
        for q in test_data.get("questions", []):
            markdown_content += f"### Question {q['id']}\n\n"
            markdown_content += f"{q['question']}\n\n"
            for opt in q.get("options", []):
                markdown_content += f"- {opt}\n"
            markdown_content += "\n"
            
        # Generate PDF
        pdf_url = _generate_pdf_report(markdown_content, title=test_data.get('title', 'Exam'))
        
        # Add PDF URL to response
        test_data["pdf_url"] = pdf_url
        test_data["message"] = f"Exam generated successfully. You can download it here: {pdf_url}"
        
        return test_data
        
    except Exception as e:
        return {"error": f"Failed to generate test: {str(e)}"}

def evaluate_answer(question: str, user_answer: str, correct_answer: str) -> Dict[str, Any]:
    """
    Evaluates a user's answer.
    """
    model = _get_model()
    
    prompt = f"""
    Question: {question}
    Correct Answer: {correct_answer}
    User Answer: {user_answer}
    
    Evaluate the user's answer. Return JSON:
    {{
        "correct": boolean,
        "feedback": "Detailed feedback explaining why it's right or wrong"
    }}
    """
    
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Failed to evaluate: {str(e)}"}

def get_exam_tool():
    return generate_test

def get_eval_tool():
    return evaluate_answer
