# Based on the last image created the dockerpi Dockerfile
# https://github.com/lukechilds/dockerpi/blob/6c1ac8edab988dca8bb36dddc5388e8c4123c824/Dockerfile
# It's just the VM image with a compressed Raspbian filesystem added
FROM lukechilds/dockerpi:vm

LABEL maintainer="Carlos Pereira Atencio <carlosperate@embeddedlog.com>"

# Select the GitHub tag from the release that hosts the OS files
# https://github.com/carlosperate/rpi-os-custom-image/releases/
ARG GH_TAG="2021-05-28"

# To build a different image type from the release the FILE_SUFFIX variable
# can be overwritten with the `docker build --build-arg` flag
ARG FILE_SUFFIX="autologin-ssh-expanded"

# This only needs to be changed if the releases filename format changes
ARG FILE_PREXIF="raspberry-pi-os-lite-buster-"${GH_TAG}"-"

ARG FILESYSTEM_IMAGE_URL="https://github.com/carlosperate/rpi-os-custom-image/releases/download/"${GH_TAG}"/"${FILE_PREXIF}${FILE_SUFFIX}".zip"
ADD $FILESYSTEM_IMAGE_URL /filesystem.zip

# entrypoint.sh has been added in the parent lukechilds/dockerpi:vm
ENTRYPOINT ["/entrypoint.sh"]
