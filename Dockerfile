# Based on the last image created the dockerpi Dockerfile
# https://github.com/lukechilds/dockerpi/blob/35b55bcd34746380e034675048391c98ef85907c/Dockerfile
# It's just the VM image with a compressed Raspbian filesystem added
FROM lukechilds/dockerpi:vm

LABEL maintainer="Carlos Pereira Atencio <carlosperate@embeddedlog.com>"

# Image created in https://github.com/carlosperate/rpi-os-custom-image/
ARG FILESYSTEM_IMAGE_URL="https://github.com/carlosperate/rpi-os-custom-image/releases/download/2017-07-05/raspberry-pi-os-lite-jessie-2017-07-05-autologin-ssh.zip"

ADD $FILESYSTEM_IMAGE_URL /filesystem.zip

# entrypoint.sh has been added in the parent lukechilds/dockerpi:vm
ENTRYPOINT ["/entrypoint.sh"]
