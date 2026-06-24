import streamlit as st
import PyPDF2
import re
from datetime import datetime

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 3rem;
        margin: 0;
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .score-card:hover {
        transform: translateY(-5px);
    }
    .score-card h3 {
        font-size: 1rem;
        margin: 0;
        opacity: 0.9;
    }
    .score-card h1 {
        font-size: 2.5rem;
        margin: 0.5rem 0;
    }
    .score-card.green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .score-card.blue {
        background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
    }
    .score-card.orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .score-card.purple {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .keyword-tag {
        display: inline-block;
        background: #e8f4f8;
        color: #2c3e50;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.85rem;
        border: 1px solid #b8d4e3;
    }
    .keyword-tag.missing {
        background: #ffe8e8;
        border-color: #f5c6c6;
        color: #c0392b;
    }
    .suggestion-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .suggestion-box.warning {
        border-left-color: #f39c12;
        background: #fff8e1;
    }
    .suggestion-box.success {
        border-left-color: #27ae60;
        background: #e8f8f0;
    }
    .footer {
        text-align: center;
        color: #7f8c8d;
        padding: 2rem 0;
        margin-top: 2rem;
        border-top: 1px solid #ecf0f1;
    }
    .info-box {
        background: #f0f4f8;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 1px solid #dce4ec;
    }
    .info-box h3 {
        margin-top: 0;
        color: #2c3e50;
    }
    .info-box ul {
        margin-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📄 AI Resume Analyzer</h1>
    <p>Upload your resume and get instant AI-powered analysis with score and suggestions</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your resume in PDF format",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        file_size = uploaded_file.size / 1024
        st.markdown(f"""
        <div style="background: #e8f8f0; padding: 1rem; border-radius: 10px; border: 1px solid #27ae60;">
            File uploaded successfully<br>
            Name: {uploaded_file.name}<br>
            Size: {file_size:.1f} KB
        </div>
        """, unsafe_allow_html=True)
        
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_preview = ""
            for page in pdf_reader.pages[:2]:
                text_preview += page.extract_text()
            
            if text_preview:
                with st.expander("Resume Preview"):
                    st.text(text_preview[:500] + "..." if len(text_preview) > 500 else text_preview)
        except:
            pass

with col2:
    st.markdown("### Analysis Settings")
    
    job_role = st.text_input(
        "Target Job Role",
        placeholder="e.g., Software Engineer, Data Scientist, Product Manager"
    )
    
    st.markdown("**Quick Select:**")
    role_cols = st.columns(3)
    roles = ["Software Engineer", "Data Scientist", "DevOps Engineer"]
    for i, role in enumerate(roles):
        with role_cols[i]:
            if st.button(role, key=f"role_{i}", use_container_width=True):
                job_role = role
    
    experience = st.selectbox(
        "Experience Level",
        [
            "Entry Level (0-2 years)",
            "Mid Level (3-5 years)",
            "Senior Level (5-10 years)",
            "Expert Level (10+ years)"
        ]
    )
    
    st.markdown("---")
    analyze_btn = st.button("Analyze Resume", type="primary", use_container_width=True)

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return " ".join(text.split())
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_resume(text, job_role, experience):
    text_lower = text.lower()
    
    keywords = {
        "Technical Skills": {
            "Programming Languages": ["python", "java", "javascript", "c++", "ruby", "php", "swift", "kotlin", "go", "rust", "typescript", "c#", "scala"],
            "Web Development": ["html", "css", "react", "angular", "vue", "node.js", "django", "flask", "spring", "asp.net"],
            "Database": ["sql", "mysql", "postgresql", "mongodb", "oracle", "redis", "cassandra", "elasticsearch"],
            "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "ci/cd", "terraform", "ansible", "linux"],
            "Data Science & AI": ["machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn", "data mining", "statistics"]
        },
        "Soft Skills": {
            "Communication": ["communication", "presentation", "public speaking", "writing", "storytelling", "negotiation"],
            "Leadership": ["leadership", "management", "team lead", "supervisor", "mentor", "coach", "director"],
            "Problem Solving": ["problem solving", "analytical", "critical thinking", "troubleshooting", "strategic thinking"],
            "Teamwork": ["team", "collaboration", "cooperation", "interpersonal", "cross-functional"],
            "Adaptability": ["adaptability", "flexibility", "quick learner", "multitasking", "resilience"]
        },
        "Experience": {
            "Project Management": ["project", "managed", "led", "coordinated", "organized", "planned", "executed"],
            "Development": ["developed", "designed", "implemented", "created", "built", "programmed", "engineered"],
            "Achievements": ["achieved", "improved", "increased", "reduced", "delivered", "launched", "optimized"]
        },
        "Education": {
            "Degrees": ["bachelor", "master", "phd", "mba", "b.tech", "m.tech", "b.sc", "m.sc", "b.a", "m.a", "b.com", "m.com"],
            "Fields": ["computer science", "engineering", "management", "business", "mathematics", "physics", "chemistry", "biology", "economics", "finance"]
        }
    }
    
    role_specific = {
        "software engineer": ["agile", "scrum", "api", "microservices", "git", "unit testing", "debugging", "code review", "object oriented", "design patterns", "algorithms", "data structures"],
        "data scientist": ["statistics", "data visualization", "dashboard", "etl", "data cleaning", "feature engineering", "model deployment", "a/b testing", "analytics"],
        "devops engineer": ["ci/cd", "infrastructure", "monitoring", "automation", "scripting", "configuration management", "security", "networking", "load balancing"],
        "product manager": ["product strategy", "roadmap", "user stories", "product development", "market research", "competitive analysis", "product roadmap", "user feedback"],
        "frontend developer": ["ui", "ux", "responsive design", "web performance", "accessibility", "cross-browser", "frontend", "user interface"],
        "backend developer": ["api", "database", "server", "microservices", "cloud", "scalability", "backend", "data persistence"],
        "full stack developer": ["frontend", "backend", "database", "api", "cloud", "deployment", "full stack"],
        "machine learning engineer": ["model deployment", "feature engineering", "data pipeline", "mlops", "model evaluation", "hyperparameter tuning"]
    }
    
    results = {}
    total_found = 0
    total_possible = 0
    
    for category, subcategories in keywords.items():
        results[category] = {}
        category_found = 0
        category_possible = 0
        
        for subcategory, words in subcategories.items():
            found_words = []
            for word in words:
                if word in text_lower:
                    found_words.append(word)
            results[category][subcategory] = found_words
            category_found += len(found_words)
            category_possible += len(words)
            total_found += len(found_words)
            total_possible += len(words)
    
    role_keywords_found = []
    role_keywords_total = []
    
    job_lower = job_role.lower()
    for role, words in role_specific.items():
        if role in job_lower:
            for word in words:
                role_keywords_total.append(word)
                if word in text_lower:
                    role_keywords_found.append(word)
    
    overall_score = int((total_found / total_possible) * 100) if total_possible > 0 else 0
    
    category_scores = {}
    for category, subcategories in results.items():
        found = sum(len(words) for words in subcategories.values())
        total = sum(len(words) for words in keywords[category].values())
        category_scores[category] = int((found / total) * 100) if total > 0 else 0
    
    role_score = int((len(role_keywords_found) / len(role_keywords_total)) * 100) if role_keywords_total else 0
    
    suggestions = []
    
    if category_scores.get("Technical Skills", 0) < 40:
        suggestions.append("Add more technical skills relevant to your field. Include specific tools and frameworks you've used.")
    elif category_scores.get("Technical Skills", 0) < 60:
        suggestions.append("Consider adding more specific technical skills and technologies. Mention the tools you're most proficient in.")
    
    if category_scores.get("Soft Skills", 0) < 40:
        suggestions.append("Highlight communication, leadership, and teamwork abilities. Use specific examples of when you demonstrated these skills.")
    elif category_scores.get("Soft Skills", 0) < 60:
        suggestions.append("Add more soft skills and provide examples of how you've used them in professional settings.")
    
    if category_scores.get("Experience", 0) < 40:
        suggestions.append("Use numbers to show impact (e.g., 'Increased sales by 20%'). Include specific projects and achievements with measurable outcomes.")
    elif category_scores.get("Experience", 0) < 60:
        suggestions.append("Add more bullet points for each role. Focus on achievements, not just responsibilities.")
    
    if category_scores.get("Education", 0) < 30:
        suggestions.append("Clearly mention degrees, certifications, and relevant coursework. Include GPA if impressive.")
    
    if role_keywords_found:
        missing_role_keywords = [kw for kw in role_keywords_total if kw not in role_keywords_found]
        if missing_role_keywords:
            suggestions.append(f"Include these important keywords: {', '.join(missing_role_keywords[:5])}...")
    else:
        suggestions.append(f"Research common keywords for {job_role} positions and incorporate them into your resume.")
    
    if overall_score < 30:
        suggestions.append("Consider restructuring your resume. Use a professional template and focus on relevant experience.")
    elif overall_score < 50:
        suggestions.append("Focus on adding quantifiable achievements and relevant keywords. Consider consulting a career coach.")
    elif overall_score < 70:
        suggestions.append("Focus on adding more specific details and quantifying achievements.")
    elif overall_score < 85:
        suggestions.append("Add more specific technical skills and industry keywords.")
    else:
        suggestions.append("Your resume is highly competitive. Consider maintaining it and tailoring slightly for each application.")
    
    if len(text.split()) < 200:
        suggestions.append("Add more details about your experience, projects, and skills.")
    elif len(text.split()) > 800:
        suggestions.append("Consider trimming to 1-2 pages for better readability.")
    
    word_frequency = {}
    common_words = ["python", "java", "javascript", "sql", "aws", "docker", "kubernetes", 
                   "project", "team", "management", "leadership", "communication", "analytical"]
    
    for word in common_words:
        count = text_lower.count(word)
        if count > 0:
            word_frequency[word] = count
    
    return {
        "overall_score": overall_score,
        "category_scores": category_scores,
        "detailed_results": results,
        "suggestions": suggestions,
        "total_keywords_found": total_found,
        "total_keywords_possible": total_possible,
        "role_score": role_score,
        "role_keywords_found": role_keywords_found,
        "role_keywords_total": role_keywords_total,
        "word_frequency": word_frequency,
        "text_length": len(text.split())
    }

if analyze_btn:
    if uploaded_file is None:
        st.error("Please upload a resume first")
    elif not job_role:
        st.error("Please enter your target job role")
    else:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            
            if "Error" in resume_text:
                st.error(resume_text)
            else:
                analysis = analyze_resume(resume_text, job_role, experience)
                
                st.markdown("---")
                st.markdown("## Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="score-card">
                        <h3>Overall Score</h3>
                        <h1>{analysis['overall_score']}%</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="score-card blue">
                        <h3>Technical Skills</h3>
                        <h1>{analysis['category_scores'].get('Technical Skills', 0)}%</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="score-card orange">
                        <h3>Soft Skills</h3>
                        <h1>{analysis['category_scores'].get('Soft Skills', 0)}%</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="score-card purple">
                        <h3>{job_role} Match</h3>
                        <h1>{analysis['role_score']}%</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("### Overall Progress")
                st.progress(analysis['overall_score'] / 100)
                
                tab1, tab2, tab3, tab4 = st.tabs([
                    "Detailed Analysis",
                    "Suggestions",
                    "Keywords Found",
                    "Statistics"
                ])
                
                with tab1:
                    st.markdown("### Category-wise Analysis")
                    
                    for category, subcategories in analysis['detailed_results'].items():
                        st.markdown(f"#### {category}")
                        cols = st.columns(3)
                        
                        for idx, (subcategory, words) in enumerate(subcategories.items()):
                            with cols[idx % 3]:
                                if words:
                                    st.markdown(f"""
                                    <div style="background: #e8f8f0; padding: 0.8rem; border-radius: 8px; margin: 0.3rem 0; border-left: 3px solid #27ae60;">
                                        <b>Found: {subcategory}</b><br>
                                        <span style="font-size: 0.9rem;">Found: {len(words)}</span>
                                        <div style="font-size: 0.8rem; color: #7f8c8d; margin-top: 0.3rem;">
                                            {', '.join(words[:3])}{'...' if len(words) > 3 else ''}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div style="background: #fef0f0; padding: 0.8rem; border-radius: 8px; margin: 0.3rem 0; border-left: 3px solid #e74c3c;">
                                        <b>Not Found: {subcategory}</b><br>
                                        <span style="font-size: 0.9rem;">None found</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                
                with tab2:
                    st.markdown("### Improvement Suggestions")
                    
                    if analysis['suggestions']:
                        for suggestion in analysis['suggestions']:
                            if "competitive" in suggestion or "excellent" in suggestion:
                                st.markdown(f"""
                                <div class="suggestion-box success">
                                    {suggestion}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="suggestion-box warning">
                                    {suggestion}
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.success("No major suggestions found")
                    
                    st.markdown("---")
                    st.markdown("### Quick Resume Tips")
                    
                    tip_cols = st.columns(2)
                    tips = [
                        "Use action verbs (Developed, Led, Created)",
                        "Quantify achievements (Increased sales by 20%)",
                        "Tailor resume for each job application",
                        "Keep it concise - 1-2 pages maximum",
                        "Include relevant keywords from job description",
                        "Highlight most recent and relevant experience"
                    ]
                    for i, tip in enumerate(tips):
                        with tip_cols[i % 2]:
                            st.info(tip)
                
                with tab3:
                    st.markdown("### Keywords Found")
                    
                    all_keywords = []
                    for category, subcategories in analysis['detailed_results'].items():
                        for subcategory, words in subcategories.items():
                            all_keywords.extend(words)
                    
                    if all_keywords:
                        st.success(f"Total Keywords Found: {len(all_keywords)}")
                        
                        cols = st.columns(5)
                        for idx, keyword in enumerate(sorted(set(all_keywords))):
                            with cols[idx % 5]:
                                st.markdown(f"""
                                <span class="keyword-tag">{keyword}</span>
                                """, unsafe_allow_html=True)
                    
                    if analysis['role_keywords_total']:
                        st.markdown("### Job Role Keywords")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("Found:")
                            if analysis['role_keywords_found']:
                                for kw in analysis['role_keywords_found']:
                                    st.markdown(f'<span class="keyword-tag">{kw}</span>', unsafe_allow_html=True)
                            else:
                                st.write("None found")
                        
                        with col2:
                            st.markdown("Missing:")
                            missing = [kw for kw in analysis['role_keywords_total'] if kw not in analysis['role_keywords_found']]
                            if missing:
                                for kw in missing[:10]:
                                    st.markdown(f'<span class="keyword-tag missing">{kw}</span>', unsafe_allow_html=True)
                                if len(missing) > 10:
                                    st.write(f"... and {len(missing) - 10} more")
                            else:
                                st.success("All keywords found")
                
                with tab4:
                    st.markdown("### Resume Statistics")
                    
                    stat_col1, stat_col2, stat_col3 = st.columns(3)
                    with stat_col1:
                        st.metric("Word Count", analysis['text_length'])
                        st.metric("Total Keywords Found", analysis['total_keywords_found'])
                    with stat_col2:
                        st.metric("Keyword Match Rate", f"{int((analysis['total_keywords_found'] / analysis['total_keywords_possible']) * 100)}%")
                        st.metric("Role Match Rate", f"{analysis['role_score']}%")
                    with stat_col3:
                        st.metric("Categories Analyzed", len(analysis['detailed_results']))
                        st.metric("Sub-categories", sum(len(v) for v in analysis['detailed_results'].values()))
                    
                    if analysis['word_frequency']:
                        st.markdown("### Keyword Frequency")
                        freq_data = dict(sorted(analysis['word_frequency'].items(), key=lambda x: x[1], reverse=True))
                        for word, count in list(freq_data.items())[:10]:
                            st.text(f"{word}: {'█' * count} ({count} times)")
                
                st.markdown("---")
                
                report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report = f"""
RESUME ANALYSIS REPORT

Generated: {report_date}
Job Role: {job_role}
Experience Level: {experience}

OVERALL SCORE: {analysis['overall_score']}%

CATEGORY SCORES:
Technical Skills: {analysis['category_scores'].get('Technical Skills', 0)}%
Soft Skills: {analysis['category_scores'].get('Soft Skills', 0)}%
Experience: {analysis['category_scores'].get('Experience', 0)}%
Education: {analysis['category_scores'].get('Education', 0)}%

ROLE MATCH SCORE: {analysis['role_score']}%

DETAILED KEYWORD ANALYSIS:

"""
                for category, subcategories in analysis['detailed_results'].items():
                    report += f"\n{category}:\n"
                    for subcategory, words in subcategories.items():
                        status = "Found" if words else "Not Found"
                        report += f"   {status}: {subcategory} ({len(words)} found)\n"
                        if words:
                            report += f"      Keywords: {', '.join(words)}\n"

                report += """

SUGGESTIONS:

"""
                for i, suggestion in enumerate(analysis['suggestions'], 1):
                    report += f"   {i}. {suggestion}\n"

                report += f"""

STATISTICS:
Word Count: {analysis['text_length']}
Total Keywords Found: {analysis['total_keywords_found']}
Total Keywords Possible: {analysis['total_keywords_possible']}
Keyword Match Rate: {int((analysis['total_keywords_found'] / analysis['total_keywords_possible']) * 100)}%
Role Match Rate: {analysis['role_score']}%

Generated by AI Resume Analyzer
"""

                st.download_button(
                    label="Download Complete Analysis Report",
                    data=report,
                    file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

st.markdown("""
<div class="footer">
    <p>Built with Streamlit and Python</p>
    <p style="font-size: 0.8rem;">Your resume is processed locally and not stored anywhere</p>
</div>
""", unsafe_allow_html=True)