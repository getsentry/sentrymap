import json

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from github_organization import load_data

import redis


app = FastAPI(debug=True)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    # On startup the data is saved in redis
    repos = []
    repositories = r.get("repositories")
    if repositories:
        repos = json.loads(repositories)

    countries = []
    for repo in repos:
        countries.append(
            {
                "name": repo["name"],
                "size": len(repo["authors"]) + 1,
            }
        )

    from maps import HexGrid
    grid = HexGrid(21, 29) 
    # grid.grow_chunk2(sum(c["size"] for c in countries))
    grid.grow_chunk2(22)

    return {
        "grid": grid.grid,
    }

load_data()
