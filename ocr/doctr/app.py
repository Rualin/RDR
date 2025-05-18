import os
from enum import Enum

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from doctr.io import DocumentFile

from api_source import gigachat_api
from api_source import init_doctr_predictor


load_dotenv()
giga_api = gigachat_api()
ocr_predictor = init_doctr_predictor(os.getenv("DET_ARCH"), os.getenv("RECO_ARCH"))


class OCRResult(BaseModel):
    text: str


class Confirmation(BaseModel):
    message: str


class ModelType(str, Enum):
    det = "det"
    reco = "reco"


app = FastAPI()


@app.post("/predict/", status_code=201)
async def upload_file(file: UploadFile) -> OCRResult:
    if not file:
        raise HTTPException(400, "No file sent")

    content = await file.read()

    if file.content_type.endswith("pdf"):
        doc = DocumentFile.from_pdf(content)
    else:
        doc = DocumentFile.from_images(content)

    recognized_text = ocr_predictor(doc).render()
    with open("recognized.txt", "wt") as output_file_for_ocr:
        output_file_for_ocr.write(recognized_text)
    with open("recognized.txt", "rb") as recognized_file_binary:
        giga_api.upload_file(recognized_file_binary)

    response = giga_api.request()
    giga_api.delete_file()

    return OCRResult(text=response.choices[0].message.content)


@app.post("/update_weights/{model_type}", status_code=201)
async def update_weights(model_type: ModelType, new_weights: UploadFile) -> Confirmation:
    if not new_weights:
        raise HTTPException(400, "No file sent")

    if not new_weights.filename.endswith((".pth", ".pt")):
        raise HTTPException(400, "Unsupported file type. It must be '.pth' or '.pt'")
    weights_filename = f"weights/{model_type.value}.pt"

    with open(weights_filename, "wb") as weights:
        content = await new_weights.read()
        weights.write(content)

    return Confirmation(message=f"{new_weights.filename} saved to {weights_filename}")
