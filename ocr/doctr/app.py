from os.path import isfile
from enum import Enum

from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


det_arch = 'weights/det.pth'
if not isfile(det_arch):
    det_arch = 'fast_base'

reco_arch = 'weights/reco.pth'
if not isfile(reco_arch):
    reco_arch = 'crnn_vgg16_bn'

predictor = ocr_predictor(det_arch=det_arch,
                          reco_arch=reco_arch,
                          pretrained=True,
                          assume_straight_pages=False
                          )


class OCRResult(BaseModel):
    text: str


class Confirmation(BaseModel):
    message: str


class ModelType(str, Enum):
    det = "det"
    reco = "reco"


app = FastAPI()


@app.post("/uploadfile/", status_code=201)
async def upload_file(file: UploadFile) -> OCRResult:
    if not file:
        raise HTTPException(400, "No file sent")

    content = await file.read()

    if file.filename.endswith('.pdf'):
        doc = DocumentFile.from_pdf(content)
    else:
        doc = DocumentFile.from_images(content)

    return OCRResult(text=predictor(doc).render())


@app.post("/update_weights/{model_type}", status_code=201)
async def update_weights(model_type: ModelType, new_weights: UploadFile) -> Confirmation:
    if not new_weights:
        raise HTTPException(400, "No file sent")

    if not new_weights.filename.endswith('.pth'):
        raise HTTPException(400, "Usupported file type. It must be '.pth'")
    weights_filename = f'weights/{model_type}.pth'

    with open(weights_filename, 'wb') as weights:
        content = await new_weights.read()
        weights.write(content)

    return Confirmation(message=f'{new_weights.filename} saved to {weights_filename}')
