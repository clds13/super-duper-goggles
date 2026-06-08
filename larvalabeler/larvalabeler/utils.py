import logging
import os

import yaml


def load_config(config_path="config.yaml"):
    """
    Load the YAML configuration file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        config: Dictionary containing the configuration settings.
    """
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # Construct full paths for the output directories and log file
    project_dir = config["output"]["project"]
    config["output"]["save_dir"] = os.path.join(project_dir, config["output"]["save"])
    config["output"]["review_dir"] = os.path.join(
        project_dir, config["output"]["review"]
    )
    config["output"]["empty_dir"] = os.path.join(project_dir, config["output"]["empty"])
    config["logging"]["log_file"] = os.path.join(project_dir, config["output"]["log"])

    return config


def setup_logging(log_file, log_level):
    """
    Set up logging configuration.

    Args:
        log_file: Path to the log file.
        log_level: Logging level.
    """
    # Ensure the directory for the log file exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.getLogger().addHandler(logging.StreamHandler())
