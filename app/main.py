from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from utils import classify_image
from labels import labels
from pydantic import BaseModel

app = FastAPI(
    title='Test Task App'
)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=[
            'HEAD',
            'OPTIONS',
            'GET',
            'POST',
            'DELETE',
            'PATCH',
        ],
        allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                       "Authorization", ],
        allow_credentials=True,
    )

class ImageForm(BaseModel):
    file: UploadFile = File(...)


@app.post('/')
async def post(request: Request, file: UploadFile = File(...)):

    if not file:
        # If the image is not provided, raise an HTTPException with a 400 Bad Request status code
        raise HTTPException(status_code=400, detail="Image not provided")

    try:
        image = Image.open(file.file)
    except Exception as e:
        # If there is an error opening the image, raise an HTTPException with a 422 Unprocessable Entity status code
        raise HTTPException(status_code=422, detail="Error opening the image")

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
