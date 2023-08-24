import json

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from github_organization import load_data
from utils import normalize_countries

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

repo_to_country = {
    "sentry": "sentry", 
    "getsentry": "sentry",
    "sentry-docs": "docs", 
    "develop": "docs",
    "relay": "ingest",
    "sentry-android-gradle-plugin": "sdks", 
    "sentry-cocoa": "sdks", 
    "sentry-cordova": "sdks", 
    "sentry-dart": "sdks", 
    "sentry-dotnet": "sdks", 
    "sentry-electron": "sdks",
    "sentry-elixir": "sdks", 
    "sentry-go": "sdks",
    "sentry-java": "sdks", 
    "sentry-javascript": "sdks", 
    "sentry-javascript-bundler-plugins": "sdks", 
    "sentry-kotlin-multiplatform": "sdks", 
    "sentry-laravel": "sdks", 
    "sentry-maven-plugin": "sdks", 
    "sentry-php": "sdks", 
    "sentry-php-sdk": "sdks", 
    "sentry-python": "sdks", 
    "sentry-react-native": "sdks", 
    "sentry-ruby": "sdks", 
    "sentry-symfony": "sdks", 
    "sentry-unity": "sdks", 
    "sentry-unreal": "sdks", 
    "sentry-xamarin": "sdks",
    "symbolic": "processing", 
    "symbolicator": "processing", 
    "sentry-cli": "processing", 
    "rust-sourcemap": "processing", 
    "watto": "processing", 
    "js-source-scopes": "processing",
}

country_names = {
    "sentry": "The United States of Sentry",
    "docs": "Docstopia",
    "ingest": "Ingestistan",
    "sdks": "SDKSSR",
    "processing": "Processia",
}


@app.get("/clear-cache")
async def home(request: Request):
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.delete("repositories")
    return {"status": "ok"}


@app.get("/")
async def home(request: Request):
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    # On startup the data is saved in redis
    repos = []
    repositories = r.get("repositories")
    if repositories:
        repos = json.loads(repositories)

    countries = {}
    for repo in repos:
        country = repo_to_country.get(repo["name"])
        if country is None:
            continue

        if country not in countries.keys():
            countries[country] = {
                "name": country,
                "size": len(repo["authors"])+1,
            }
        else:
            countries[country]["size"] += len(repo["authors"])

    from pprint import pprint
    pprint(countries)

    countries = normalize_countries(countries, 1, 30)    
    pprint(countries)

    from maps import HexGrid
    grid = HexGrid(21, 29) 

    labels = []
    for i, key in enumerate(countries.keys()):
        chunk_x, chunk_y = grid.grow_chunk2(i+1, countries[key]["size"])
        labels.append({"text": country_names[key], "x": chunk_x, "y": chunk_y})

    grid.print2()
    return {
        "grid": grid.grid,
        "labels": labels,
    }

load_data()
