FROM python:3.11-slim

# Pracovní adresář uvnitř kontejneru
WORKDIR /app

# Nejprve requirements, ať se cacheuje instalace závislostí
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Zbytek projektu
COPY . .

# Aplikace poběží na portu 5000
EXPOSE 5000

# Start aplikace
CMD ["python", "app.py"]