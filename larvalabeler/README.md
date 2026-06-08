# larvalabeler: Automated Zebrafish Larvae Annotation

## Overview

larvalabeler streamlines the process of creating annotated zebrafish larvae datasets for computer vision tasks. This project is designed to automate the process of extracting frames from a video, generating annotations using state-of-the-art (SOTA) computer vision models, filtering out frames without annotations, and allowing user review and refinement of the annotations. The ultimate goal is to prepare a well-structured dataset for training or evaluation in various computer vision tasks.

## Key Features

-   **Automated Pipeline:** Efficiently extracts frames, generates annotations, and filters empty images.
-   **SOTA Model Integration:** Leverages powerful computer vision models for accurate annotation.
-   **Customizable Configuration:** Easily adapt the pipeline to different datasets and tasks through a `config.yaml` file.
-   **Dataset Organization:** Structures the final dataset into training, validation, and test sets.

## Pipeline Description

`larvalabeler` is structured as a multi-step pipeline:

1. **Configuration and Setup:** Loads parameters from `config.yaml` and initializes logging.
2. **Frame Extraction:** Extracts a specified number of random frames from the input video.
3. **Annotation Generation:** Utilizes a detection model and a SAM model to generate annotations for each frame.
4. **Filtering Empty Images:** Removes frames without annotations to maintain dataset quality.
5. **User Review:** Presents a graphical interface for users to review and refine annotations.
6. **Dataset Preparation:** Organizes the annotated images into a structured dataset ready for model training.

## File Structure

-   **`main.py`:** Main script that orchestrates the entire pipeline.
-   **`utils.py`:** Contains utility functions for configuration loading, logging, etc.
-   **`extract.py`:** Handles frame extraction from video files.
-   **`annotation.py`:** Manages annotation generation and filtering of empty images.
-   **`review.py`:** Provides the user interface for annotation review.
-   **`combine.py`:** Structures the final dataset for training/evaluation.

## Requirements

-   Python 3.12

## Installation

1. **Clone the Repository**: First, you'll need to clone this repository to your local machine. This step will download all the files you need to run the `larvalabeler` pipeline.

    Open your terminal or command prompt and run the following command:

    ```bash
    git clone https://github.com/Lin-Lab-CSB/larvalabeler.git
    ```

2. **Set Up a Virtual Environment (Recommended)**: It's recommended to create a virtual environment before installing the required dependencies. This helps keep your Python environment clean and avoids conflicts with other projects.

    In your terminal, navigate to the directory where you cloned the repository:

    ```bash
    cd larvalabeler
    ```

    Then, create a virtual environment by running:

    - On macOS/Linux:

        ```bash
        python3 -m venv venv
        ```

    - On Windows:

        ```bash
        python -m venv venv
        ```

    To activate the virtual environment, use the following commands:

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    Once activated, your terminal should show `(venv)` before the command prompt, indicating that the virtual environment is active.

3. **Install Dependencies**: With the virtual environment activated, you can now install the required dependencies. Run the following command:

    ```bash
    pip install -r requirements.txt
    ```

    This command reads the `requirements.txt` file and installs all the necessary packages that `larvalabeler` depends on.

## How to Run

1. **Set up Configuration**: Modify the `config.yaml` file to include the paths, model details, and other parameters specific to your setup. This file tells the pipeline where to find your data and how to process it.

2. **Run the Pipeline**: To start the pipeline, simply run the `main.py` script. This will kick off the entire process, including frame extraction, annotation generation, filtering of empty images, and the review process:

    ```bash
    python main.py
    ```

3. **Review the Dataset**: After the pipeline completes, you'll have a well-organized dataset ready for training or evaluation in your computer vision tasks. You can manually review and refine the annotations using the provided interface.

## Future Improvements

-   Integration with additional annotation tools or models for more robust annotations.
-   Automated hyperparameter tuning for optimal frame extraction and annotation generation.
-   Expansion of the pipeline to handle additional data formats or more complex preprocessing steps.

## License

To be determined.
