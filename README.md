# Docker Raspberry Pi OS QEMU

Docker images with Raspberry Pi OS for armhf running on QEMU.

These images are built on top of the fantastic
[dockerpi](https://github.com/lukechilds/dockerpi) project, all credit for
the hard work goes to them. The main difference in this version is that the
[Raspbian OS Lite image used](https://github.com/carlosperate/rpi-os-custom-image)
has been updated to enable autologin.

Automatic login makes these images useful for things like running automated
tests on CI.

## Use these images

```
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:buster-latest
```

### Other images

```
docker run -it ghcr.io/carlosperate/rpi-os-lite:stretch-latest
```

```
docker run -it ghcr.io/carlosperate/rpi-os-lite:buster-latest
```

## Build and run this docker image from the repository

```
docker build -t carlosperate/qemu-rpi-os .
```

```
docker run -it carlosperate/qemu-rpi-os
```
