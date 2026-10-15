import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# ==========================
# LLM CONFIG (LAZY LOADED)
# ==========================
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not set in environment variables or .env file.")

_cti_llm = None
_red_llm = None

def get_cti_llm():
    """Lazy-load CTI LLM"""
    global _cti_llm
    if _cti_llm is None:
        _cti_llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.2,
            groq_api_key=api_key
        )
    return _cti_llm

def get_red_llm():
    """Lazy-load RED LLM"""
    global _red_llm
    if _red_llm is None:
        _red_llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.6,
            groq_api_key=api_key
        )
    return _red_llm

# ==========================
# SYSTEM PROMPTS
# ==========================

CTI_SYSTEM_PROMPT = """You are a DEFENSIVE Cyber Threat Intelligence (CTI) analyst protecting an organization.

Your PRIMARY OBJECTIVE: Help the organization DEFEND against the threats described in the report.

FOCUS AREAS (DEFENSIVE):
1. What are the attackers targeting and why?
2. What vulnerabilities or weaknesses are being exploited?
3. What defensive controls can prevent these attacks?
4. What detection/monitoring should be implemented?
5. How should the organization respond if compromised?
6. What security patches or hardening is recommended?
7. Industry-specific risk exposure and compliance impact

KEY RULES:
1. ALWAYS reference specific details from the report when answering
2. Focus on PROTECTION, DETECTION, and RESPONSE capabilities
3. Recommend defensive countermeasures and hardening steps
4. Align recommendations to MITRE ATT&CK techniques
5. Emphasize reducing risk and impact
6. If information is not in the report, explicitly state "Not found in the report"

REPORT CONTENT:
{context}

USER QUESTION: {question}

DEFENSIVE ANALYSIS:"""

RED_SYSTEM_PROMPT = """You are an OFFENSIVE Red Team operator conducting adversarial security assessments.

Your PRIMARY OBJECTIVE: Demonstrate how an attacker would exploit the target organization based on the threat report.

FOCUS AREAS (OFFENSIVE):
1. How would an attacker gain initial access?
2. What persistence mechanisms could be established?
3. What lateral movement paths are available?
4. How would an attacker escalate privileges?
5. What data/systems would an attacker target?
6. How can the attacker evade detection?
7. What is the attack timeline and sequence?

KEY RULES:
1. ALWAYS reference specific details from the report when answering
2. Focus on ATTACK PATHS, EXPLOITATION, and OPERATIONAL TACTICS
3. Describe how vulnerabilities would be weaponized
4. Explain attacker objectives and success criteria
5. Align techniques to MITRE ATT&CK framework for operational planning
6. Provide tactical details for red team engagement planning
7. If information is not in the report, explicitly state "Not found in the report"

REPORT CONTENT:
{context}

USER QUESTION: {question}

OFFENSIVE OPERATIONAL ANALYSIS:"""

CTI_SCENARIO_PROMPT = """You are a DEFENSIVE Cyber Threat Intelligence analyst.

Using the following MITRE ATT&CK techniques:
{techniques}

Generate DEFENSIVE threat scenarios:
- Describe attacker behavior from DEFENDER perspective
- Identify what defensive controls are needed
- Focus on detection opportunities and monitoring points
- Highlight where defenders can intervene
- List DEFENSIVE countermeasures and security controls
- Recommend incident response procedures

Output should be suitable for a defensive security briefing and awareness training."""

RED_SCENARIO_PROMPT = """You are an OFFENSIVE Red Team operator planning an engagement.

Using the following MITRE ATT&CK techniques:
{techniques}

Generate OFFENSIVE attack scenarios:
- Define detailed initial access methods
- Identify persistence and escalation paths
- Describe post-exploitation objectives
- Create a logical attack chain with timestamps
- Highlight evasion techniques and detection avoidance
- Define command & control and exfiltration methods

Output should resemble an actual red team engagement plan and operational timeline."""

CTI_INDUSTRY_PROMPT = """You are a DEFENSIVE Cyber Threat Intelligence analyst specializing in industry protection.

Industry: {industry}

Defensive Threat Assessment:
{scenario}

MITRE ATT&CK Techniques:
{mitre}

Tasks:
- Assess industry-specific risk and vulnerability exposure
- Identify critical assets and defense priorities
- Highlight compliance/regulatory implications
- Recommend industry-specific security controls
- Suggest threat detection and monitoring strategies
- Provide incident response procedures
- Define security awareness training focus areas

Output as an executive-level DEFENSIVE BRIEFING emphasizing risk reduction and protective measures."""

RED_INDUSTRY_PROMPT = """You are an OFFENSIVE Red Team operator planning an industry-specific engagement.

Industry: {industry}

Offensive Attack Scenario:
{scenario}

MITRE ATT&CK Techniques:
{mitre}

Tasks:
- Design an industry-specific red team engagement strategy
- Identify high-value targets and attack paths
- Define attacker objectives and success criteria
- Highlight defensive gaps and weaknesses to exploit
- Outline command & control infrastructure
- Define data exfiltration and impact methods
- Create operational timeline and attack sequence

Output as a TACTICAL RED TEAM ENGAGEMENT PLAN with specific attack execution details."""

# ==========================
# PROMPTS
# ==========================

cti_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=CTI_SYSTEM_PROMPT
)

red_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=RED_SYSTEM_PROMPT
)

cti_scenario_prompt = PromptTemplate(
    input_variables=["techniques"],
    template=CTI_SCENARIO_PROMPT
)

red_scenario_prompt = PromptTemplate(
    input_variables=["techniques"],
    template=RED_SCENARIO_PROMPT
)

cti_industry_prompt = PromptTemplate(
    input_variables=["industry", "scenario", "mitre"],
    template=CTI_INDUSTRY_PROMPT
)

red_industry_prompt = PromptTemplate(
    input_variables=["industry", "scenario", "mitre"],
    template=RED_INDUSTRY_PROMPT
)

# ==========================
# CHAIN BUILDERS (LAZY LOADED)
# ==========================

_cti_rag_chain = None
_red_rag_chain = None
_cti_scenario_chain = None
_red_scenario_chain = None
_cti_industry_chain = None
_red_industry_chain = None

def get_cti_rag_chain():
    global _cti_rag_chain
    if _cti_rag_chain is None:
        _cti_rag_chain = cti_prompt | get_cti_llm()
    return _cti_rag_chain

def get_red_rag_chain():
    global _red_rag_chain
    if _red_rag_chain is None:
        _red_rag_chain = red_prompt | get_red_llm()
    return _red_rag_chain

def get_cti_scenario_chain():
    global _cti_scenario_chain
    if _cti_scenario_chain is None:
        _cti_scenario_chain = cti_scenario_prompt | get_cti_llm()
    return _cti_scenario_chain

def get_red_scenario_chain():
    global _red_scenario_chain
    if _red_scenario_chain is None:
        _red_scenario_chain = red_scenario_prompt | get_red_llm()
    return _red_scenario_chain

def get_cti_industry_chain():
    global _cti_industry_chain
    if _cti_industry_chain is None:
        _cti_industry_chain = cti_industry_prompt | get_cti_llm()
    return _cti_industry_chain

def get_red_industry_chain():
    global _red_industry_chain
    if _red_industry_chain is None:
        _red_industry_chain = red_industry_prompt | get_red_llm()
    return _red_industry_chain

# ==========================
# EXPORTED CHAINS (use get_ functions)
# ==========================

cti_rag_chain = get_cti_rag_chain
red_rag_chain = get_red_rag_chain
cti_scenario_chain = get_cti_scenario_chain
red_scenario_chain = get_red_scenario_chain
cti_industry_chain = get_cti_industry_chain
red_industry_chain = get_red_industry_chain

__all__ = [
    "get_cti_rag_chain",
    "get_red_rag_chain",
    "get_cti_scenario_chain",
    "get_red_scenario_chain",
    "get_cti_industry_chain",
    "get_red_industry_chain",
]
