# Based on the last image created the dockerpi Dockerfile
# https://github.com/lukechilds/dockerpi/blob/35b55bcd34746380e034675048391c98ef85907c/Dockerfile
# It's just the VM image with a compressed Raspbian filesystem added
FROM lukechilds/dockerpi:vm

ARG FILESYSTEM_IMAGE_URL="https://github.com/carlosperate/rpi-os-custom-image/releases/download/v2020-08-24/2020-08-20-raspios-buster-armhf-lite-autologin.img.zip"

ADD $FILESYSTEM_IMAGE_URL /filesystem.zip

# entrypoint.sh has been added in the parent lukechilds/dockerpi:vm
# Included here to ensure CI services like GH Actions
ENTRYPOINT ["/entrypoint.sh"]
