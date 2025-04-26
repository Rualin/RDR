from os.path import isfile
from enum import Enum

from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from doctr.io import DocumentFile
from doctr.models import ocr_predictor, crnn_vgg16_bn, fast_base
from doctr.datasets import VOCABS
import torch

vocab = VOCABS['russian'] + VOCABS['latin'] + '№'

det_weights = 'weights/det.pth'
if isfile(det_weights):
    det_model = fast_base(pretrained=False, pretrained_backbone=False)
    det_params = torch.load(det_weights, map_location="cpu")
    det_model.load_state_dict(det_params)
else:
    det_model = 'fast_base'

reco_weights = 'weights/reco.pth'
if isfile(reco_weights):
    reco_model = crnn_vgg16_bn(pretrained=False, pretrained_backbone=False, vocab=vocab)
    reco_param = torch.load(reco_weights, map_location="cpu")
    reco_model.load_state_dict(reco_param)
else:
    reco_model = 'crnn_vgg16_bn'

predictor = ocr_predictor(det_arch=det_model,
                          reco_arch=reco_model,
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
        raise HTTPException(400, "Unsupported file type. It must be '.pth'")
    weights_filename = f'weights/{model_type}.pth'

    with open(weights_filename, 'wb') as weights:
        content = await new_weights.read()
        weights.write(content)

    return Confirmation(message=f'{new_weights.filename} saved to {weights_filename}')
