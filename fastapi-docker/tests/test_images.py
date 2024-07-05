import pytest
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

# Directory where files will be saved
UPLOAD_DIRECTORY = "C:/Users/user/Pegatron/Pegatron_Repo/fastapi-docker/app/img"

client = TestClient(app)

@app.get("/image/{item_id}")
async def read_item_id(item_id: int):
    return {"item_id": item_id}

@app.get("/item_name")
async def read_item_name(item_name: str):
    return {"item_name": item_name}


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

# ensure that images is successfully uploaded 
def test_upload_image(item_id: int, item_name: str):
    # item_id = item_id
    # item_name = item_name
    file_path = UPLOAD_DIRECTORY+f'/{item_id}_{item_name}.jpg'

    with open(file_path, "rb") as f:
        response = client.post(
            f"/image/{item_id}?item_name={item_name}",
            # data={"item_name": item_name},
            files = {"file": (item_name, f, "image/jpeg")}
        )
    
        assert response.status_code == 200
        assert response.json() == {"message": f"Successfully uploaded {item_name}"}

# # Ensure that images is successfully read 
def test_read_image():
    item_id = 1
    item_name = "test_image"
    file_path = UPLOAD_DIRECTORY+f'/{item_id}_{item_name}.jpg'

    # Verify the file exists
    assert os.path.exists(file_path)

    with open(file_path, "rb") as f:
        response = client.get(
            f"/image/{item_id}?item_name={item_name}",
        )
    
    assert response.status_code == 200
    # assert response.json() == {"message": f"Successfully uploaded {item_name}"}

# # Ensure that image's name has been successfully modified
def test_rename_image():
    item_id = 1
    current_filename = "test_image"
    new_filename = "renamed_image"
    file_path = UPLOAD_DIRECTORY+f'/{item_id}_{current_filename}.jpg'
    new_file_path = UPLOAD_DIRECTORY+f'/{item_id}_{new_filename}.jpg'

    # Verify the file exists
    assert os.path.exists(file_path)
   
   # Perform the put request
    response = client.put(
        f"/image/{item_id}?current_filename={current_filename}&new_filename={new_filename}",
        json={"current_filename": current_filename, "new_filename": new_filename}
    )

    # Check the response
    assert response.status_code == 200
    # assert response.json() == {"message": f"Successfully deleted file of item_id {item_id}"}

    # Verify the new file exists
    assert os.path.exists(new_file_path)

    # # Verify the old file no longer exists
    # assert not os.path.exists(file_path)
    
# Ensure that images has been successfully deleted 
def test_delete_image():
    item_id = 1
    item_name = "renamed_image"
    file_path = UPLOAD_DIRECTORY+f'/{item_id}_{item_name}.jpg'

    # Verify the file exists
    assert os.path.exists(file_path)

    # Perform the delete request
    response = client.delete(f"/image/{item_id}")

    # Check the response
    assert response.status_code == 200
    assert response.json() == {"message": f"Successfully deleted file of item_id {item_id}"}

    # # Verify the file is deleted
    # assert not os.path.exists(file_path)

def test_delete_nonexistent_image():
    item_id = 999

    # Perform the delete request for a nonexistent image
    response = client.delete(f"/image/{item_id}")

    # Check the response
    assert response.status_code == 404
    assert response.json() == {"detail": "Image not found"}

# # Example usage in your application
# if __name__ == "__main__":
#     item_id = fetch_item_id()
#     item_name = fetch_item_name()
# print(item_id)
# print(item_name)