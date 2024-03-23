import uvicorn

if __name__ == "__main__":
        uvicorn.run("app.api.main:APP", host="0.0.0.0", port=5174, reload=True)
