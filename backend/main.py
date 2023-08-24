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
    "sdks": "SDKingdom",
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

    # Get all country information
    country_info = {}
    country_known_residents = {}

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

        if country not in country_known_residents.keys():
            country_known_residents[country] = set()

        # Add residents to country
        unique_authors = []
        for author in repo["authors"]:
            if author["login"] not in country_known_residents[country]:
                country_known_residents[country].add(author["login"])
                unique_authors.append(author)

        if country not in country_info.keys():
            country_info[country] = {
                "name": country_names[country],
                "residents": unique_authors,
                "provinces": set([repo["name"], ]),
            }
        else:
            country_info[country]["residents"] += unique_authors
            country_info[country]["provinces"].add(repo["name"])

    # Sort residents and provinces
    for country in country_info.keys():
        country_info[country]["residents"] = sorted(country_info[country]["residents"], key=lambda x: x.get("name") or x.get("login"))
        country_info[country]["provinces"] = sorted(country_info[country]["provinces"], key=lambda x: x.lower())

    # Normalize country sizes
    countries = normalize_countries(countries, 1, 30)    
    from pprint import pprint
    pprint(countries)

    # Generate grid and labels to draw the map
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
        "country_info": country_info,
    }

# When app starts, load data from Github.
load_data()
