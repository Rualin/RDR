FROM ghcr.io/mindee/doctr:torch-viz-html-contrib-py3.12.7-v0.11.0

WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app/weights
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["fastapi", "run", "app.py" ]
CMD ["--host", "0.0.0.0", "--port", "8000"]