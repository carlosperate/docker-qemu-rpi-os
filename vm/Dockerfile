# Build stage for qemu-system-arm
FROM ubuntu:23.10 AS qemu-builder
ARG QEMU_VERSION=8.2.0
ENV QEMU_TARBALL="qemu-${QEMU_VERSION}.tar.xz"
WORKDIR /qemu

RUN # Update package lists
RUN apt-get update

RUN # Pull source
RUN apt-get -y install wget
RUN wget "https://download.qemu.org/${QEMU_TARBALL}"

RUN # Verify signatures
RUN apt-get -y install gpg
RUN wget "https://download.qemu.org/${QEMU_TARBALL}.sig"
RUN gpg --keyserver keyserver.ubuntu.com --recv-keys CEACC9E15534EBABB82D3FA03353C9CEF108B584
RUN gpg --verify "${QEMU_TARBALL}.sig" "${QEMU_TARBALL}"

RUN # Extract source tarball
RUN apt-get -y install pkg-config xz-utils
RUN tar xvf "${QEMU_TARBALL}"

RUN # Build source
# These seem to be the only deps actually required for a successful  build
RUN apt-get -y install python3 python3-venv build-essential libslirp-dev libglib2.0-dev libpixman-1-dev ninja-build
# These don't seem to be required but are specified here: https://wiki.qemu.org/Hosts/Linux
RUN apt-get -y install libfdt-dev zlib1g-dev
# Not required or specified anywhere but supress build warnings
RUN apt-get -y install flex bison
WORKDIR /qemu/qemu-${QEMU_VERSION}
RUN ./configure --static --target-list=arm-softmmu,aarch64-softmmu --enable-slirp --disable-gio --disable-docs
RUN make -j$(nproc)

RUN # Strip the binary, this gives a substantial size reduction!
RUN cp -r /qemu/qemu-${QEMU_VERSION}/build /qemu/build
WORKDIR /qemu/build
RUN strip "arm-softmmu/qemu-system-arm" "aarch64-softmmu/qemu-system-aarch64" "qemu-img"


# Build stage for fatcat
FROM debian:stable-slim AS fatcat-builder
ARG FATCAT_VERSION=v1.1.0
ARG FATCAT_CHECKSUM="303efe2aa73cbfe6fbc5d8af346d0f2c70b3f996fc891e8859213a58b95ad88c"
ENV FATCAT_TARBALL="${FATCAT_VERSION}.tar.gz"
WORKDIR /fatcat

RUN # Update package lists
RUN apt-get update

RUN # Pull source
RUN apt-get -y install wget
RUN wget "https://github.com/Gregwar/fatcat/archive/${FATCAT_TARBALL}"
RUN echo "${FATCAT_CHECKSUM} ${FATCAT_TARBALL}" | sha256sum --check

RUN # Extract source tarball
RUN tar xvf "${FATCAT_TARBALL}"

RUN # Build source
RUN apt-get -y install build-essential cmake
RUN cmake fatcat-* -DCMAKE_CXX_FLAGS='-static'
RUN make -j$(nproc)


# Build the dockerpi VM image
FROM busybox:1.36 AS dockerpi-vm
LABEL maintainer="Luke Childs <lukechilds123@gmail.com>"
ARG RPI_KERNEL_URL="https://github.com/dhruvvyas90/qemu-rpi-kernel/archive/afe411f2c9b04730bcc6b2168cdc9adca224227c.zip"
ARG RPI_KERNEL_CHECKSUM="295a22f1cd49ab51b9e7192103ee7c917624b063cc5ca2e11434164638aad5f4"

COPY --from=qemu-builder /qemu/build/arm-softmmu/qemu-system-arm /usr/local/bin/qemu-system-arm
COPY --from=qemu-builder /qemu/build/aarch64-softmmu/qemu-system-aarch64 /usr/local/bin/qemu-system-aarch64
COPY --from=qemu-builder /qemu/build/qemu-img /usr/local/bin/qemu-img
COPY --from=fatcat-builder /fatcat/fatcat /usr/local/bin/fatcat

ADD $RPI_KERNEL_URL /tmp/qemu-rpi-kernel.zip

RUN cd /tmp && \
    echo "$RPI_KERNEL_CHECKSUM  qemu-rpi-kernel.zip" | sha256sum -c && \
    unzip qemu-rpi-kernel.zip && \
    mkdir -p /root/qemu-rpi-kernel && \
    cp qemu-rpi-kernel-*/kernel-qemu-4.19.50-buster /root/qemu-rpi-kernel/ && \
    cp qemu-rpi-kernel-*/versatile-pb.dtb /root/qemu-rpi-kernel/ && \
    rm -rf /tmp/*

VOLUME /sdcard

ADD ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]