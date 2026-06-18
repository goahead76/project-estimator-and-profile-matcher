from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pypdf 
import io
from fastapi.responses import FileResponse

app = FastAPI()

#Enable CORS for frontend communicatio
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def read_root():
    # This searches for index.html in your root project folder and returns it
    return FileResponse("index.html")

#handling the binary file comming from frontend while upload the file
@app.post("/filtered-data")
async def parse_n_filter_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code = 400, detail="Only PDF files can be readable")
    
    try:
        pdf_bytes = await file.read()
        pdf_stream = io.BytesIO(pdf_bytes)  #converts binary stream into in-memory file for pypdf
        pdf_reader = pypdf.PdfReader(pdf_stream)
        extracted_text = ""

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        # Define your filtering keyword
        search_keyword = "analytics" 
        
        filtered_lines = [
            line.strip() 
            for line in extracted_text.split("\n") 
            if search_keyword in line.lower() and line.strip()
        ]

        # --- TERMINAL PRINTS START HERE ---
        print("\n" + "="*50)
        print(f"📄 RECEIVED FILE: {file.filename}")
        print(f"🔍 FILTERED LINES CONTAINING '{search_keyword}':")
        print("="*50)
        
        if not filtered_lines:
            print("[No matching lines found in this PDF]")
        else:
            for index, line in enumerate(filtered_lines, start=1):
                print(f"{index}. {line}")
                
        print("="*50 + "\n")
        # --- TERMINAL PRINTS END HERE ---

        return {
            "status": "success",
            "message": f"Successfully parsed and printed {len(filtered_lines)} lines to the console."
        }

   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {str(e)}")

    

