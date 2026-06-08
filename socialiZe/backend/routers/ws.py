import asyncio
import os
from datetime import datetime

import cv2
import numpy as np
from fastapi import APIRouter, WebSocket, Depends
from FrameLogger import AsyncFrameLogger
from PySpinManager import PySpinManager

router = APIRouter()

# Global variables
is_recording = False
video_writer = None
video_folder_path = "C:\\Users\\LinAdmin\\Documents\\Christine\\Videos\\"
frame_rate = 20  # Frame rate
high_res_frame_size = (1920, 1200)  # High-resolution size
start_time = None  # Start time of recording
duration = 0  # Duration of the recording
connection_active = False  # Flag to indicate WebSocket connection status
video_save_path = ""  # Path to save the video and CSV

manager = PySpinManager()

def get_camera_feed():
    global manager
    camera = manager.get_camera(0)

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Failed to capture frame")
                continue

            high_res_frame = cv2.resize(frame, high_res_frame_size)  # High-resolution frame for recording
            resized_frame = cv2.resize(frame, (960, 600))  # Resized frame for WebSocket transmission
            yield high_res_frame, resized_frame
    except Exception as e:
        print(f"An error occurred: {e}")

async def get_logger():
    # Instantiate the AsyncFrameLogger
    logger = AsyncFrameLogger(db_path='frame_log.db', batch_size=500)
    # Ensure the database is set up
    await logger._setup_db()
    return logger

@router.websocket("/camera-feed")
async def websocket_endpoint(websocket: WebSocket, logger: AsyncFrameLogger = Depends(get_logger)):
    global is_recording, video_writer, start_time, duration, connection_active, video_save_path

    await websocket.accept()
    camera_feed = get_camera_feed()
    connection_active = True

    async def send_camera_feed():
        global is_recording, video_writer, start_time, duration, connection_active, video_save_path
        frame_count = 0  # Count of frames recorded

        try:
            while True:
                high_res_frame, resized_frame = next(camera_feed)

                if is_recording:
                    if frame_count < frame_rate * duration:
                        # Capture the timestamp when the frame is processed
                        timestamp = datetime.now()
                        # Asynchronously log the frame with the captured timestamp
                        await logger.log_frame(frame_count, timestamp)

                        # Add frame number text
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        frame_text = f"Frame: {frame_count}"
                        text_size = cv2.getTextSize(frame_text, font, 1, 2)[0]
                        text_x = high_res_frame_size[0] - text_size[0] - 10
                        text_y = text_size[1] + 10
                        cv2.putText(high_res_frame, frame_text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

                        # Add timestamp text
                        timestamp_text = f"Timestamp: {timestamp}"
                        timestamp_text_size = cv2.getTextSize(timestamp_text, font, 0.8, 2)[0] 
                        text_y += timestamp_text_size[1] + 10  
                        left_offset = 50  # Adjust this value to control how far left
                        text_x = max(left_offset, text_x - timestamp_text_size[0])  # Ensure it doesn't go off-screen 
                        cv2.putText(high_res_frame, timestamp_text, (text_x, text_y), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

                        video_writer.write(high_res_frame)
                        frame_count += 1
                    else:
                        # Stop recording
                        is_recording = False
                        video_writer.release()
                        video_writer = None
                        print("Recording stopped")

                        await logger.flush()  # Ensure all logs are written before export

                        # After stopping, export logged data to CSV and clear the database
                        csv_filename = f"frame_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                        csv_path = os.path.join(video_save_path, csv_filename)
                        await logger.export_to_csv(csv_path)
                        await logger.clear_database()

                # Convert frame to JPEG for WebSocket transmission
                ret, jpeg_frame = cv2.imencode('.jpg', resized_frame)
                if ret:
                    await websocket.send_bytes(jpeg_frame.tobytes())

                await asyncio.sleep(0)
        except asyncio.CancelledError:
            print("Error - Connection closed...")
            await logger.flush()

    async def receive_messages():
        global is_recording, video_writer, start_time, duration, connection_active, video_save_path
        try:
            while True:
                message = await websocket.receive_json()
                print(message)
                command = message.get("command", "")
                if command == "start" and not is_recording:
                    is_recording = True
                    duration = int(message.get("duration", 0))
                    start_time = datetime.now()
                    destination = message.get("destination", video_folder_path)

                    # Determine the save path for the video
                    video_save_path, filename = setup_video_recording(destination, message)
                    full_video_path = os.path.join(video_save_path, filename)

                    video_writer = cv2.VideoWriter(full_video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, high_res_frame_size)
                    print("Recording started")

                elif command == "stop" and is_recording:
                    # Stop command logic can be added here if needed
                    pass
                else:
                    print("Skipping command. Invalid.")
        except asyncio.CancelledError:
            print("WebSocket closed.")

    sender_task = asyncio.create_task(send_camera_feed())
    receiver_task = asyncio.create_task(receive_messages())

    await asyncio.gather(sender_task, receiver_task, return_exceptions=True)
    await logger.flush()

def setup_video_recording(destination, message):
    documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')
    dest_folder = os.path.normpath(os.path.join(documents_folder, destination))

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    trial_number = len([name for name in os.listdir(dest_folder) if os.path.isfile(os.path.join(dest_folder, name))])
    video_file_name = message.get("filename", f"RENAME_recording_{trial_number + 1}.mp4")
    if not video_file_name.endswith(".mp4"):
        video_file_name += ".mp4"

    return dest_folder, video_file_name
