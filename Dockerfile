FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y git-lfs
RUN git lfs install
RUN git lfs pull

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]