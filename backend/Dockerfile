FROM python:3.12.4

WORKDIR /app

COPY req.txt . /app

RUN pip install -r req.txt

EXPOSE 8000

CMD ["gunicorn", "src.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]