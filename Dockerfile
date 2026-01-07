FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install fastapi uvicorn pydantic sqlalchemy python-dotenv httpx email-validator pydantic-settings

COPY . .

RUN python init_db.py

EXPOSE 8080

CMD ["python", "-m", "app.main"]