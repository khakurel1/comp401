# Optimal Portfolio Allocation

This guide provides step-by-step instructions on setting up the backend API and the frontend for the Optimal Portfolio Allocation application.

### Setting Up the Backend API

Follow these steps to prepare and run the backend API:

1. **Create and Activate a New Environment**

   First, create a new virtual environment and activate it. This ensures that the dependencies for the project do not interfere with your global Python setup.

   - For Unix/macOS:

     ```bash
     python -m venv env && source env/bin/activate
     ```

   - For Windows:

     ```cmd
     python -m venv env
     .\env\Scripts\activate
     ```

2. **Install the Requirements**

   Install all the required packages listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**

   Start the backend server by running:

   ```bash
   python api/main.py
   ```

   This command starts the backend server, which the frontend will communicate with.

### Setting Up the Frontend

To set up the frontend for the Optimal Portfolio Allocation application, follow these steps:

1. **Navigate to the Frontend Directory**

   Change to the `frontend` directory where the frontend code resides:

   ```bash
   cd ./frontend/
   ```

2. **Install the Packages**

   Install the necessary npm packages required for the frontend:

   ```bash
   npm install
   ```

3. **Run the Frontend**

   From inside the `frontend` folder, start the frontend development server:

   ```bash
   npm run dev
   ```

   This will serve the frontend application, which can be accessed through a web browser.

