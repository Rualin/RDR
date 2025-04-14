from fastapi import FastAPI, UploadFile, HTTPException
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


predictor = ocr_predictor()

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    if not file:
        raise HTTPException(400, "No file sent")
    image = await file.read()
    doc = DocumentFile.from_images([image])
    result = predictor(doc)
    return {"result": result.render()}
