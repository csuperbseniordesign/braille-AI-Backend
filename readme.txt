# FastAPI Application Setup

This document provides instructions to set up and run the FastAPI application in a Python virtual environment.

## Prerequisites

- Python 3.x installed on your system
- `venv` module available in your Python installation

## Setup Instructions

Follow these steps to set up and run the FastAPI application:

1. **Create a Virtual Environment**

    Open a terminal or command prompt and navigate to your project directory. Then, run the following command to create a virtual environment:


    python -m venv venv
 

2. **Activate the Virtual Environment**

    - On Windows:

      venv\Scripts\activate


    - On macOS and Linux:

      source venv/bin/activate
    

3. **Install Dependencies**

    Once the virtual environment is activated, install the required dependencies by running:

    pip install -r requirements.txt


4. **Run the FastAPI Application**

    After installing the dependencies, you can run the FastAPI application using:

    uvicorn app.main:app --reload


    Replace `main:app` with the appropriate module and application instance if different.

## Additional Information

- To deactivate the virtual environment, simply run:

  deactivate


- To update requirements.txt when installing new libraries, simply run:

pip freeze > requirements.txt


- Ensure you have a `requirements.txt` file in your project directory with all the necessary dependencies listed.

Follow these steps to set up and run the FastAPI application successfully.