#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch a Raspberry PI OS image with Docker and QEMU, run a couple of
benchmarks, and close it.

This script requires a Pi OS image with autologin enabled.
"""
import os
import sys
import uuid
import argparse

import pexpect


DOCKER_IMAGE = "ghcr.io/carlosperate/dockerpi-vm:local"
PI_VERSION = "pi1"

RPI_OS_USERNAME = "pi"
RPI_OS_PASSWORD = "raspberry"

BASH_PROMPT = "{}@raspberrypi:~$ ".format(RPI_OS_USERNAME)


def launch_docker_spawn(docker_img, img_path, pi_version):
    """Runs the provided Raspberry Pi OS Lite image in QEMU inside a Docker
    container and returns a child process to run commands inside it.

    :param img_path: Path to the Raspberry Pi OS Lite image to update.
    """
    img_path = os.path.abspath(img_path)
    if not os.path.isfile(img_path):
        raise Exception("Provided OS file cannot be found: {}".format(img_path))
    if not img_path.endswith(".img"):
        raise Exception("Provided OS .img file does not have the right extension: {}".format(img_path))

    docker_container_name = "rpi-os-{}".format(str(uuid.uuid4())[:8])
    docker_cmd = " ".join([
        "docker",
        "run",
        "-it",
        "--rm",
        "--name {}".format(docker_container_name),
        # "-p 5022:5022",
        "-v {}:/sdcard/filesystem.img".format(img_path),
        docker_img,
        pi_version,
    ])
    print("Docker cmd: {}".format(docker_cmd))

    child = pexpect.spawn(docker_cmd, timeout=600, encoding='utf-8')
    child.logfile = sys.stdout

    return child, docker_container_name


def close_container(child, docker_container_name):
    try:
        print('! Attempting to close process.')
        child.close()
        print("! Exit status: {}".format(child.exitstatus))
        print("! Signal status: {}".format(child.signalstatus))
    finally:
        print('! Check if {} container is still running'.format(docker_container_name))
        container_id = pexpect.run(
            'docker ps --filter "name={}" -q'.format(docker_container_name),
        )
        print(container_id)
        if container_id:
            print('! Stopping {} container'.format(docker_container_name))
            cmd_op, exit_status  = pexpect.run(
                'docker stop {}'.format(docker_container_name), withexitstatus=True,
            )
            print("{}\n! Exit status: {}".format(cmd_op, exit_status))
        else:
            print('! Docker container was already stopped ✅')


def run(docker_img, img_path, pi_version):
    print("Staring Raspberry Pi OS container with img: {}".format(img_path))

    child, docker_container_name = None, None
    try:
        child, docker_container_name = launch_docker_spawn(docker_img, img_path, pi_version)
        child.expect_exact(BASH_PROMPT)

        # System info
        child.sendline("uname -a")
        child.expect_exact(BASH_PROMPT)
        child.sendline("cat /etc/os-release | head -n 1")
        child.expect_exact(BASH_PROMPT)
        child.sendline("cat /proc/cpuinfo")
        child.expect_exact(BASH_PROMPT)

        # Benchmarks
        child.sendline("sudo apt update -qq")
        child.expect_exact(BASH_PROMPT)
        child.sendline("sudo apt install -y speedtest-cli sysbench")
        child.expect_exact(BASH_PROMPT)
        child.sendline("speedtest-cli --secure")
        child.expect_exact(BASH_PROMPT)
        child.sendline("# CPU test - 1 thread")
        child.expect_exact(BASH_PROMPT)
        child.sendline("sysbench --num-threads=1 --validate=on --test=cpu --cpu-max-prime=1000 run")
        child.expect_exact(BASH_PROMPT)
        child.sendline("# CPU test - 4 thread")
        child.expect_exact(BASH_PROMPT)
        child.sendline("sysbench --num-threads=4 --validate=on --test=cpu --cpu-max-prime=1000 run")
        child.expect_exact(BASH_PROMPT)
        child.sendline("# Disk test - Write")
        child.expect_exact(BASH_PROMPT)
        child.sendline("rm -f ~/test.tmp && sync && dd if=/dev/zero of=~/test.tmp bs=1M count=256 conv=fsync")
        child.expect_exact(BASH_PROMPT)
        child.sendline("# Disk test - Read")
        child.expect_exact(BASH_PROMPT)
        child.sendline("sync && dd if=~/test.tmp of=/dev/null bs=1M && rm -f ~/test.tmp")
        child.expect_exact(BASH_PROMPT)

        # We are done, let's exit
        child.sendline("sudo shutdown now")
        child.expect(pexpect.EOF)
        child.wait()
    # Let ay exceptions bubble up, but ensure clean-up is run
    finally:
        if child:
            close_container(child, docker_container_name)


def main():
    parser = argparse.ArgumentParser(description="Launch and shutdown a Raspberry Pi OS image with Docker and QEMU.")
    parser.add_argument("os_img", type=str, help="Path to the Raspberry Pi OS Lite image .img file")
    parser.add_argument("-d", "--docker-img", type=str, default=DOCKER_IMAGE, help="(Optional) Docker image to use")
    parser.add_argument("-p", "--pi-version", type=str, default=PI_VERSION, help="(Optional) Raspberry Pi version (pi1, pi2, pi3)")
    args = parser.parse_args()

    if args.pi_version not in ("pi1", "pi2", "pi3", "pivirt"):
        raise Exception("Invalid Raspberry Pi version provided: {}".format(args.pi_version))

    run(args.docker_img, args.os_img, args.pi_version)

    return 0


if __name__ == "__main__":
    exit(main())
