FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY Task2/task2a.py Task2/utils.py ./
COPY Task3/task2a_runner.py ./
ENTRYPOINT ["python", "task2a_runner.py"]
