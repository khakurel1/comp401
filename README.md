# Optimal Portfolio Allocation Application

## Table of Contents

- [Getting Started](#getting-started)
  - [Introduction](#introduction)
  - [Background and Motivation](#background-and-motivation)
  - [Application Overview](#application-overview)
  - [Key Features](#key-features)
  - [Technical Stack](#technical-stack)
  - [Setting Up the Backend API](#setting-up-the-backend-api)
  - [Setting Up the Frontend](#setting-up-the-frontend)
- [User Guide](#user-guide)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Contributing Guidelines](#contributing-guidelines)
- [Frequently Asked Questions (FAQ)](#faq)
- [Glossary](#glossary)
- [Appendix](#appendix)
- [License](#license)
- [Contact](#contact)

## Getting Started

### Introduction

The Optimal Portfolio Allocation application is a dynamic web-based platform designed to assist users in crafting optimized investment portfolios tailored to their risk tolerance and financial goals.

### Background and Motivation

The Optimal Portfolio Allocation application is conceived at the intersection of economics, mathematics, and computing, drawing inspiration from academic coursework in Econ 337, portfolio management exercises, and professional shadowing experiences. This project aims to demystify the complexities of portfolio allocation and asset pricing for those new to the financial industry, fostering a deeper understanding and confidence in investment strategies.

In a landscape where financial tools and literacy remain largely accessible to a privileged few, the widening wealth gap underscores the urgent need for inclusive financial education. The Optimal Portfolio Allocation application seeks to bridge this divide, offering a user-friendly interface that empowers users to make informed investment decisions, regardless of their financial background.

### Application Overview

The Optimal Portfolio Allocation application is a dynamic web-based platform designed to assist users in crafting optimized investment portfolios tailored to their risk tolerance and financial goals. Utilizing a sophisticated mathematical framework, the application guides users through the process of allocating their wealth across various asset classes, balancing risk and return to achieve optimal portfolio performance.

#### Key Features

- **User-Centric Design**: Prioritizing ease of use and accessibility, the application offers a robust login system and intuitive navigation, ensuring a seamless user experience.
- **Advanced Portfolio Optimization**: Drawing on principles from the Efficient Frontier and Modern Portfolio Theory, the application provides personalized portfolio recommendations based on user input such as asset preferences and risk tolerance.
- **Interactive Learning Experience**: Users are encouraged to experiment with different asset allocations, gaining hands-on experience and insights into the fundamentals of portfolio diversification and risk management.
- **Inclusive and Equitable**: The application is designed with a strong emphasis on racial and gender equity, employing gender-neutral language and ensuring compliance with Web Content Accessibility Guidelines (WCAG) to accommodate a diverse user base.

#### Technical Stack

- **Backend**: Python with FastAPI for creating efficient, scalable APIs.
- **Database**: SQLite, chosen for its simplicity and ease of integration, to manage user data and historical asset performance.
- **Frontend**: A responsive design utilizing HTML, CSS, and JavaScript to provide a dynamic, engaging user interface.
- **Security**: Implementation of JWTBearer for authentication, ensuring secure access to the application's features.

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
      python -m venv env && .\env\Scripts\activate
      ```

2. **Install the Requirements**

    To ensure that all necessary Python packages are installed for the project to run properly, you will need to install the dependencies listed in the `requirements.txt` file. After setting up your Python environment, you can install these dependencies using `pip`, Python's package installer.

    ```bash
    pip install -r requirements.txt
    ```

    This command will automatically read the `requirements.txt` file and install all the listed packages along with their specified versions. Make sure you are in the project's root directory where `requirements.txt` is located when you run this command.

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

## Contributing Guidelines

We welcome contributions from the community! If you'd like to contribute to the Optimal Portfolio Allocation application, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them thoroughly.
4. Commit your changes with a descriptive commit message.
5. Push your branch to your forked repository.
6. Submit a pull request to the main repository, providing a clear description of your changes and any necessary context.




# Stock-Evaluator Project Setup Guide

## Connecting to the Virtual Machine

To initiate a connection to your virtual machine, use the following SSH command:

```bash
ssh -i ~/.ssh/id_rsa.pem asmodk@172.172.155.79
Make sure to replace ~/.ssh/id_rsa.pem with the actual path to your private key and 172.172.155.79 with the IP address of your VM.
```
Exploring the Project Directory
After logging into the VM, you can navigate through the project's structure:

```bash
ls # Lists the contents of the home directory, look for 'stock-evaluator'
cd stock-evaluator/ # Changes the directory to 'stock-evaluator'
ls # Lists the project files including 'LICENSE', 'README.md', etc.
```
Running the Application with Podman-Compose
Use podman-compose to start the application's services:

```bash
podman-compose up -d # Starts services in detached mode
podman ps # Shows running containers to verify they started correctly
```

If you have made changes to the compose.yaml or need to restart the services, run:

```bash
podman-compose up -d # This command can be repeated as needed
```


# Stock-Evaluator Project Deployment Guide

This guide outlines the steps for deploying the Stock-Evaluator project using Podman, a daemonless container engine, and Podman Compose as an alternative to Docker.

## Deployment Process Overview

1. **Containerize the Application using Podman and Podman Compose**

2. **Provision a Virtual Machine (VM)**

3. **Set up Nginx on the VM**

   - Nginx will act as a reverse proxy to direct traffic appropriately within the VM.

4. **Build the Image from the Container Registry**

   - Instead of Docker Hub, use a compatible registry that works with Podman if needed.

5. **Set up Podman environment in the VM**

   - Install Podman and configure it to manage your containers.

6. **Compile the Frontend into Static Files**

   - Prepare the frontend components to be served through Nginx.

7. **Run the Podman Compose Configuration**

   - Utilize `podman-compose` to deploy the services as defined in your configuration files.

## Deployment Architecture

- **Client**: Sends requests via HTTP.
- **Reverse Proxy (Nginx)**: Directs incoming requests to the appropriate service.
- **Frontend**: Provides the user interface, served by Nginx.
- **Compiled Static Files**: The assets (HTML, CSS, JavaScript) used by the frontend.
- **Podman Containers**: Run the Python APIs, each listening on its own port.
- **Load Balanced Backend**: A load balancer that distributes incoming API requests evenly across the containers.

Note: In this setup, Podman is used in place of Docker, providing a similar functionality with the added benefit of not requiring a daemon to run.



## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or need assistance, please feel free to reach out at [khakurel1@kenyon.edu](mailto:khakurel1@kenyon.edu).
