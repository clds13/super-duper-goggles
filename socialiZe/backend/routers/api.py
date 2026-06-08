import io
import json
import mimetypes
import os
import shutil
import tempfile
from typing import Dict, List

import matplotlib.pyplot as plt
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

router = APIRouter()


@router.get(
        "/ping",
        name="Ping",
        summary="Ping the server to check if it is running.", 
        response_description="Pong!",
        response_model=dict)
async def ping():
    return {"message": "pong"}


@router.post(
        "/echo",
        name="Echo",
        summary="Echo the data back to the client.",
        response_description="The data that was sent to the server.",
        response_model=dict,
        openapi_extra={
            "example": {
                "data": {
                    "foo": "bar"
                }
            }
        })
async def echo(data):
    return data


@router.post(
    "/plot",
    name="Plot",
    summary="Plot the given data.",
)
async def plot_data(data: List[Dict[str, float]]):

    print("Plotting data")

    plt.ioff()  # Turn off interactive mode to prevent plot display

    x_values = [data[i]['x'] for i in range(len(data))]
    y_values = [data[i]['y'] for i in range(len(data))]
    timestamps = [data[i]['timestamp'] for i in range(len(data))]

    fig, ax = plt.subplots()
    ax.plot(x_values, y_values)

    # Save the plot to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        plot_filepath = temp_file.name
        plt.savefig(plot_filepath, format='png')

    # Return the plot image as a response
    with open(plot_filepath, "rb") as file:
        plot_data = file.read()

    return StreamingResponse(io.BytesIO(plot_data), media_type="image/png")


@router.get("/download/{filename}")
async def download_video(filename: str):
    print("Attempting to download file:", filename)
    file_path = os.path.join('recordings', filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print("Attempting to upload file")

    # Check if the file is a video
    if mimetypes.guess_type(file.filename)[0].startswith('video'):
        with open(f'uploads/{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return the filename and the file size
        return {"filepath": f"/uploads/{file.filename}", "filesize": os.path.getsize(f'uploads/{file.filename}'), "raw_filename": file.filename}
    
    # Check if the file is a .csv
    elif file.filename.endswith('.csv'):
        with open(f'trajectories/{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get how many lines are in the file
        num_lines = 0
        with open(f'trajectories/{file.filename}', 'r') as buffer:
            lines = buffer.readlines()
            num_lines = len(lines)
        
        return {"filepath": f"/trajectories/{file.filename}", "filesize": os.path.getsize(f'trajectories/{file.filename}'), "raw_filename": file.filename, "num_lines": num_lines}

    # If the file is neither a video nor a .csv, return an error
    return {"error": "Invalid file format"}


class DataModel(BaseModel):
    x: float
    y: float
    angle: float
    timestamp: float

class LogData(BaseModel):
    path: str = Field(..., example="/home/user/Projects/ProjectName")
    filename: str = Field(..., example="test.json")
    data: List[DataModel]


@router.post("/log/")
async def log_data(log_data: LogData):
    print("Logging data to file:", log_data.filename)
    print("Directory:", log_data.path)

    # Get the user's documents directory
    documents_dir = os.path.join(os.path.expanduser('~'), 'Documents')

    # Get the directory to save the file in
    save_dir = log_data.path.split('/')[:-1]
    save_dir = '/'.join(save_dir)

    # Check if log_data.path is a valid directory in the user's documents directory
    if not os.path.exists(os.path.join(documents_dir, save_dir)):
        # Create the directory
        os.makedirs(os.path.join(documents_dir, save_dir))

    # Check if the file is a .json
    if log_data.filename.endswith('.json'):
        # Write the data to a JSON file
        with open(os.path.join(documents_dir, save_dir, log_data.filename), 'w') as buffer:
            json.dump(log_data.model_dump(include={'data'}), buffer, indent=4)

        return {"success": True}
    
    # If the file is not a .json, return an error
    return {"error": "Invalid file format"}
