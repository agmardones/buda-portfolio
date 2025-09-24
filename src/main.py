from fastapi import FastAPI

from src.rest.router import router as portfolio_router

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(portfolio_router)
