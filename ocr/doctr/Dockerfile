FROM ghcr.io/mindee/doctr:torch-viz-html-contrib-py3.12.7-v0.11.0

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "run", "app.py", "--port", "8000"]