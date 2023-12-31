<div align="center">
	<img width="256" src="https://raw.githubusercontent.com/lukechilds/dockerpi/5f58e8b5fefde0e5d4aedd19d7c04a2ff77eb4c3/media/logo.svg">
</div>

# dockerpi Fork

This is a fork of the original
[dockerpi](https://github.com/lukechilds/dockerpi/) project, to be able to 
apply fixes and improvements, since the original upstream project hasn't been
updated in two and a half years.

List of changes:
- [GitHub view of full diff](https://github.com/carlosperate/docker-qemu-rpi-os/compare/f0f1c1dd6c2470012a6588fae08e528198203710...main#diff-11dbc6371a321f05fc4ae47aa94884866787bc1427d9b5e4a9590b4cdf7f964c)
  (only files within the `vm` folder are from `dockerpi`)
- Removed the `dockerpi` image and only kept the `vm`
    - As only the `vm` image is used by the docker-qemu-rpi-os project in the main [../Dockerfile](../Dockerfile)
    - commit [b91b284](https://github.com/carlosperate/docker-qemu-rpi-os/commit/b91b284ff848a7c265230ba5630bd7578074eec2)
- Fix build issue `xz: Cannot exec: No such file or directory`
    - Fix from upstream PR: https://github.com/lukechilds/dockerpi/pull/59
    - commit [46deb95](https://github.com/carlosperate/docker-qemu-rpi-os/commit/46deb95ca5df09be1aec482e45f304025cba802e)
- Fix build issue `Package python is not available, but is referred to by another package.`
    - Fix from upstream PR: https://github.com/lukechilds/dockerpi/pull/61
    - commit [0cca83a](https://github.com/carlosperate/docker-qemu-rpi-os/commit/0cca83af5c67a90b2ba646098496105e890346fe)
- Fix run issue uncompressing OS image zip files larger than 4GB `unzip: bad length`
    - Fix from upstream PR: https://github.com/lukechilds/dockerpi/pull/48
    - commit [1d6745d](https://github.com/carlosperate/docker-qemu-rpi-os/commit/1d6745db79c300ce6445d049760a2e01f4ee43d0)
- Updated Qemu to 8.2.0
    - commit [9837075](https://github.com/carlosperate/docker-qemu-rpi-os/commit/983707533f070b372d10d499ada7cad838fe0e16)
    - Fixes issue where Qemu for pi2/3 hangs on power down (before the container had to be manually killed)
    - Extra configure flags:
        - `--disable-gio`: https://gitlab.com/qemu-project/qemu/-/issues/1190
        - `--disable-docs`: To avoid needing the `sphinx` python dependencies
        - `--enable-slirp`: To resolve `network backend 'user' is not compiled into this binary`
          Since v7.2+ Qemu does not include the `slirp` networking lib
          Due to an issue in debian's `libslirp-dev` package, need to move image to Ubuntu 23.10
          https://stackoverflow.com/questions/75641274/network-backend-user-is-not-compiled-into-this-binary
          https://bugs.launchpad.net/ubuntu/+source/libslirp/+bug/2029431
          https://www.mail-archive.com/qemu-devel@nongnu.org/msg903610.html
    - `entrypoint.sh`: Output of `qemu-img info` now returns multiple `virtual-size` keys and only one needed
- Create an additional board type for performance reasons
    - https://github.com/carlosperate/docker-qemu-rpi-os/issues/3
    - Uses the `virt` machine type: https://www.qemu.org/docs/master/system/arm/virt.html
    - This is not an accurate Pi emulation, but has better performance and 1 GB of RAM
    - Docker image has to build the kernel, as the pi kernel does not include the required configuration
    - commit [xxxxx](https://github.com/carlosperate/docker-qemu-rpi-os/commit/xxxx)
- Added developer documentation for this fork to parent directory [../dev-docs.md](../dev-docs.md)

The rest of the original README can be seen below.

----------

> A Virtualised Raspberry Pi inside a Docker image

Gives you access to a virtualised ARM based Raspberry Pi machine running the Raspian operating system.

This is not just a Raspian Docker image, it's a full ARM based Raspberry Pi virtual machine environment.

<div align="center">
	<img src="https://raw.githubusercontent.com/lukechilds/dockerpi/5f58e8b5fefde0e5d4aedd19d7c04a2ff77eb4c3/media/demo.svg" width="720">
</div>

## Usage

```
docker run -it lukechilds/dockerpi
```

By default all filesystem changes will be lost on shutdown. You can persist filesystem changes between reboots by mounting the `/sdcard` volume on your host:

```
docker run -it -v $HOME/.dockerpi:/sdcard lukechilds/dockerpi
```

If you have a specific image you want to mount you can mount it at `/sdcard/filesystem.img`:

```
docker run -it -v /2019-09-26-raspbian-buster-lite.img:/sdcard/filesystem.img lukechilds/dockerpi
```

If you only want to mount your own image, you can download a much slimmer VM only Docker container that doesn't contain the Raspbian filesystem image:

[![Docker Image Size](https://badgen.net/docker/size/lukechilds/dockerpi/latest/amd64?icon=docker&label=lukechilds/dockerpi:latest)](https://hub.docker.com/r/lukechilds/dockerpi/tags?name=latest)
[![Docker Image Size](https://badgen.net/docker/size/lukechilds/dockerpi/vm/amd64?icon=docker&label=lukechilds/dockerpi:vm)](https://hub.docker.com/r/lukechilds/dockerpi/tags?name=vm)

```
docker run -it -v /2019-09-26-raspbian-buster-lite.img:/sdcard/filesystem.img lukechilds/dockerpi:vm
```

## Which machines are supported?

By default a Raspberry Pi 1 is virtualised, however experimental support has been added for Pi 2 and Pi 3 machines.

You can specify a machine by passing the name as a CLI argument:

```
docker run -it lukechilds/dockerpi pi1
docker run -it lukechilds/dockerpi pi2
docker run -it lukechilds/dockerpi pi3
```

> **Note:** In the Pi 2 and Pi 3 machines, QEMU hangs once the machines are powered down requiring you to `docker kill` the container. See [#4](https://github.com/lukechilds/dockerpi/pull/4) for details.


## Wait, what?

A full ARM environment is created by using Docker to bootstrap a QEMU virtual machine. The Docker QEMU process virtualises a machine with a single core ARM11 CPU and 256MB RAM, just like the Raspberry Pi. The official Raspbian image is mounted and booted along with a modified QEMU compatible kernel.

You'll see the entire boot process logged to your TTY until you're prompted to log in with the username/password pi/raspberry.

```
pi@raspberrypi:~$ uname -a
Linux raspberrypi 4.19.50+ #1 Tue Nov 26 01:49:16 CET 2019 armv6l GNU/Linux
pi@raspberrypi:~$ cat /etc/os-release | head -n 1
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
pi@raspberrypi:~$ cat /proc/cpuinfo
processor       : 0
model name      : ARMv6-compatible processor rev 7 (v6l)
BogoMIPS        : 798.31
Features        : half thumb fastmult vfp edsp java tls
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xb76
CPU revision    : 7

Hardware        : ARM-Versatile (Device Tree Support)
Revision        : 0000
Serial          : 0000000000000000
pi@raspberrypi:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:          246Mi        20Mi       181Mi       1.0Mi        44Mi       179Mi
Swap:          99Mi          0B        99Mi
```

## Build

Build this image yourself by checking out this repo, `cd` ing into it and running:

```
docker build -t lukechilds/dockerpi .
```

Build the VM only image with:

```
docker build -t lukechilds/dockerpi:vm --target dockerpi-vm .
```

## Credit

Thanks to [@dhruvvyas90](https://github.com/dhruvvyas90) for his [dhruvvyas90/qemu-rpi-kernel](https://github.com/dhruvvyas90/qemu-rpi-kernel) repo.

## License

MIT © Luke Childs
