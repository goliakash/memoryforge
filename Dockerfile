FROM python:3.13-slim

WORKDIR /app

# Install security updates
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 8000

ENV HOST=0.0.0.0
ENV PORT=8000

CMD ["python", "main.py", "server"]
