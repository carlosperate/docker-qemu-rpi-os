# Docker Raspberry Pi OS for Arm Virtualised with QEMU

Docker images with a QEMU virtual machine emulating ARMv6 and running
Raspberry Pi OS (formerly Raspbian) for the armhf architecture.

Oversimplified diagram:

```
+-------------------------------+
|                               |
|  Docker Container             |
|                               |
|  +-------------------------+  |
|  |                         |  |
|  |  Raspberry Pi OS        |  |
|  |                         |  |
|  +-------------------------+  |
|  |                         |  |
|  |  QEMU Emulating ARMv6   |  |
|  |                         |  |
|  +-------------------------+  |
|                               |
+-------------------------------+
|                               |
|  PC Host OS                   |
|                               |
+-------------------------------+
```

These Docker images are built on top of the fantastic
[dockerpi](https://github.com/lukechilds/dockerpi) project, all credit for
the hard work goes to them. The main difference in this version is that the
[Raspberry Pi OS Lite image used](https://github.com/carlosperate/rpi-os-custom-image)
has been updated to enable autologin and ssh.

These changes make these images useful for things like running automated
tests on CI, like GitHub Actions.

## How to use these images

The main image produced in this repository can be run with this command:

```
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:buster-latest
```

## Other images

Older versions of Raspbian/Raspberry Pi OS:

```
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:jessie-latest
```

```
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:stretch-latest
```

```
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:buster-latest
```


## Build and run this docker image from the repository

```
docker build -t carlosperate/qemu-rpi-os-lite .
```

```
docker run -it carlosperate/qemu-rpi-os-lite
```
