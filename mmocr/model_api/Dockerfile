# syntax=docker/dockerfile:1

FROM mmocr:1.0.1
WORKDIR /mmocr/workspace

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /mmocr/workspace/data

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]