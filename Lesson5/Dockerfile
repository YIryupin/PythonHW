# Используем официальный минимальный образ Ubuntu 
FROM ubuntu:latest 
 
# Устанавливаем переменную, чтобы избежать интерактивных вопросов 
ENV DEBIAN_FRONTEND=noninteractive 
 
# Обновляем пакеты 
RUN apt update 
 
# Устанавливаем Python, pip и venv 
RUN apt install -y python3 python3-pip python3-venv 
 
# Удаляем кэшированные списки пакетов APT 
RUN rm -rf /var/lib/apt/lists/* 
# Создаём рабочую директорию 
WORKDIR /app 
# Создаём виртуальное окружение 
RUN python3 -m venv .venv 
# Устанавливаем библиотеку aiogram в виртуальное окружение 
RUN .venv/bin/pip install aiogram 
# Устанавливаем библиотеку dotenv в виртуальное окружение 
RUN .venv/bin/pip install dotenv 
# Копируем файлы проекта в контейнер 
COPY . /app 
# Запускаем проект с использованием виртуального окружения 
CMD [".venv/bin/python3", "MyFirstGameBot.py"]