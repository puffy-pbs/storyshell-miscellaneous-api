FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

RUN apt-get update && apt-get install libreoffice imagemagick ffmpeg -y

RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml

COPY . .

EXPOSE 5000/tcp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]