FROM ghcr.io/mindee/doctr:torch-viz-html-contrib-py3.11.8-2025-04

WORKDIR /usr/src/app
COPY . .

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "vim", "nano", "-y"]
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["fastapi", "run", "app.py" ]
CMD ["--host", "0.0.0.0", "--port", "8000"]