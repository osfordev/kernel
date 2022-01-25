#!/bin/bash
#

set -e

source "/usr/local/bin/docker-entrypoint-kernel.include"


export_builtin_variables

cd /usr/src/linux
KERNEL_SLUG=$(basename $(pwd -LP) | cut -d- -f2-)

case "$1" in
	configure)
		configure_kernel
		exit $?
		;;
	compile)
		build_kernel
		exit $?
		;;
	*)
		echo >&2
		if [ -n "$*" ]; then
			echo "[ERROR] Unknown quick command: $*" >&2
			exit 127
		fi
		cat /BANNER >&2
		echo >&2
		echo -n "KERNEL_VERSION: " >&2
		cat /KERNEL_VERSION | head -n 1 >&2
		echo -n "DOCKER_ARCH: " >&2
		cat /DOCKER_ARCH | head -n 1 >&2
		echo >&2
		echo "Available quick commands: 'configure', 'compile'" >&2
		echo >&2
		echo >&2
		cat <<EOF >&2
# Quick Start

## Configure Kernel
docker run --rm --interactive --tty \\
  --mount type=bind,source="\${PWD}",target=/data/build \\
  --volume "osfordev-kernel-cache":/data/cache \\
  ghcr.io/osfordev/kernel \\
    configure

## Make Kernel
docker run --rm --interactive --tty \\
  --mount type=bind,source="\${PWD}",target=/data/build \\
  --volume "osfordev-kernel-cache":/data/cache \\
  ghcr.io/osfordev/kernel \\
    compile

EOF
		echo >&2
		exit 1
		;;
esac
