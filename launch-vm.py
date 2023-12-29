#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch a Raspberry PI OS image with Docker and QEMU, run a few commands,
and close it.

This can be used as a simple test to time startup and tear down speed
of different Raspberry Pi emulation configurations.
"""
import os
import sys
import uuid

import pexpect


DOCKER_IMAGE = "ghcr.io/carlosperate/dockerpi-vm:local2"
PI_TYPE = "pi1"
#PI_TYPE = "pi2"
#PI_TYPE = "pi3"

RPI_OS_USERNAME = "pi"
RPI_OS_PASSWORD = "raspberry"

BASH_PROMPT = "{}@raspberrypi:~$ ".format(RPI_OS_USERNAME)



def launch_docker_spawn(img_path):
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
        DOCKER_IMAGE,
        PI_TYPE
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
            print('! Docker container was already stopped.')


def run(img_path):
    print("Staring Raspberry Pi OS container with img: {}".format(img_path))

    child, docker_container_name = None, None
    try:
        child, docker_container_name = launch_docker_spawn(img_path)
        child.expect_exact(BASH_PROMPT)
        child.sendline("uname -a")
        child.expect_exact(BASH_PROMPT)
        child.sendline("cat /etc/os-release | head -n 1")
        child.expect_exact(BASH_PROMPT)
        child.sendline("cat /proc/cpuinfo")
        child.expect_exact(BASH_PROMPT)
        # child.sendline("sudo apt install -y speedtest-cli")
        # child.expect_exact(BASH_PROMPT)
        # child.sendline("speedtest-cli --secure")
        # child.expect_exact(BASH_PROMPT)
        child.sendline('python -c "import platform as p; print(p.machine(), p.architecture())"')
        child.expect_exact(BASH_PROMPT)

        # We are done, let's exit
        child.sendline("sudo shutdown now")
        child.expect(pexpect.EOF)
        child.wait()
    # Let ay exceptions bubble up, but ensure clean-up is run
    finally:
        if child:
            close_container(child, docker_container_name)


if __name__ == "__main__":
    # Hacky way to pass the first two argument as the .img path
    run(sys.argv[1])
