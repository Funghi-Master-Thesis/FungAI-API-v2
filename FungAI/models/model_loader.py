print("Starting FastAPI application...")

import PIL
import numpy as np
import pandas as pd
import torch
import sys
import os
import cv2
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, Response
from PIL import Image
import io
import torchvision.transforms as transforms
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from torch.profiler import profile, record_function, ProfilerActivity
from utils.utils import build_annotation_dataframe, check_annot_dataframe, transform_bilinear, transform_bilinear_validate, infer, infer_single_image, calculate_model_performance, generate_fn_cost_matrix, generate_fp_cost_matrix, get_current_timestamp
from models.models import get_model
# Jinja2 templates setup
templates = Jinja2Templates(directory="templates")

print("Imports done")

sys.path.append('/zhome/ac/d/174101/thesis/src')
import torchvision.datasets as datasets


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device set")



base_path = Path(__file__).resolve().parent
model_name = "DataSetLast2Days_levit_128s_model.pth" #specify a model
model_path = Path(base_path) / "DataSetLast2Days" / f"{model_name}" 

train_data = base_path / "DataSetLast2Days/train.csv"
test_data = base_path / 'DataSetLast2Days/test.csv'
val_data = base_path / "DataSetLast2Days/val.csv"
train_df = pd.read_csv(train_data)
test_df = pd.read_csv(test_data)
val_df = pd.read_csv(val_data)
all_df = pd.concat([train_df, test_df, val_df], ignore_index=True)  




all_class_names = list(all_df['class_name'].unique())
all_num_classes = len(all_class_names)

print("Datasets loaded")
all_model = get_model("levit_128s", all_num_classes)
all_model = all_model.to(device)
all_model.load_state_dict(torch.load(model_path, map_location=device))

base_path = Path(__file__).resolve().parent
model_name = "DataSetCutLast2Days_vit_b_16_model.pth" #specify a model
model_path = Path(base_path) / 'DataSetCutLast2Days/' / f"{model_name}" 

train_data = base_path / "DataSetCutLast2Days/train.csv"
train_data = base_path / 'DataSetCutLast2Days/test.csv'
train_data = base_path / "DataSetCutLast2Days/val.csv"
train_df = pd.read_csv(train_data)
test_df = pd.read_csv(test_data)
val_df = pd.read_csv(val_data)
all_df = pd.concat([train_df, test_df, val_df], ignore_index=True)  




six_class_names = list(all_df['class_name'].unique())
six_num_classes = len(six_class_names)

print("Datasets loaded")
six_model = get_model("vit_b_16", six_num_classes)
six_model = six_model.to(device)
six_model.load_state_dict(torch.load(model_path, map_location=device))


# Prediction endpoint
def predict_image(image_path, ismasked):
    all_model.eval()
    image_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224),
                        interpolation=PIL.Image.BILINEAR),


    ])

    
    image = cv2.imread(image_path)  # Read image using cv2
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (400,600))
    
    if(not ismasked):
        mask = np.zeros((600, 400), np.uint8)
        xrange = [100, 300, 500]
    
        for i in range(3):
            cv2.circle(mask, (100, xrange[i]), 75, (255, 255, 255), -1)
            cv2.circle(mask, (300, xrange[i]), 75, (255, 255, 255), -1)
        image = cv2.bitwise_and(image, image, mask=mask)
        
    image_transformed = image_transform(image)
    print("test1")
    # Display the transformed image (optional)
    image_transformed_sq = torch.unsqueeze(image_transformed, dim=0)
    print("test1323")
    with torch.no_grad():
        image_transformed_sq = image_transformed_sq.to(device)
        outputs = all_model(image_transformed_sq)
        print("test22")
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        # probabilities = torch.sigmoid(outputs)
        print("test223")   
        top_probabilities, top_indices = torch.topk(probabilities, 5)
    print("test2")
    
    # Inference
    # Convert to numpy and make the output more readable
    top_probabilities = top_probabilities.cpu().numpy().flatten() * 100  # Convert to percentage
    top_indices = top_indices.cpu().numpy().flatten()
    print(top_probabilities)
    predictions = []
    print("test3")
    
    for i in range(len(top_probabilities)):
        predictions.append({
            "class_name": all_class_names[top_indices[i]],
            "probability": top_probabilities[i].item()
    })
    # Print the results

    # Render predictions.html template with predictions
    return predictions

def apply_circular_mask(image, scale_factor=0.675):
    """Apply a circular mask to the image with an adjustable scale factor."""
    height, width = image.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    center = (width // 2, height // 2)
    radius = int(min(center[0], center[1], width - center[0], height - center[1]) * scale_factor)
    cv2.circle(mask, center, radius, (255, 255, 255), -1)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    return masked_image

def cut_to_boundingbox(image):
    """Cut the image to the bounding box of the circle."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    x, y, w, h = cv2.boundingRect(thresh)
    image = image[y:y+h, x:x+w]
    return image

def predict_single_image(image_path, ismasked):
    six_model.eval()
    image_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224),
                        interpolation=PIL.Image.BILINEAR),


    # transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])

    
    image = cv2.imread(image_path)  # Read image using cv2
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if(not ismasked):
        image = apply_circular_mask(image)
        image = cut_to_boundingbox(image)
    image_transformed = image_transform(image)
    print("test1")
    # Display the transformed image (optional)
    image_transformed_sq = torch.unsqueeze(image_transformed, dim=0)
    print("test1323")
    with torch.no_grad():
        image_transformed_sq = image_transformed_sq.to(device)
        outputs = six_model(image_transformed_sq)
        print("test22")
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        # probabilities = torch.sigmoid(outputs)
        print("test223")   
        top_probabilities, top_indices = torch.topk(probabilities, 5)
    print("test2")
    
    # Inference
    # Convert to numpy and make the output more readable
    top_probabilities = top_probabilities.cpu().numpy().flatten() * 100  # Convert to percentage
    top_indices = top_indices.cpu().numpy().flatten()
    print(top_probabilities)
    predictions = []
    print("test3")
    
    for i in range(len(top_probabilities)):
        predictions.append({
            "class_name": six_class_names[top_indices[i]],
            "probability": top_probabilities[i].item()
    })
    # Print the results

    # Render predictions.html template with predictions
    return predictions
    


