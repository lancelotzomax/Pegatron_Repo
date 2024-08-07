from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import logging # for more logging info
import uvicorn
import os

# Directory where files will be saved
UPLOAD_DIRECTORY = "C:/Users/user/Pegatron/Pegatron_Repo/fastapi-docker/app/img"

# Create the FastAPI Instance 
app = FastAPI(title="Fast API",
              description="API for Image Upload")

LOG = logging.getLogger(__name__)
LOG.info("API is starting up")
LOG.info(uvicorn.Config.asgi_version)

# router = APIRouter

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/image/{item_id}")
async def read_item_id(item_id: int):
    return {"item_id": item_id}

@app.get("/item_name")
async def read_item_name(item_name: str):
    return {"item_name": item_name}


@app.post("/image/{item_id}")
async def upload_image(item_id: int, item_name: str, file: UploadFile = File(...)):
    try:
        # Ensure the directory exists
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)

        # Read the file contents
        contents = await file.read()
        
        # Construct a file path
        file_path = os.path.join(UPLOAD_DIRECTORY, f"{item_id}_{item_name}.jpg")

        # Write the file to the specified path
        with open(file_path, 'wb') as f:
            f.write(contents)

    except Exception as e:
        return {"message": f"There was an error uploading the file: {str(e)}"}
    
    finally:
        await file.close()

    return {"message": f"Successfully uploaded {item_name}"}


@app.get("/image/{item_id}")
def read_image(item_id: int, item_name: str):
    # Construct the file path based on item_id
    file_path = os.path.join(UPLOAD_DIRECTORY, f"{item_id}_{item_name}.jpg")
    
    #Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # Return the file as a FileResponse
    return FileResponse(file_path, media_type="image/jpeg")


@app.put("/image/{item_id}")
def rename_image(item_id: int,  current_filename: str, new_filename: str):
    # Construct the current file path using item_id
    current_file_path = os.path.join(UPLOAD_DIRECTORY, f"{item_id}_{current_filename}.jpg")
    
    # Construct the new file path using the new filename
    new_file_path = os.path.join(UPLOAD_DIRECTORY, f"{item_id}_{new_filename}.jpg")

    # Check if the current file exists
    if not os.path.exists(current_file_path):
        raise HTTPException(status_code=404, detail="Current file not found")

    # Check if the new file name already exists
    if os.path.exists(new_file_path):
        raise HTTPException(status_code=400, detail="New file name already exists")

    # Rename the file
    try:
        os.rename(current_file_path, new_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error renaming file: {str(e)}")

    return {"message": f"Successfully renamed {item_id}_{current_filename}.jpg to {item_id}_{new_filename}.jpg"}


@app.delete("/image/{item_id}")
def delete_image(item_id: int):
    # Find the file with the specified item_id
    file_path = None
    for filename in os.listdir(UPLOAD_DIRECTORY):
        if filename.startswith(f"{item_id}_"):
            file_path = os.path.join(UPLOAD_DIRECTORY, filename)
            break

    # Check if the file exists
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # Delete the file
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

    return {"message": f"Successfully deleted file of item_id {item_id}"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)