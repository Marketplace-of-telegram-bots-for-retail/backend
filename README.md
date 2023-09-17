# Backend of Marketplace telegram bots for retail TEST
Backend of Marketplace telegram bots for retail

  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
  ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) 
  ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
  ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
  ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
  ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)


### Локальный запуск для разработки на linux

  - клонируем develop
  - cd backend где docker-compose_copy.yml
  - можно проверить версию python желательно 3.10.12 но в принципе скорее всего и так все будет работать
  - python3 -m venv venv
  - pip install -m backend/requirements.txt
  - проверьте что от прошлых проектов не осталось запущенных контейнеров, которые занимают наши порты и хосты
  - sudo docker ps -a
  - sudo docker compose -f docker-compose_copy.yml up -d # это поднимет postgres, проверить что docker-compose_copy.yml и .env в гитигноре и удалены из      индекса они не должны пушиться
  - python manage.py makemigrations ### Предлагаю не пушить миграции до момента пока все модели не будут готовы, migrations в .gitignor
  - python manage.py migrate
  - python manage.py createsuperuser
  - python manage.py runserver
  - остановка базы
  - sudo docker compose -f docker-compose_copy.yml down
  
 
  