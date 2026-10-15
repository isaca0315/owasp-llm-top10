from langchain_core.prompts import PromptTemplate
from groq_llm import get_groq_model
import re
import time

llm = None

def get_llm():
    """Lazy-load LLM"""
    global llm
    if llm is None:
        try:
            llm = get_groq_model()
        except Exception as e:
            print(f"Warning: Could not initialize LLM: {e}")
            llm = None
    return llm

MITRE_MAP = {
    "T1059": "Command and Scripting Interpreter",
    "T1027": "Obfuscated Files or Information",
    "T1047": "Windows Management Instrumentation",
    "T1566": "Phishing",
    "T1203": "Exploitation for Client Execution",
    "T1053": "Scheduled Task/Job",
    "T1199": "Trusted Relationship",
}

def extract_mitre_techniques(text):
    """Stage 1: regex-based extraction"""
    return list(set(re.findall(r"T\d{4}(?:\.\d{3})?", text)))


def infer_mitre_techniques(text):
    """Stage 2: LLM-based inference when IDs are missing (with fallback)"""
    # Skip LLM inference to avoid rate limiting - use keyword fallback directly
    print("Using keyword-based fallback for MITRE technique inference (to avoid rate limits)")
    return _fallback_technique_inference(text)


def _fallback_technique_inference(text):
    """Fallback keyword-based technique inference when API is unavailable"""
    text_lower = text.lower()
    techniques = []
    
    # Keyword mapping to MITRE techniques
    keyword_map = {
        "T1059": ["command", "script", "powershell", "cmd", "bash", "shell"],
        "T1027": ["obfuscate", "encode", "encrypt", "hide", "packed"],
        "T1047": ["wmi", "windows management"],
        "T1566": ["phish", "email", "attachment", "link"],
        "T1203": ["exploit", "vulnerability", "cve"],
        "T1053": ["scheduled task", "cron", "at command"],
        "T1199": ["trusted", "supply chain", "third party"],
    }
    
    for technique_id, keywords in keyword_map.items():
        if any(keyword in text_lower for keyword in keywords):
            techniques.append(technique_id)
    
    return list(set(techniques))


def build_mitre_summary(techniques):
    return [
        {
            "technique_id": t,
            "name": MITRE_MAP.get(t, "Unknown Technique")
        }
        for t in techniques
    ]
