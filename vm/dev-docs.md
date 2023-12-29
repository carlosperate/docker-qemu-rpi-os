# Dev docs

## Create image

```
docker build -t ghcr.io/carlosperate/dockerpi-vm:local .
```

## Run container pointing to Pi OS image file

```
docker run --rm -v full_path_to.img:/sdcard/filesystem.img -p 5022:5022 ghcr.io/carlosperate/dockerpi-vm:local
```

## Push image to GH Container Registry

```
docker login ghcr.io -u <your_username>
```
```
docker tag IMAGE_ID ghcr.io/carlosperate/dockerpi-vm:VERSION
```
```
docker push ghcr.io/carlosperate/dockerpi-vm:VERSION
```
