FROM python:3.10-slim

RUN useradd -m -r -u 100 user

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R user:user /app

USER user

EXPOSE 5000

CMD ["bash", "-c", "python ./db/filling_database.py && flask run --debug -h '0.0.0.0'"]