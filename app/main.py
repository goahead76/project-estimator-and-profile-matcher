from fastapi import FastAPI, File, UploadFile, HTTPException, Form 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import spacy, io , pypdf
from typing import List, Dict
from fastapi.responses import FileResponse
import traceback  # Helps print structural debug logs
import urllib.request, os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def read_root():
    return FileResponse("index.html")

nlp = spacy.load("en_core_web_sm", disable=["ner","textcat"])

MANDATORY_CATEGORIES = {
    "Tech Stack": ["sql", "analytics", "data science", "web development", "ui/ux", "api", "database", "cloud", "integration"],
    "Timeline": ["timeline", "deadline", "milestone", "phase", "duration", "weeks", "months", "schedule", "go-live"],
    "Team Size": ["team", "engineer", "developer", "resource", "designer", "architect", "headcount", "fte"],
    "Constraints": ["must", "shall", "required", "sla", "compliance", "uptime", "budget"]
}

@app.post("/filtered-data")
async def parse_n_filter_file(
    file: UploadFile = File(...),
    keywords: str = Form(default="")
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files can be readable")
    
    try:
        # Read the file payload safely using the verified 'file' reference
        pdf_bytes = await file.read()
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = pypdf.PdfReader(pdf_stream)
        
        extracted_text_pieces = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text_pieces.append(text.replace("\n", " ").strip())
        
        combined_text = " ".join(extracted_text_pieces)

        runtime_categories = {k: v.copy() for k, v in MANDATORY_CATEGORIES.items()}
        if keywords and keywords.strip():
            custom_kws = [kw.lower().strip() for kw in keywords.split(",") if kw.strip()]
            runtime_categories["Custom Searches"] = custom_kws

        doc_nlp = nlp(combined_text)
        
        filtered_sentences = []
        chart_metrics = {cat: 0 for cat in runtime_categories.keys()}
        keyword_density = {}

        for sent in doc_nlp.sents:
            sentence_str = sent.text.strip()
            sentence_lower = sentence_str.lower()
            
            matched_kws = []
            sentence_categories = []
            
            for category, kw_list in runtime_categories.items():
                found_kws = [kw for kw in kw_list if kw in sentence_lower]
                if found_kws:
                    matched_kws.extend(found_kws)
                    sentence_categories.append(category)
                    chart_metrics[category] += 1
                    
                    for kw in found_kws:
                        keyword_density[kw] = keyword_density.get(kw, 0) + 1
            
            if matched_kws:
                filtered_sentences.append({
                    "sentence": sentence_str,
                    "matched_keywords": list(set(matched_kws)),
                    "categories": list(set(sentence_categories))
                })

        return {
            "status": "success",
            "filename": file.filename,
            "total_matches_found": len(filtered_sentences),
            "chart_data": {
                "categories": list(chart_metrics.keys()),
                "counts": list(chart_metrics.values())
            },
            "keyword_density": {
                "labels": [k.upper() for k in keyword_density.keys()],
                "values": list(keyword_density.values())
            },
            "results": filtered_sentences
        }

    except Exception as e:
        # Crucial: Prints the exact breaking file line to your VS Code terminal
        print("❌ BACKEND ERROR EXTRACTION LOGS:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
# ==========================================
# TEMPORARY DOWNLOADER CODE (Delete after running)
# ==========================================
try:
    static_file_path = os.path.join("static", "chart.umd.js")
    os.makedirs("static", exist_ok=True)
    
    print("⏳ Downloading actual JavaScript file from unpkg registry...")
    req = urllib.request.Request(
        'https://unpkg.com', 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    # This downloads the true JavaScript source array code data
    raw_js_bytes = urllib.request.urlopen(req).read()
    
    with open(static_file_path, "wb") as f:
        f.write(raw_js_bytes)
        
    print("🎉 SUCCESS: The real library file has been written into static/chart.umd.js!")
except Exception as e:
    print(f"❌ Startup Downloader Failed: {e}")