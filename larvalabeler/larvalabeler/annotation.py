import logging
import os
import shutil

from ultralytics.data.annotator import auto_annotate


def generate_annotations(
    data_dir: str, det_model: str, sam_model: str, device: str, output_dir: str
) -> None:
    """
    Generate annotations for the images in the data directory using the specified models.

    Args:
        data_dir: Directory containing images to annotate.
        det_model: Path to the detection model.
        sam_model: Path to the SAM model.
        device: Device to run the models on.
        output_dir: Directory to save the generated annotations.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        auto_annotate(
            data=data_dir,
            det_model=det_model,
            sam_model=sam_model,
            device=device,
            output_dir=output_dir,
        )
        logging.info(f"Annotations generated and saved to {output_dir}")
    except Exception as e:
        logging.error(f"Error during annotation generation: {e}")
        raise


def filter_empty_images(data_dir: str, annotation_dir: str, empty_dir: str) -> int:
    """
    Move images without corresponding annotations to the empty directory and return the count of empty images.

    Args:
        data_dir: Directory containing images.
        annotation_dir: Directory containing annotations.
        empty_dir: Directory to move images without annotations.
    """
    try:
        os.makedirs(empty_dir, exist_ok=True)
        empty_count = 0

        for image_name in os.listdir(data_dir):
            if image_name.endswith((".jpg", ".png")):
                annotation_name = image_name.rsplit(".", 1)[0] + ".txt"
                annotation_path = os.path.join(annotation_dir, annotation_name)

                if not os.path.exists(annotation_path):
                    shutil.move(
                        os.path.join(data_dir, image_name),
                        os.path.join(empty_dir, image_name),
                    )
                    logging.info(f"Moved {image_name} to {empty_dir}")
                    empty_count += 1

        logging.info(f"Filtered out {empty_count} images without annotations")
        return empty_count

    except Exception as e:
        logging.error(f"Error during filtering of empty images: {e}")
        raise
