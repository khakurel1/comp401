# This is a Python script that uses the uvicorn library to run a FastAPI application.

# The script starts by importing the uvicorn module, which is a Python ASGI server for FastAPI applications.

# The script then checks if it is being run as the main program (i.e., when the script is executed directly, not imported as a module).

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api.main:APP", host="0.0.0.0", port=8081, reload=True)

# When the script is executed, it will start the FastAPI application on the specified host and port, and it will automatically reload the application when changes are detected in the source code.
