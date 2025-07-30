FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run seed_admin script once at build/startup time
RUN python seed_admin.py || echo "⚠️ Admin seed failed or already exists"

# Start the app
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:create_app()"]
