# Base image olarak Python kullanıyoruz
FROM python:3.11-slim

# Çalışma dizinini oluştur
WORKDIR /app

# Bağımlılık dosyalarını kopyala
COPY requirements.txt .

# Bağımlılıkları kur
RUN pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . .

# Flask’ın dışarıya erişebilmesi için host'u belirt
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Uygulamayı çalıştır
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Container portunu expose et
EXPOSE 5000
