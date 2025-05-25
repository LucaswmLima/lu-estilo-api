from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router_images = APIRouter(prefix="/images", tags=["images"])

IMAGE_FOLDER = "app/static/images"

@router_images.get("/{image_name}")
def get_image(image_name: str):
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return FileResponse(image_path)
