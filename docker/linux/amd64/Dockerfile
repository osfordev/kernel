# https://hub.docker.com/r/zxteamorg/gentoo-sources-bundle
ARG KERNEL_VERSION=


# Target container with Gentoo Linux + necessary tools to build kernel and initramfs
FROM --platform=amd64 zxteamorg/gentoo-sources-bundle:${KERNEL_VERSION} as stage
COPY docker/linux/docker-entrypoint-kernel.include /stage/usr/local/bin/docker-entrypoint-kernel.include
COPY docker/linux/docker-entrypoint-kernel.sh      /stage/usr/local/bin/docker-entrypoint-kernel.sh
COPY docker/linux/docker-build-sites-copier.sh     /build/docker/docker-build-sites-copier.sh
COPY sites                                         /build/sites
# Filter sites
RUN /build/docker/docker-build-sites-copier.sh /build/sites /stage/support/sites/
# We need intel-microcode and linux-firmware to bundle microcode. See more https://wiki.gentoo.org/wiki/Microcode
RUN emerge-webrsync
RUN \
  ACCEPT_LICENSE="intel-ucode linux-fw-redistributable no-source-code" \
  FEATURES="-ipc-sandbox -network-sandbox -pid-sandbox -sandbox -usersandbox" \
  emerge --quiet --oneshot \
    sys-apps/iucode_tool
RUN \
  ACCEPT_LICENSE="intel-ucode linux-fw-redistributable no-source-code" \
  FEATURES="-ipc-sandbox -network-sandbox -pid-sandbox -sandbox -usersandbox" \
  ROOT=/stage \
  KERNEL_DIR=/usr/src/linux \
  emerge --quiet --oneshot --nodeps \
    sys-firmware/intel-microcode \
    sys-kernel/linux-firmware
# Cleanup
RUN \
  rm -rf /stage/etc/env.d; \
  rm -rf /stage/etc/environment.d; \
  rm -rf /stage/var/lib/gentoo; \
  rm -rf /stage/var/lib/portage; \
  rm -rf /stage/var/tmp; \
  rm -rf /stage/var/cache


FROM --platform=amd64 zxteamorg/gentoo-sources-bundle:${KERNEL_VERSION}
COPY --from=stage /stage /
VOLUME [ "/data/build", "/data/cache" ]
ENV SITE=
ENTRYPOINT [ "/usr/local/bin/docker-entrypoint-kernel.sh" ]
