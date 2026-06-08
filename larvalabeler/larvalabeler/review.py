import logging
import os
import shutil

import cv2
import numpy as np

ANNOTATION_WINDOW_NAME = "Annotated Image"
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1200
SAVE_KEY = ord("s")
DISCARD_KEY = ord("d")
REVIEW_KEY = ord("r")


def display_annotation(image_path: str, annotation_path: str) -> str:
    """
    Display the image with annotations and wait for user input to determine the next action.

    Args:
        image_path: Path to the image file.
        annotation_path: Path to the annotation file.

    Returns:
        Action as a string ('save', 'discard', 'review').
    """
    cv2.namedWindow(ANNOTATION_WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(ANNOTATION_WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

    image = cv2.imread(image_path)

    with open(annotation_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split()
        _ = int(parts[0])
        points = np.array(list(map(float, parts[1:]))).reshape(-1, 2)
        points[:, 0] *= image.shape[1]
        points[:, 1] *= image.shape[0]
        points = points.astype(int)

        cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imshow(ANNOTATION_WINDOW_NAME, image)
    key = cv2.waitKey(0)

    if key == SAVE_KEY:
        return "save"
    elif key == DISCARD_KEY:
        return "discard"
    elif key == REVIEW_KEY:
        return "review"
    else:
        return ""


def review_annotations(
    data_dir: str, annotation_dir: str, save_dir: str, review_dir: str
) -> dict:
    """
    Review annotations, allowing the user to save, discard, or mark for review.

    Args:
        data_dir: Directory containing images.
        annotation_dir: Directory containing annotations.
        save_dir: Directory to save accepted annotations and images.
        review_dir: Directory to save annotations and images marked for review.

    Returns:
        metadata: Dictionary containing metadata about the review process.
    """
    try:
        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(review_dir, exist_ok=True)
        save_count, review_count, discard_count = 0, 0, 0

        for image_name in os.listdir(data_dir):
            if image_name.endswith((".jpg", ".png")):
                image_path = os.path.join(data_dir, image_name)
                annotation_path = os.path.join(
                    annotation_dir, image_name.rsplit(".", 1)[0] + ".txt"
                )

                if os.path.exists(annotation_path):
                    action = display_annotation(image_path, annotation_path)

                    if action == "save":
                        shutil.move(
                            annotation_path,
                            os.path.join(save_dir, os.path.basename(annotation_path)),
                        )
                        shutil.move(
                            image_path,
                            os.path.join(save_dir, os.path.basename(image_path)),
                        )
                        logging.info(
                            f"Saved {image_name} and its annotation to {save_dir}"
                        )
                        save_count += 1
                    elif action == "discard":
                        os.remove(annotation_path)
                        os.remove(image_path)
                        logging.info(f"Discarded {image_name} and its annotation")
                        discard_count += 1
                    elif action == "review":
                        shutil.move(
                            annotation_path,
                            os.path.join(review_dir, os.path.basename(annotation_path)),
                        )
                        shutil.move(
                            image_path,
                            os.path.join(review_dir, os.path.basename(image_path)),
                        )
                        logging.info(
                            f"Moved {image_name} and its annotation to {review_dir}"
                        )
                        review_count += 1
                    else:
                        logging.info(f"Skipping {image_name}")

        # Return metadata about the review process
        metadata = {
            "saved_images": save_count,
            "review_images": review_count,
            "discarded_images": discard_count,
        }
        return metadata

    except Exception as e:
        logging.error(f"Error during annotation review: {e}")
        raise
