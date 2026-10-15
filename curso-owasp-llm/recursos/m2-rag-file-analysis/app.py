import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded (for debugging)
api_key_check = os.getenv("GROQ_API_KEY")
if api_key_check:
    print(f"[OK] GROQ_API_KEY loaded (length: {len(api_key_check)})")
else:
    print("[ERROR] WARNING: GROQ_API_KEY not found in environment!")

from utils.pdf_reader import extract_pdf_text
from chains import (
    get_cti_rag_chain,
    get_red_rag_chain,
    get_cti_scenario_chain,
    get_red_scenario_chain,
    get_cti_industry_chain,
    get_red_industry_chain
)
from mitre_map import (
    extract_mitre_techniques,
    infer_mitre_techniques,
    build_mitre_summary,
)

app = Flask(__name__, template_folder="templates", static_folder="static")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# session_id -> stored data
stored_reports = {}


# ==========================
# HOME
# ==========================
@app.route("/")
def index():
    return render_template("index.html")


# ==========================
# PDF INGESTION
# ==========================
@app.route("/upload", methods=["POST"])
def upload_pdf():
    try:
        file = request.files.get("pdf")
        if not file:
            return jsonify({"error": "No PDF uploaded"}), 400

        path = os.path.join(UPLOAD_DIR, file.filename)
        file.save(path)

        print(f"\n📄 PDF Upload:")
        print(f"  Filename: {file.filename}")
        print(f"  Path: {path}")

        text = extract_pdf_text(path)
        
        # Validate we have content
        if not text or len(text.strip()) < 50:
            error_msg = f"PDF appears to be empty or unreadable. Extracted {len(text)} characters."
            print(f"  ❌ {error_msg}")
            return jsonify({"error": error_msg}), 400
        
        session_id = file.filename
        
        print(f"  Extracted Text Length: {len(text)} chars")
        print(f"  Session ID: {session_id}")

        try:
            techniques = extract_mitre_techniques(text)
            if not techniques:
                techniques = infer_mitre_techniques(text)
        except Exception as e:
            print(f"  Error extracting MITRE techniques: {e}")
            techniques = []  # Continue with empty techniques on error

        mitre_summary = build_mitre_summary(techniques)
        
        print(f"  MITRE Techniques Found: {len(techniques)}")

        stored_reports[session_id] = {
            "text": text,
            "mitre": mitre_summary
        }
        
        print(f"  [OK] Report stored with session ID: {session_id}")
        print(f"  Text Preview: {text[:200]}...")

        try:
            from rag_store import build_vectorstore
            build_vectorstore(text, session_id)
        except Exception as e:
            print(f"  Warning: Could not build vectorstore: {e}")
            # Continue without vectorstore - the report is still stored

        return jsonify({
            "session_id": session_id,
            "mitre_techniques": mitre_summary,
            "message": "Report ingested successfully"
        })
    except Exception as e:
        print(f"Error during PDF upload: {e}")
        return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500


# ==========================
# ASK QUESTIONS (CTI / RED)
# ==========================
@app.route("/ask", methods=["POST"])
def ask():
    session_id = request.json.get("session_id")
    question = request.json.get("question")
    mode = request.json.get("mode", "cti").lower()  # cti | red

    print(f"\n📋 ASK Request:")
    print(f"  Session ID: {session_id}")
    print(f"  Mode: {mode}")
    print(f"  Question: {question}")
    print(f"  Stored Sessions: {list(stored_reports.keys())}")

    if session_id not in stored_reports:
        error_msg = f"Invalid session. Available sessions: {list(stored_reports.keys())}"
        print(f"  ❌ {error_msg}")
        return jsonify({"error": error_msg}), 400

    context = stored_reports[session_id]["text"]
    print(f"  Context Length: {len(context)} chars")
    print(f"  Context Preview: {context[:200]}...")

    if mode == "cti":
        print(f"  Using CTI Chain")
        response = get_cti_rag_chain().invoke({
            "context": context,
            "question": question
        })
    elif mode == "red":
        print(f"  Using RED Chain")
        response = get_red_rag_chain().invoke({
            "context": context,
            "question": question
        })
    else:
        return jsonify({"error": "Invalid mode"}), 400

    print(f"  ✅ Response received")
    return jsonify({
        "mode": mode,
        "answer": response.content
    })


# ==========================
# SCENARIO GENERATION (CTI / RED)
# ==========================
@app.route("/scenario", methods=["POST"])
def scenario():
    session_id = request.json.get("session_id")
    mode = request.json.get("mode", "red").lower()  # default RED

    if session_id not in stored_reports:
        return jsonify({"error": "Invalid session"}), 404

    mitre = stored_reports[session_id]["mitre"]
    
    # Format MITRE techniques for the prompt
    techniques_text = "\n".join([f"- {t['technique_id']}: {t['name']}" for t in mitre]) if mitre else "No techniques identified"

    if mode == "cti":
        scenario = get_cti_scenario_chain().invoke({
            "techniques": techniques_text
        })
    elif mode == "red":
        scenario = get_red_scenario_chain().invoke({
            "techniques": techniques_text
        })
    else:
        return jsonify({"error": "Invalid mode"}), 400

    return jsonify({
        "mode": mode,
        "scenario": scenario.content
    })


# ==========================
# INDUSTRY ENGAGEMENT (CTI / RED)
# ==========================
@app.route("/engagement", methods=["POST"])
def engagement():
    session_id = request.json.get("session_id")
    industry = request.json.get("industry")
    mode = request.json.get("mode", "red").lower()

    if session_id not in stored_reports:
        return jsonify({"error": "Invalid session"}), 404

    mitre = stored_reports[session_id]["mitre"]
    
    # Format MITRE techniques for the prompt
    techniques_text = "\n".join([f"- {t['technique_id']}: {t['name']}" for t in mitre]) if mitre else "No techniques identified"

    # Generate scenario first (mode-aware)
    if mode == "cti":
        scenario = get_cti_scenario_chain().invoke({
            "techniques": techniques_text
        }).content

        plan = get_cti_industry_chain().invoke({
            "industry": industry,
            "scenario": scenario,
            "mitre": techniques_text
        })

    elif mode == "red":
        scenario = get_red_scenario_chain().invoke({
            "techniques": techniques_text
        }).content

        plan = get_red_industry_chain().invoke({
            "industry": industry,
            "scenario": scenario,
            "mitre": techniques_text
        })

    else:
        return jsonify({"error": "Invalid mode"}), 400

    return jsonify({
        "mode": mode,
        "engagement_plan": plan.content
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
