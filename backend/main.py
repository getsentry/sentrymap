import json

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from github_organization import load_data

import redis


app = FastAPI(debug=True)

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

    return countries


load_data()
