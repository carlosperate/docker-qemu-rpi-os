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

This will drop you into a bash session inside Raspberry Pi OS.

### SSH

You can also launch an image with port forwarding and access it via SSH:

```
docker run -it -p 5022:5022 ghcr.io/carlosperate/qemu-rpi-os-lite:buster-latest
```

- SSH port: `5022`
- SSH username: `pi`
- SSH password: `raspberry`

## Available Images

The main latest image is `buster-latest`:

```
ghcr.io/carlosperate/qemu-rpi-os-lite:buster-latest
```

There are two additional versions for each release.
1) `Extended` with an extra 1GB of disk space:
    ```
    ghcr.io/carlosperate/qemu-rpi-os-lite:buster-extended-latest
    ```
2) `Mu`, an specialised image with the
  [Mu Editor](https://github.com/mu-editor/mu) dependencies pre-installed:
    ```
    ghcr.io/carlosperate/qemu-rpi-os-lite:buster-mu-latest
    ```

All images can be found here:
https://github.com/users/carlosperate/packages/container/package/qemu-rpi-os-lite

### Releases

Each OS release is tracked and customised edited via this
[Raspberry Pi OS Custom Image](https://github.com/carlosperate/rpi-os-custom-image)
repository, which then hosts the custom images in its
[releases page](https://github.com/carlosperate/rpi-os-custom-image/releases).

### Older OS versions

Older versions of Raspbian/Raspberry Pi OS have been tagged and published:

```
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:jessie-latest
```

```
docker run -it ghcr.io/carlosperate/qemu-rpi-os-lite:stretch-latest
```

## Build and run this docker image from the repository

```
git clone https://github.com/carlosperate/docker-qemu-rpi-os.git
```

```
cd docker-qemu-rpi-os
```

``` 
docker build -t carlosperate/qemu-rpi-os-lite .
```

```
docker run -it carlosperate/qemu-rpi-os-lite
```
