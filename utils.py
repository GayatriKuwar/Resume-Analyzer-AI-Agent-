import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        # Extract text from each page
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        if not text.strip():
            return "⚠️ No text could be extracted from this PDF. Please make sure it's a text-based PDF."
        
        return text
    except Exception as e:
        return f"❌ Error extracting text: {str(e)}"
        
def calculate_keyword_score(text, job_role):
    """Calculate keyword match score based on job role"""
    # Common keywords for different roles
    keywords = {
        "Software Engineer": ["python", "java", "javascript", "sql", "aws", "docker", "git", 
                             "react", "node.js", "agile", "scrum", "api", "microservices"],
        "Data Scientist": ["python", "r", "sql", "machine learning", "data analysis", "statistics",
                          "tensorflow", "pytorch", "pandas", "numpy", "visualization"],
        "DevOps Engineer": ["aws", "docker", "kubernetes", "ci/cd", "linux", "bash", "python",
                           "terraform", "ansible", "jenkins", "monitoring"],
        "Product Manager": ["product strategy", "roadmap", "agile", "scrum", "user stories",
                           "analytics", "market research", "product development"]
    }
    
    # Get keywords for specified role or use general
    role_keywords = keywords.get(job_role, ["python", "sql", "javascript", "project", "team"])
    
    text_lower = text.lower()
    found_keywords = [kw for kw in role_keywords if kw.lower() in text_lower]
    
    score = min(100, int((len(found_keywords) / len(role_keywords)) * 100))
    return score, found_keywords

def analyze_keyword_density(text):
    """Analyze keyword density and provide suggestions"""
    common_skills = ["python", "java", "javascript", "sql", "aws", "docker", "kubernetes",
                    "machine learning", "ai", "data", "analysis", "project management", "agile"]
    
    text_lower = text.lower()
    analysis = {}
    
    for skill in common_skills:
        count = text_lower.count(skill)
        if count > 0:
            analysis[skill] = count
    
    return analysis