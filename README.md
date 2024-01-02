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
has been updated to enable auto-login, SSH, and expand their filesystem size.

These changes make these images useful for things like running automated
tests on CI, e.g. GitHub Actions.

## How to use these images

The main image produced in this repository can be run with this command:

```bash
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:bullseye-latest
```

This will drop you into a bash session inside Raspberry Pi OS.

### SSH

You can also launch an image with port forwarding and access it via SSH:

```bash
docker run -it -p 5022:5022 ghcr.io/carlosperate/qemu-rpi-os-lite:bullseye-latest
```

- SSH port: `5022`
- SSH username: `pi`
- SSH password: `raspberry`

## Available Images

There are two main releases right now `buster-latest` and
`bullseye-latest`:

```
ghcr.io/carlosperate/qemu-rpi-os-lite:bullseye-latest
```

```
ghcr.io/carlosperate/qemu-rpi-os-lite:buster-latest
```

Each Pi OS release has its own tag, including the OS release date in this
format:

```
ghcr.io/carlosperate/qemu-rpi-os-lite:buster-yyyy-mm-dd
```

There also is an additional tag on each release with the postfix `mu` in the
tag name, which is an specialised image created specifically to include the
[Mu Editor](https://github.com/mu-editor/mu) dependencies pre-installed,
which is used for CI tests on that project:

```
ghcr.io/carlosperate/qemu-rpi-os-lite:buster-yyyy-mm-dd-mu
```

All images can be found here:
https://github.com/carlosperate/docker-qemu-rpi-os/pkgs/container/qemu-rpi-os-lite

### Releases

Each OS release is tracked and customised via the
[Raspberry Pi OS Custom Image](https://github.com/carlosperate/rpi-os-custom-image)
repository, which then hosts the custom images in its
[releases page](https://github.com/carlosperate/rpi-os-custom-image/releases).

### Older OS versions

Older versions of Raspbian/Raspberry Pi OS have been tagged and published:

```bash
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:jessie-latest
```

```bash
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:stretch-latest
```

## Build and run this docker image from the repository

This information can be found in the [dev-docs.md](dev-docs.md) file.
