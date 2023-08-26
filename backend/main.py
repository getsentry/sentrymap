import json
import os
import random

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import redis

from data import load_data
from hexgrid import HexGrid
from utils import normalize_countries


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


COUNTRY_NAMES = {
    "sentry": "The United States of Sentry",
    "docs": "Docstopia",
    "ingest": "Ingestistan",
    "sdks": "SDKingdom",
    "processing": "Processia",
}

REPO_TO_COUNTRY = {
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

class DECOR:
    CASTLE = -1
    MOUNTAIN = -2
    PYRAMIDE = -3
    PORTAL = -4 
    SPRING = -5
    CASTLE2 = -6
    HORSE = -7
    MONSTER = -8
    TREAURE = -9
    ISLAND = -10
    WRECK = -11
    BOAT_SMALL = -12
    BOAT_TILE_3 = -13
    BOAT_TILE = -14
    TREES = -15
  
START_TILE = {
    "sentry": DECOR.CASTLE,
    "docs": DECOR.HORSE,
    "ingest": DECOR.PYRAMIDE,
    "sdks": DECOR.MOUNTAIN,
    "processing": DECOR.PORTAL,
}


@app.get("/clear-cache")
async def home(request: Request):
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.delete("repositories")
    return {"status": "ok"}


@app.get("/reload-data")
async def home(request: Request):
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.delete("repositories")
    load_data()
    return {"status": "ok"}


@app.get("/")
async def home(request: Request):
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

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
        country = REPO_TO_COUNTRY.get(repo["name"])
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
                "name": COUNTRY_NAMES[country],
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
    countries = normalize_countries(countries, 1, 60)    
    from pprint import pprint
    print("Countries:")
    pprint(countries)

    # Generate grid and labels to draw the map
    grid = HexGrid(19, 39) 
    labels = []
    for i, key in enumerate(countries.keys()):
        points_in_land = grid.grow_chunk(i+1, countries[key]["size"])

        start_point = points_in_land[0]
        grid.grid[start_point[0]][start_point[1]] = START_TILE[key]

        if countries[key]["name"] == "sentry":
            grid.grid[points_in_land[1][0]][points_in_land[1][1]] = DECOR.SPRING
            grid.grid[points_in_land[2][0]][points_in_land[3][1]] = DECOR.TREES
            grid.grid[points_in_land[3][0]][points_in_land[3][1]] = DECOR.TREES
            grid.grid[points_in_land[4][0]][points_in_land[3][1]] = DECOR.TREES
        elif countries[key]["name"] == "docs":
            grid.grid[points_in_land[1][0]][points_in_land[1][1]] = DECOR.HORSE
            grid.grid[points_in_land[2][0]][points_in_land[2][1]] = DECOR.HORSE
            grid.grid[points_in_land[3][0]][points_in_land[3][1]] = DECOR.HORSE
        elif countries[key]["name"] == "sdks":
            pass

        if i == 0:
            THINGS_TO_DRAW = [
                DECOR.MONSTER, DECOR.ISLAND, DECOR.WRECK, DECOR.BOAT_SMALL, DECOR.BOAT_TILE
            ]
            for j in range(0, 5):
                while True:
                    x, y = random.randint(0, grid.rows-1), random.randint(0, grid.cols-1)
                    if grid.grid[x][y] == 0:
                        grid.grid[x][y] = THINGS_TO_DRAW[j]
                        break

        labels.append({"text": COUNTRY_NAMES[key], "x": points_in_land[0][0], "y": points_in_land[0][1]})

    grid.print()

    return {
        "grid": grid.grid,
        "labels": labels,
        "country_info": country_info,
    }

# When app starts, load data from Github.
load_data()
