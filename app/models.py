from typing import List

from pydantic import BaseModel


class Repo(BaseModel):
    """Модель данных для репозитория."""

    repo: str
    owner: str
    position_cur: int
    position_prev: int
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str


class Activity(BaseModel):
    """Модель данных для активности репозитория."""

    date: str
    commits: int
    authors: List[str]
