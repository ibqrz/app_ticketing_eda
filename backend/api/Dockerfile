FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY common/requirements.txt common-requirements.txt
COPY api/requirements.txt api-requirements.txt
RUN pip install --no-cache-dir -r common-requirements.txt -r api-requirements.txt

COPY common ./common
COPY api/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
