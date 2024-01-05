# Using a fork of the https://github.com/lukechilds/dockerpi vm with multiple
# improvements and fixes.
FROM ghcr.io/carlosperate/qemu-rpi-vm:2024-01-03

LABEL org.opencontainers.image.authors="Carlos Pereira Atencio <carlosperate@embeddedlog.com>"
LABEL org.opencontainers.image.description="Docker image with Raspberry Pi OS running on QEMU."
LABEL org.opencontainers.image.source="https://github.com/carlosperate/docker-qemu-rpi-os"

# Select the GitHub tag from the release that hosts the OS files
# https://github.com/carlosperate/rpi-os-custom-image/releases/
ARG GH_TAG="buster-legacy-2023-05-03"

# To build a different image type from the release the FILE_SUFFIX variable
# can be overwritten with the `docker build --build-arg` flag
ARG FILE_SUFFIX="autologin-ssh-expanded"

# This only needs to be changed if the releases filename format changes
ARG FILE_PREXIF="raspberry-pi-os-lite-"${GH_TAG}"-"

ARG FILESYSTEM_IMAGE_URL="https://github.com/carlosperate/rpi-os-custom-image/releases/download/"${GH_TAG}"/"${FILE_PREXIF}${FILE_SUFFIX}".zip"
ADD $FILESYSTEM_IMAGE_URL /filesystem.zip

# entrypoint.sh has been added in the parent lukechilds/dockerpi:vm
ENTRYPOINT ["/entrypoint.sh"]
