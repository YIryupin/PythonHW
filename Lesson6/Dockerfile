FROM python:3.12.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта в контейнер 
#COPY . /app 
# Запускаем проект с использованием виртуального окружения 
# ВНИМАНИЕ!!! Этот докер файл не включал создание VENV, очевидно это вообще избыточная вещь, 
# т.к. и так индивидуальный образ создаётся
#CMD [".venv/bin/python3", "MyFirstGameBot.py"]

# Копируем весь проект (бот, миграции, утилиты)
COPY . .
# Исправляем формат конца строки для entrypoint.sh
RUN sed -i 's/\r$//' entrypoint.sh && \
   chmod +x entrypoint.sh
RUN chmod +x entrypoint.sh
CMD ["/bin/bash", "./entrypoint.sh"]
#такой вызов работать не будет из за разнецы с символах конца строки для винды и линукса:
#CMD ["entrypoint.sh"]

#в докер файле может быть только одна деректива CMD!!! поэтому нужен entrypoint.sh
#CMD ["python", "migrate.py"]

#CMD ["python", "MyFirstGameBot.py"]
