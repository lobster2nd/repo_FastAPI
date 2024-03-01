# Анализ репозиториев GitHub  

Отображение топ 100 публичных репозиториев и информацию об активности выбранного репозитория по коммитам  

## Стек технологий  

<img src="https://img.shields.io/badge/Python - black?style=for-the-badge&logo=Python&logoColor=blue"/> <img src="https://img.shields.io/badge/fastapi - black?style=for-the-badge&logo=fastapi&logoColor=white"/> <img src="https://img.shields.io/badge/pydantic - black?style=for-the-badge&logo=pydantic&logoColor=white"/>  <img src="https://img.shields.io/badge/docker - black?style=for-the-badge&logo=docker&logoColor=blue"/>  

## Установка и запуск проекта локально (Linux)  
+ Склонировать репозиторий и перейти в него в командной строке:  
```
git clone https://github.com/lobster2nd/repo_FastAPI.git  
cd repo_FastAPI  
```
+ Запустить проект в контейнере
```
sudo docker-compose up --build
```
Сервис будет доступен локально по адресу http://0.0.0.0:8000/  

### Эндпоинты:  

+ Отображение топ 100 публичных репозиториев. Топ составляется по количеству звезд.  
```
curl http://0.0.0.0:8000/api/v1/repos/top100/
```
Схема (список объектов):  
repo: string – название репозитория (full_name в API GitHub)  
owner: string - владелец репозитория  
position_cur: integer – текущая позиция в топе  
position_prev: integer – предыдущая позиция в топе  
stars: integer – количество звёзд  
watchers: integers – количество просмотров  
forks: integer – количество форков  
open_issues: integer – количество открытых issues  
language: string - язык 

+ Информация об активности выбранного репозитория по коммитам.  
Заменить {owner} на имя владельца репозитория, {repo} - на название репозитория  
```
curl http://0.0.0.0:8000/api/v1/repos/{owner}/{repo}/activity
```
Схема (список объектов):  
date: date  
commits: int – количество коммитов за конкретный день  
authors: list[string] – список разработчиков, которые выполняли коммиты  

