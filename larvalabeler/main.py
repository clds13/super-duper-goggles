import logging
import os

import yaml
from larvalabeler.annotation import filter_empty_images, generate_annotations
from larvalabeler.extract import extract_random_frames
from larvalabeler.review import review_annotations
from larvalabeler.utils import load_config, setup_logging


def main():
    # Load configuration
    config = load_config()

    # Set up logging
    setup_logging(config["logging"]["log_file"], config["logging"]["level"])

    try:
        logging.info("Starting the annotation workflow...")

        # Step 1: Extract frames from video
        extract_random_frames(
            config["input"]["video"],
            config["input"]["frames"],
            config["output"]["project"],
            seed=42,
        )

        # Step 2: Generate annotations
        generate_annotations(
            config["output"]["project"],
            config["models"]["detector"],
            config["models"]["sam"],
            config["hardware"]["device"],
            config["output"]["project"],
        )

        # Step 3: Filter out images without annotations
        empty_count = filter_empty_images(
            config["output"]["project"],
            config["output"]["project"],
            config["output"]["empty_dir"],
        )

        # Step 4: User input for remaining images
        review_metadata = review_annotations(
            config["output"]["project"],
            config["output"]["project"],
            config["output"]["save_dir"],
            config["output"]["review_dir"],
        )

        # Save overall metadata at the root level of the project directory
        metadata = {
            "video_file": config["input"]["video"],
            "total_frames_requested": config["input"]["frames"],
            "empty_images": empty_count,
            "review_metadata": review_metadata,
            "random_seed": 42,
        }
        metadata_path = os.path.join(config["output"]["project"], "metadata.yaml")
        with open(metadata_path, "w") as file:
            yaml.dump(metadata, file)
        logging.info(f"Saved metadata to {metadata_path}")

        logging.info("Annotation workflow completed successfully.")

    except Exception as e:
        logging.error(f"Workflow failed: {e}")
        raise


if __name__ == "__main__":
    main()
