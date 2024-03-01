import requests
from fastapi import FastAPI, Query, Path
from cachetools import LRUCache

from models import Repo, Activity


app = FastAPI()
cache = LRUCache(maxsize=1)


@app.get("/api/v1/repos/top100")
def get_top100(sort_by: str = Query("stars")):
    """Получает топ 100 репозиториев с возможностью сортировки."""

    url = "https://api.github.com/search/repositories"
    params = {
        "q": "is:public",
        "sort": sort_by,
        "per_page": 100
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP

        top_repos = []
        response_json = response.json()
        if "items" in response_json:
            for idx, repo_data in enumerate(response_json["items"], start=1):
                repo = Repo(
                    repo=repo_data.get("full_name", ""),
                    owner=repo_data.get("owner", {}).get("login", ""),
                    position_cur=idx,
                    position_prev=get_previous_position(repo_data.get(
                        "full_name", "")),
                    stars=repo_data.get("stargazers_count", 0),
                    watchers=repo_data.get("watchers_count", 0),
                    forks=repo_data.get("forks_count", 0),
                    open_issues=repo_data.get("open_issues_count", 0),
                    language=repo_data.get("language", "") or ""
                )
                top_repos.append(repo)

            update_cache(top_repos)

            return top_repos
        else:
            return {"error": "Response does not contain 'items' key"}, 500
    except requests.RequestException as e:
        return {"error": f"Failed to fetch top 100 repos from GitHub API:"
                         f" {e}"}, 500


def get_previous_position(repo_name: str) -> int:
    """Получает предыдущую позицию репозитория в топе."""

    prev_top = cache.get("prev_top")
    if prev_top:
        for repo in prev_top:
            if repo.repo == repo_name:
                return repo.position_cur
    return 0


def update_cache(top_repos):
    """Обновляет кэш с текущим топом репозиториев."""

    cache["prev_top"] = top_repos


@app.get("/api/v1/repos/{owner}/{repo}/activity")
def get_repo_activity(owner: str = Path(...), repo: str = Path(...)):
    """
    Информация об активности репозитория по коммитам за выбранный промежуток
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP

        activity_data = response.json()

        if (activity_data and isinstance(activity_data, list)
                and len(activity_data) > 0):
            activity = Activity(
                date=str(activity_data[0].get("weeks")[0].get("w", "")
                         ) if activity_data else "",
                commits=sum(sum(week.get("c", 0) for week in c.get("weeks")
                                ) for c in activity_data),
                authors=[c.get("author", {}).get(
                    "login", "") for c in activity_data]
            )

            return activity
        else:
            return {"error": "No activity data found for the repository"}, 404
    except requests.RequestException as e:
        return {
            "error": f"Failed to fetch activity for {owner}/{repo} "
                     f"from GitHub API: {e}"
        }, 500
