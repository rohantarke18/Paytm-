from fastapi import FastAPI

app = FastAPI(
    title="Merchant Growth AI",
    description="Autonomous AI teammate for Paytm merchants",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Merchant Growth AI is running!",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }