# Development Documentation

## `qemu-rpi-os-lite`

### Build docker image

```bash
git clone https://github.com/carlosperate/docker-qemu-rpi-os.git
```
```bash
cd docker-qemu-rpi-os
```
```bash
docker build -t carlosperate/qemu-rpi-os-lite .
```

### Run docker image

```bash
docker run -it carlosperate/qemu-rpi-os-lite
```

### Publish docker image

TBD.


## `dockerpi` Fork

The [vm](vm) folder contains a fork of the
[dockerpi](https://github.com/lukechilds/dockerpi/) project, with modifications
as listed in its [vm/README.md](vm/README.md) file.

### Build image

```bash
docker build -t ghcr.io/carlosperate/dockerpi-vm:local .
```

### Run container pointing to Pi OS image file

```bash
docker run -it --rm -v full_path_to.img:/sdcard/filesystem.img -p 5022:5022 ghcr.io/carlosperate/dockerpi-vm:local
```

### Push image to GH Container Registry

```bash
docker login ghcr.io -u <your_username>
```
```bash
docker tag IMAGE_ID ghcr.io/carlosperate/dockerpi-vm:VERSION
```
```bash
docker push ghcr.io/carlosperate/dockerpi-vm:VERSION
```
