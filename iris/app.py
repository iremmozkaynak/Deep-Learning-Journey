from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator
import torch
import torch.nn as nn
import logging

# Logging ayarla
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Iris Flower Classifier", version="1.0.0")

# Templates
templates = Jinja2Templates(directory="templates")

# Iris sınıf isimleri
CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]


# Model mimarisi (eğitimde kullanılan ile aynı)
class IrisClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 3)
        )

    def forward(self, x):
        return self.linear_layer_stack(x)


# Modeli yükle
try:
    model = IrisClassifier()
    model.load_state_dict(torch.load("models/iris_classification_model.pth", map_location=torch.device("cpu")))
    model.eval()
    logger.info("Model başarıyla yüklendi.")
except FileNotFoundError:
    logger.error("Model dosyası bulunamadı: models/iris_classification_model.pth")
    model = None
except Exception as e:
    logger.error(f"Model yüklenirken hata oluştu: {e}")
    model = None


class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    @field_validator("sepal_length", "sepal_width", "petal_length", "petal_width")
    @classmethod
    def must_be_positive(cls, v, info):
        if v <= 0:
            raise ValueError(f"{info.field_name} pozitif bir sayı olmalıdır.")
        return v


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/predict")
async def predict(features: IrisFeatures):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model şu anda kullanılamıyor. Lütfen daha sonra tekrar deneyin."
        )

    try:
        # Giriş verisini tensor'a çevir
        input_tensor = torch.tensor(
            [[features.sepal_length, features.sepal_width,
              features.petal_length, features.petal_width]],
            dtype=torch.float32
        )

        # Tahmin yap
        with torch.inference_mode():
            logits = model(input_tensor)
            probabilities = torch.softmax(logits, dim=1)
            predicted_class_idx = probabilities.argmax(dim=1).item()
            confidence = probabilities[0][predicted_class_idx].item() * 100

        predicted_class = CLASS_NAMES[predicted_class_idx]

        # Tüm sınıfların olasılıklarını döndür
        all_probabilities = {
            CLASS_NAMES[i]: round(probabilities[0][i].item() * 100, 2)
            for i in range(3)
        }

        logger.info(f"Tahmin: {predicted_class} ({confidence:.1f}%)")

        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 2),
            "probabilities": all_probabilities,
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Tahmin hatası: {e}")
        raise HTTPException(status_code=500, detail="Tahmin sırasında bir hata oluştu.")
