from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from PIL import Image
from utils import classify_image
from labels import labels
from pydantic import BaseModel

app = FastAPI(
    title='Test Task App'
)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


class ImageForm(BaseModel):
    file: UploadFile = File(...)


@app.post('/')
async def post(request: Request, file: UploadFile = File(...)):

    image = Image.open(file.file)

    width, height = image.size
    class_idx = classify_image(image)
    class_label = labels[class_idx]

    response = {
        'request': request,
        'width': width,
        'height': height,
        'class_label': class_label
    }

    return templates.TemplateResponse('index.html', response)


@app.get('/')
async def get(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
