FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .



# Start the app
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:create_app()"]
