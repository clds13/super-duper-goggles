import logging
import os
import random

import cv2
import yaml


def extract_random_frames(
    video_path: str, num_frames: int, output_dir: str, seed: int
) -> None:
    """
    Extracts a specified number of random frames from a video and saves them as images.
    Also saves metadata about the extraction process.

    Args:
        video_path: The path to the video file.
        num_frames: The number of frames to extract.
        output_dir: The directory to save the extracted frames.
        seed: The random seed for frame selection to ensure reproducibility.
    """
    try:
        # Set the random seed for reproducibility
        random.seed(seed)

        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        if num_frames > total_frames:
            raise ValueError(
                f"Cannot extract {num_frames} frames. Video only has {total_frames} frames."
            )

        frame_indices = random.sample(range(total_frames), num_frames)
        os.makedirs(output_dir, exist_ok=True)

        for i, frame_index in enumerate(frame_indices):
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = video.read()
            if ret:
                frame_filename = f"frame_{i}.jpg"
                frame_path = os.path.join(output_dir, frame_filename)
                cv2.imwrite(frame_path, frame)
                logging.info(f"Saved frame {frame_index} as {frame_path}")
            else:
                logging.warning(f"Failed to read frame {frame_index}")

        video.release()
        logging.info(
            f"Successfully extracted {len(frame_indices)} frames from {video_path}"
        )

        # Save metadata about the frame extraction process
        metadata = {
            "video_file": video_path,
            "total_frames_in_video": total_frames,
            "extracted_frames": num_frames,
            "random_seed": seed,
            "frame_indices": frame_indices,
        }
        metadata_path = os.path.join(output_dir, "metadata.yaml")
        with open(metadata_path, "w") as file:
            yaml.dump(metadata, file)
        logging.info(f"Saved metadata to {metadata_path}")

    except Exception as e:
        logging.error(f"Error during frame extraction: {e}")
        raise
