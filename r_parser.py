import pdfplumber
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_name(text):
    lines = text.strip().split('\n')

    # check first few lines
    for line in lines[:5]:
        line = line.strip()

        # ignore empty or long lines
        if len(line) > 2 and len(line.split()) <= 3:
            return line

    return "Not Found"
def extract_email(text):
    emails = re.findall(r'\S+@\S+', text)
    return list(set(emails))   # removes duplicates

def extract_phone(text):
    phones = re.findall(r'\+?\d[\d\s\-]{8,}\d', text)

    cleaned = []
    for phone in phones:
        # remove spaces and dashes
        p = re.sub(r'[\s\-]', '', phone)

        # remove + sign
        p = p.replace("+", "")

        # keep last 10 digits (Indian number)
        if len(p) >= 10:
            p = p[-10:]
            cleaned.append(p)

    return list(set(cleaned))

skills_list = [
    "python", "java", "c++", "sql",
    "project management", "public relations",
    "teamwork", "time management",
    "leadership", "effective communication",
    "critical thinking"
]

def extract_skills(text):
    text = text.lower()
    found = []

    for skill in skills_list:
        if skill.lower() in text:
            found.append(skill)

    return list(set(found))

def extract_education(text):
    education_keywords = [
        "b.tech", "bachelor", "master", "m.tech",
        "bsc", "msc", "mba", "phd", "degree",
        "university", "college", "school"
    ]

    lines = text.lower().split('\n')
    found = []

    for line in lines:
        for keyword in education_keywords:
            if keyword in line:
                found.append(line.strip())

    return list(set(found))