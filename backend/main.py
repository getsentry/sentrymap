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


countries = {
    "sentry": ["sentry", "getsentry"], 
    "docs": ["sentry-docs", "develop"], 
    "ingest": ["relay"], 
    "sdks": ["sentry-android-gradle-plugin", "sentry-cocoa", "sentry-cordova", "sentry-dart", "sentry-dotnet", "sentry-electron", "sentry-elixir", "sentry-go", "sentry-java", "sentry-javascript", "sentry-javascript-bundler-plugins", "sentry-kotlin-multiplatform", "sentry-laravel", "sentry-maven-plugin", "sentry-php", "sentry-php-sdk", "sentry-python", "sentry-react-native", "sentry-ruby", "sentry-symfony", "sentry-unity", "sentry-unreal", "sentry-xamarin", ],
    "processing": ["symbolic", "symbolicator", "sentry-cli", "rust-sourcemap", "watto", "js-source-scopes"],

}

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

    from maps import HexGrid
    grid = HexGrid(21, 29) 

    for i, key in enumerate(countries.keys()):
        grid.grow_chunk2(i+1, countries[key]["size"])

    grid.print2()
    return {
        "grid": grid.grid,
    }

load_data()
