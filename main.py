from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import img2pdf
import os
from datetime import datetime

app = FastAPI()

# CORS Middleware (necessário caso queira expor para outras origens futuramente)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique ["http://127.0.0.1:5500"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretório onde os arquivos temporários serão armazenados
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Diretório de templates HTML
templates = Jinja2Templates(directory="templates")

# Página principal do WebApp (interface para gerar PDF)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Página da landing comercial
@app.get("/landing", response_class=HTMLResponse)
async def show_landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

# Endpoint que converte imagens para PDF
@app.post("/convert/")
async def convert_images_to_pdf(files: list[UploadFile] = File(...)):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_path = f"{UPLOAD_DIR}/converted_{timestamp}.pdf"
    
    image_paths = []
    for file in files:
        file_path = f"{UPLOAD_DIR}/{timestamp}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        image_paths.append(file_path)
    
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))

    for img in image_paths:
        os.remove(img)
        
    return FileResponse(pdf_path, media_type="application/pdf", filename=os.path.basename(pdf_path))
