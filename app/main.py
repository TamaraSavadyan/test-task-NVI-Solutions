from fastapi import FastAPI, UploadFile, File
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
from PIL import Image

app = FastAPI(
    title='Test Task App'
)
model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
model.eval()


def classify_image(image):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = preprocess(image)
    image = image.unsqueeze(0)
    output = model(image)
    _, predicted_idx = output.max(1)
    return predicted_idx.item()


@app.post('/')
async def classify(file: UploadFile = File(...)):
    image = Image.open(file.file)
    width, height = image.size
    class_idx = classify_image(image)
    class_label = 'Unknown'
    # Здесь нужно добавить код для определения метки класса по индексу, используя вашу библиотеку меток классов.
    # Можно использовать стандартный набор меток классов, доступных в torchvision.
    # Например, class_label = torchvision.models.resnet.IMAGENET_CLASSES[class_idx]
    return {'width': width, 'height': height, 'class_label': class_label}


@app.get('/')
async def say_hello():
    return {'Hello theere!'}