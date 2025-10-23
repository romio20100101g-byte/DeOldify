from fastapi import FastAPI
from pydantic import BaseModel
from deoldify.visualize import get_image_colorizer
from PIL import Image
import requests
from io import BytesIO
import uuid
import os

app = FastAPI()
colorizer = get_image_colorizer(artistic=True)

class ImageRequest(BaseModel):
    image_url: str

@app.post("/colorize")
async def colorize_image(req: ImageRequest):
    response = requests.get(req.image_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    result = colorizer.get_transformed_image_from_upload(img, render_factor=35)

    filename = f"{uuid.uuid4().hex}.jpg"
    os.makedirs("static", exist_ok=True)
    result.save(f"static/{filename}")
    return {"status": "success", "url": f"/static/{filename}"}
