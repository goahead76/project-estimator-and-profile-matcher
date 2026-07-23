# =====================================================================
# app/routers/estimator.py - Router with PDF & Profile Matcher Pipelines
# =====================================================================

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from app.services import parser, matcher  # <-- ADDED matcher IMPORT HERE
import traceback

router = APIRouter()

@router.post("/filtered-data")
async def parse_n_filter_file(
    file: UploadFile = File(...),
    keywords: str = Form(default="")
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files can be readable")
    
    try:
        # 1. Run your existing parser pipeline to extract sentences & track unique matching keywords
        result_data = await parser.extract_and_filter_pdf(file, keywords)

        # 2. Extract clean list of unique keywords found across the document body text
        # (Make sure you added the "all_matched_keywords" key to parser.py as shown earlier!)
        extracted_pdf_keywords = result_data.get("all_matched_keywords", [])

        # 3. Trigger your new developer profile matching pipeline
        # Points directly to the location of your Kaggle CSV database pool 
        csv_dataset_path = "static/csv/dev40.csv" 
        matching_payload = matcher.match_developers_and_visualize(extracted_pdf_keywords, csv_dataset_path)

        # 4. Append matching analytics and the 5 new graph data streams directly into payload mapping 
        result_data["matching_analytics"] = matching_payload
        
        return result_data

    except Exception as e:
        print("BACKEND ERROR EXTRACTION LOGS:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
