from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
from utils import classify_image

app = FastAPI(
    title='Test Task App'
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post('/')
async def post(file: UploadFile = File(...)):
    image = Image.open(file.file)
    width, height = image.size
    class_idx = classify_image(image)
    class_label = 'Unknown'
    # Здесь нужно добавить код для определения метки класса по индексу, используя вашу библиотеку меток классов.
    # Можно использовать стандартный набор меток классов, доступных в torchvision.
    # Например, class_label = torchvision.models.resnet.IMAGENET_CLASSES[class_idx]
    return {'width': width, 'height': height, 'class_label': class_label}


@app.get('/')
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})