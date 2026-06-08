# Installation Guide

## Prerequisites

Here are some prerequisites you'll need to have ready on your system:

1. Node.js

Install Node.js which is useful for developing server-side and networking applications. SvelteKit is built on top of it.

You can download it from [here](https://nodejs.org/en/download/).

2. Anaconda

Since the backend of socialiZe uses an older Python version (limited by the compatibility of the Spinnaker SDK), you should use Conda to install the required version of Python.

You can download Anaconda from [here](https://www.anaconda.com/download). For more instructions on setting it up on your system, follow the link below to your operating system:

| Operating System |
| ---------------- |
| [Windows](https://docs.anaconda.com/anaconda/install/windows/) |
| [macOS](https://docs.anaconda.com/anaconda/install/mac-os/) |
| [Linux](https://docs.anaconda.com/anaconda/install/linux/) |

3. Git

Install Git which is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

You can download it from [here](https://git-scm.com/downloads).

4. Spinnaker SDK

Since the current implementation of socialiZe uses a FLIR camera, it needs the Spinnaker SDK for the rest of the application to interact with it. The SDK is not available through standard means (i.e., how Python packages are usually available through `pip`), and it must be downloaded directly from [FLIR](https://www.flir.ca/products/spinnaker-sdk/) which requires an account (free to create).

Once the SDK is downloaded, extract the `.whl` file from the archive and save it to your Downloads directory. This will allow the Conda setup to recognize the SDK and install it as a part of the environment. For development, the SDK for Python 3.8 is being used, and it should be named with a similar convention to the following:

```
spinnaker_python-3.0.0.118-cp38-cp38-win_amd64.whl
```

Where `cp38` means Python 3.8, and `win_amd64` denotes the platform (in this case, Windows). If you have errors setting up the Conda environment, modify Line 13 of `environment.yml` to have the correct name of your downloaded Wheel file.

## Setup

Setup is divided into two parts: frontend and backend. The frontend is built using SvelteKit and the backend is built using FastAPI.

Please use two separate terminals windows to setup/run the frontend and backend. Cloning the repository can be done in either terminal and will be required to setup both the frontend and backend (should be done only once when first downloading the program).

### Cloning the repository

1. Clone the repository

```bash
git clone https://github.com/LinLabGithub/Social.git
```

This will clone the repository into a folder named `Social` in your current directory. For example, if you called `git clone` from your `Downloads` directory, you will find the cloned repository in `~/Downloads/Social`.

2. Create the Conda environment

```bash
conda env create -f environment.yml
```

This will create a Conda environment named `socialize` with all the required dependencies installed. The dependencies are listed in the `environment.yml` file.

3. Activate the Conda environment

```bash
conda activate socialize
```

This will activate the Conda environment. You will need to activate the Conda environment every time you want to run the backend.

### Setting up the Frontend

1. Navigate to the `frontend` directory

```bash
cd frontend
```

This will change your current directory to the `frontend` directory. Make sure you are in the `frontend` directory that is inside the `Social` directory you cloned in the first part of the setup.

2. Install the dependencies

```bash
npm install
```

This will install all the dependencies required to run the frontend. The dependencies are listed in the `package.json` file.

3. Run the frontend

```bash
npm run dev
```

This will run the frontend in development mode. You can access the frontend at `localhost:5173` in your browser.

### Setting up the Backend

1. Navigate to the `backend` directory

```bash
cd backend
```

This will change your current directory to the `backend` directory. Make sure you are in the `backend` directory that is inside the `Social` directory you cloned in the first part of the setup.

2. Run the backend

```bash
uvicorn main:app --reload
```

This will run the FastAPI backend server which the frontend will be communicating with to receive the camera feed.

## Post Installation

After the setup is complete, you can run the frontend and backend using the following commands:

### Activate the Environment

```bash
conda activate socialize
```

NOTE: This should only be done in the Terminal that will be used to run the backend.

### Running the Frontend

```bash
cd frontend
npm run dev
```

### Running the Backend

```bash
cd backend
uvicorn main:app --reload
```