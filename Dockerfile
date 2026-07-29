FROM python:3.12.3-slim

# Set environment variables to optimize Python performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /AuthServer
# Install dependencies first (to leverage Docker cache)[whatever frequently chnages will be pushed last]
COPY requirements.txt /AuthServer/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /AuthServer/

WORKDIR /AuthServer/auth_server
# Expose container port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
