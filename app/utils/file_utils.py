import os
from typing import List
import uuid
from fastapi import UploadFile

async def save_images(files: List[UploadFile], folder: str = "app/static/images") -> List[str]:
    os.makedirs(folder, exist_ok=True)
    paths = []
    for file in files:
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(folder, unique_name)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        # caminho relativo para guardar no banco
        relative_path = f"static/images/{unique_name}"
        paths.append(relative_path)
    return paths
