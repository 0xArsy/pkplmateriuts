import os
import json
import re

def extract_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    # Basic text extraction from HTML
    # 1. Remove script and style
    html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # 2. Extract content from specific tags
    tags_to_extract = re.findall(r'<(h[1-6]|p|li|td|strong|em|span|b|i|code).*?>(.*?)</\1>', html, flags=re.DOTALL | re.IGNORECASE)
    
    text_content = []
    for tag, content in tags_to_extract:
        # Clean tags inside content
        clean_text = re.sub(r'<.*?>', '', content)
        clean_text = clean_text.strip().replace('\n', ' ')
        if clean_text:
            text_content.append(clean_text)
            
    return " ".join(text_content)

def build_index():
    # PKPL portal has two main learning files
    chapters = [
        {
            "id": "soal-deep-dive",
            "title": "Soal + Conceptual Deep Dive (50 Soal UTS)",
            "file": "SOAL+CONCEPTUALDEEPDIVE.html"
        },
        {
            "id": "deep-dive-2",
            "title": "Conceptual Deep Dive 2 + Latihan Interaktif (15 Soal)",
            "file": "CONCEPTUALDEEPDIVE2.html"
        },
    ]

    # Extended keyword sets for PKPL topics
    pkpl_keywords = {
        "soal-deep-dive": [
            "software security", "CIA Triad", "Confidentiality", "Integrity", "Availability",
            "SSDLC", "Secure SDLC", "threat modeling", "OWASP", "OWASP Top 10",
            "SQL Injection", "XSS", "Cross-Site Scripting", "Man-in-the-Middle",
            "Brute Force", "Session Hijacking", "Social Engineering", "Phishing",
            "hashing", "salting", "enkripsi", "simetris", "asimetris", "AES", "RSA",
            "bcrypt", "SHA-256", "rainbow table", "zero-day", "vulnerability",
            "penetration testing", "SAST", "DAST", "SonarQube", "OWASP ZAP", "Fortify",
            "least privilege", "defense in depth", "MFA", "access control",
            "authentication", "authorization", "firewall", "security audit",
            "input validation", "prepared statement", "buffer overflow",
            "DoS", "DDoS", "code obfuscation", "logging", "monitoring",
            "CVE", "patch management", "security patching", "data breach",
            "black-box", "white-box", "CSP", "Content Security Policy",
            "HiJacking", "captcha", "backup", "default credentials",
        ],
        "deep-dive-2": [
            "CIA Triad", "Confidentiality", "Integrity", "Availability",
            "SSDLC", "Secure SDLC", "Requirements", "Design", "Implementation", "Testing", "Deployment",
            "SQL Injection", "XSS", "Cross-Site Scripting", "Man-in-the-Middle",
            "Brute Force", "Session Hijacking", "Social Engineering",
            "password hashing", "password salting", "salting", "hashing", "one-way",
            "enkripsi simetris", "enkripsi asimetris", "AES", "RSA", "bcrypt",
            "SHA-256", "rainbow table", "zero-day", "least privilege", "defense in depth",
            "prepared statement", "parameterized query", "SonarQube", "OWASP ZAP",
            "static code analysis", "SAST", "DAST", "penetration testing",
            "MFA", "multi-factor authentication", "key terms", "vulnerability",
            "threat modeling", "secure coding", "key exchange", "HTTPS",
        ],
    }

    search_index = []
    for chapter in chapters:
        file_path = chapter['file']
        if os.path.exists(file_path):
            print(f"Indexing {file_path}...")
            content = extract_content(file_path)
            content = re.sub(r'\s+', ' ', content).strip()

            # Use extended keyword list from chapter id + auto-extracted
            base_keywords = pkpl_keywords.get(chapter['id'], [])
            auto_keywords = list(set(re.findall(r'\b\w{4,}\b', content.lower())))
            # Combine and deduplicate (case-insensitive)
            all_keywords = list(set([k.lower() for k in base_keywords] + auto_keywords))

            search_index.append({
                "title": chapter['title'],
                "file": chapter['file'],
                "keywords": all_keywords,
                "preview": content[:200] + "..."
            })
        else:
            print(f"WARNING: {file_path} not found, skipping.")
            
    with open('search_index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)

    print(f"\n✅ search_index.json built with {len(search_index)} entries.")

if __name__ == "__main__":
    build_index()
