from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, RedirectResponse

import starlette.status as status
from pydantic import BaseModel

import logging # for more logging info
import uvicorn
import os

# Directory where files will be saved
UPLOAD_DIRECTORY = "./img/"

# Ensure the directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = FastAPI(title="Fast API",
              description="API for Image Upload")

LOG = logging.getLogger(__name__)
LOG.info("API")
LOG.info(uvicorn.Config.asgi_version)

# router = APIRouter

class Item(BaseModel):
    name:str
    item_id:int
    
@app.get("/")
def read_root():
    # redirect_url = request.url_for('signin')+ '?x-error=Invalid+credentials'
    #     return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND, headers={"x-error": "Invalid credentials"})
    return {"Hello": "World"}

@app.post("/image/{item_id}")
async def upload_image(item_id: int, file: UploadFile = File(...)):
    try:
        # Read the file contents
        contents = file.file.read()

        # Construct a file path
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

        # Write the file to the specified path
        with open(file_path, 'wb') as f:
            f.write(contents)

    except Exception as e:
        return {"message": f"There was an error uploading the file: {str(e)}"}
    
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

# @app.post('/files')
# def get_file(file: bytes = File(...)):
#     content = file.decode('utf-8')
#     lines = content.split('\n')
#     return {"content": lines}

@app.get("/image/{item_id}")
def read_image(item_name: str, item_id: int, q: Union[str, None] = None):
    return {"item_name": item_name, "item_id": item_id, "q": q}

@app.put("/image/{item_id}")
def update_item(item_id: int, updated_item: Item):
    return {"item_id": item_id, "updated_item": updated_item}

@app.delete("/image/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item{item_id} has been deleted"}


