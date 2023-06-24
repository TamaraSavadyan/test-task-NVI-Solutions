import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision.models import resnet50
from torchvision import models

model = models.resnet50(pretrained=True)
model.eval()

def classify_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_batch = input_batch.to(device)

    with torch.no_grad():
        output = model(input_batch)

    _, predicted_idx = torch.max(output, 1)
    predicted_label = predicted_idx.item()

    return predicted_label
