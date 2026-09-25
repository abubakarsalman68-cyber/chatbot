from fastapi import FastAPI

app = FastAPI(title="OpenChat Backend")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "OpenChat backend is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
