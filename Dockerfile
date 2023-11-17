FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1

RUN useradd -m -r -u 100 user

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R user:user /app

USER user

CMD [ "bash", "-c" "python filling_database.py && python server.py" ]