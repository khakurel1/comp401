# Optimal Portfolio Allocation Application

## Table of Contents

1. [Introduction](#introduction)
2. [Background and Motivation](#background-and-motivation)
3. [Application Overview](#application-overview)
4. [Key Features](#key-features)
5. [Technical Stack](#technical-stack)
6. [Setting Up the Backend API](#setting-up-the-backend-api)
   - [Create and Activate a New Environment](#create-and-activate-a-new-environment)
   - [Install the Requirements](#install-the-requirements)
   - [Run the Server](#run-the-server)
7. [Setting Up the Frontend](#setting-up-the-frontend)
   - [Navigate to the Frontend Directory](#navigate-to-the-frontend-directory)
   - [Install the Packages](#install-the-packages)
   - [Run the Frontend](#run-the-frontend)
8. [Contributing](#contributing)
9. [License](#license)
10. [Contact](#contact)

## Introduction

The Optimal Portfolio Allocation application is a dynamic web-based platform designed to assist users in crafting optimized investment portfolios tailored to their risk tolerance and financial goals.

## Background and Motivation

The Optimal Portfolio Allocation application is conceived at the intersection of economics, mathematics, and computing, drawing inspiration from academic coursework in Econ 337, portfolio management exercises, and professional shadowing experiences. This project aims to demystify the complexities of portfolio allocation and asset pricing for those new to the financial industry, fostering a deeper understanding and confidence in investment strategies.

In a landscape where financial tools and literacy remain largely accessible to a privileged few, the widening wealth gap underscores the urgent need for inclusive financial education. The Optimal Portfolio Allocation application seeks to bridge this divide, offering a user-friendly interface that empowers users to make informed investment decisions, regardless of their financial background.

## Application Overview

The Optimal Portfolio Allocation application is a dynamic web-based platform designed to assist users in crafting optimized investment portfolios tailored to their risk tolerance and financial goals. Utilizing a sophisticated mathematical framework, the application guides users through the process of allocating their wealth across various asset classes, balancing risk and return to achieve optimal portfolio performance.

### Key Features:

- **User-Centric Design**: Prioritizing ease of use and accessibility, the application offers a robust login system and intuitive navigation, ensuring a seamless user experience.
- **Advanced Portfolio Optimization**: Drawing on principles from the Efficient Frontier and Modern Portfolio Theory, the application provides personalized portfolio recommendations based on user input such as asset preferences and risk tolerance.
- **Interactive Learning Experience**: Users are encouraged to experiment with different asset allocations, gaining hands-on experience and insights into the fundamentals of portfolio diversification and risk management.
- **Inclusive and Equitable**: The application is designed with a strong emphasis on racial and gender equity, employing gender-neutral language and ensuring compliance with Web Content Accessibility Guidelines (WCAG) to accommodate a diverse user base.

### Technical Stack:

- **Backend**: Python with FastAPI for creating efficient, scalable APIs.
- **Database**: SQLite, chosen for its simplicity and ease of integration, to manage user data and historical asset performance.
- **Frontend**: A responsive design utilizing HTML, CSS, and JavaScript to provide a dynamic, engaging user interface.
- **Security**: Implementation of JWTBearer for authentication, ensuring secure access to the application's features.

The following guide provides step-by-step instructions on setting up the backend API and the frontend for the Optimal Portfolio Allocation application.

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

To ensure that all necessary Python packages are installed for the project to run properly, you will need to install the dependencies listed in the requirements.txt file. After setting up your Python environment, you can install these dependencies using pip, Python's package installer.
   ```bash
   pip install -r requirements.txt
   ```
This command will automatically read the requirements.txt file and install all the listed packages along with their specified versions. Make sure you are in the project's root directory where requirements.txt is located when you run this command.

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

   ## Contributing

We welcome contributions from the community! If you'd like to contribute to the Optimal Portfolio Allocation application, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them thoroughly.
4. Commit your changes with a descriptive commit message.
5. Push your branch to your forked repository.
6. Submit a pull request to the main repository, providing a clear description of your changes and any necessary context.

## License

The Optimal Portfolio Allocation application is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

If you have any questions or need assistance, please feel free to reach out at [khakurel1@kenyon.edu](mailto:khakurel1@kenyon.edu).


