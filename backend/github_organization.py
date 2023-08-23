import datetime
import json
import os

import redis

from github import Github
from github import Auth


NOW = datetime.datetime.utcnow()
THIRTY_DAYS = datetime.timedelta(seconds=60 * 60 * 24 * 5)  # TODO: set to 30 days!!!


def handle_sentry_repo(repo):
    """
    Parse teams from codeowners and make each team a country.
    """
    # Parse CODEOWNERS file
    file_content = repo.get_contents(".github/CODEOWNERS")
    codeowners = file_content.decoded_content.decode()

    owners = {}
    path_to_owner = {}

    for line in codeowners.split("\n"):
        if line.startswith("#") or line == "":
            continue

        parts = line.split()
        owner = parts[1]
        path = parts[0]
        if owner not in owners.keys():
            owners[owner] = {"paths": [], "authors": [], "known_authors": set()}
        else:
            owners[owner]["paths"].append(path)

        path_to_owner[path] = owner

    # get authors of repository
    commits = [x for x in repo.get_commits(since=NOW - THIRTY_DAYS)]
    for commit in commits:
        if hasattr(commit, "author") and commit.author is not None:
            changed_files = [f.filename for f in commit.files]

            for changed_file in changed_files:
                for path in path_to_owner.keys():
                    if ("/" + changed_file).startswith(path):
                        the_owner = path_to_owner.get(path)
                        if the_owner:
                            if (
                                commit.author.login
                                not in owners[the_owner]["known_authors"]
                            ):
                                owners[the_owner]["known_authors"].add(
                                    commit.author.login
                                )
                                owners[the_owner]["authors"].append(
                                    {
                                        "name": commit.author.name,
                                        "login": commit.author.login,
                                        "url": commit.author.url,
                                    }
                                )

    countries = []
    for owner in owners.keys():
        countries.append(
            {
                "name": owner.lower()
                .replace("@getsentry/", "")
                .replace("owners-", "")
                .replace("team-", ""),
                "full_name": owner,
                "topics": [],
                "url": "",
                "authors": owners[owner]["authors"],
            }
        )

    return countries


def load_data():
    """
    Load all production repositories from GitHub and retrieve authors of last 30 days.
    Each repo (expect "sentry") is a country. The number of authors is the size of the country.
    """
    print("Loading data from GitHub...")
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    github_access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
    auth = Auth.Token(github_access_token)
    g = Github(auth=auth)
    repos = []

    # r.delete("repositories")
    repositories = r.get("repositories")

    if repositories:
        repos = json.loads(repositories)
    else:
        repositories = g.search_repositories(query="topic:tag-production")

        for repo in repositories:  # remove slicing!!!
            # special handling for sentry repo
            # if repo.full_name == "getsentry/sentry":
            #     repos += handle_sentry_repo(repo)
            #     continue

            # get authors of repository
            commits = [x for x in repo.get_commits(since=NOW - THIRTY_DAYS)]

            known_authors = set()
            authors = []
            for commit in commits:
                if hasattr(commit, "author") and commit.author is not None:
                    if commit.author.login not in known_authors:
                        known_authors.add(commit.author.login)
                        authors.append(
                            {
                                "name": commit.author.name,
                                "login": commit.author.login,
                                "url": commit.author.url,
                            }
                        )

            # append repo
            repos.append(
                {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "topics": repo.topics,
                    "url": repo.url,
                    "authors": authors,
                }
            )

        r.set("repositories", json.dumps(repos))

    print("DONE Loading data from GitHub...")
    return repos


if __name__ == "__main__":
    handle_sentry_repo(None)
