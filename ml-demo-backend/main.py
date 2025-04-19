from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS to allow requests from your GitHub Pages domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourusername.github.io"],  # Your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI backend"}

@app.get("/api/data")
async def get_data():
    return {"data": [1, 2, 3, 4, 5]}