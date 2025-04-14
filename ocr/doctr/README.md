# docTR

This folder stores some developments related to docTR

## API

There is python script which creates API via FastAPI

This API gets a picture, recognizes text in it using docTR and returns structured result

## Docker

Also there is a Dockerfile for buildind a container with the API

To build the container use:

```shell
docker build -t <name_of_image> .
```

To run the app use:

```shell
docker run -d --name <name_of_container> -p 8000:8000 <name_of_image>
```

* Flag '-d' means running in background
* Flag '-p' sets a port where container listens

Now app should be running on <http://127.0.0.1:8000>

You can use curl to send image:

```shell
curl -X POST -F "file=@/path/to/image" http://127.0.0.1:8000/uploadfile/
```
