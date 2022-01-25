#!/bin/bash
#

#
# The script make a copy of all kernel configurations
# related to current kernel version 
# from source directory passed as first argument
# to target directory passed as second argument
#

set -e

SOURCE_DIR="${1}"
TARGET_DIR="${2}"

if [ -z "${SOURCE_DIR}" ]; then
	echo "Bad usage. Source directory should be passed by first argument." >&2
	exit 1
fi
if [ -z "${TARGET_DIR}" ]; then
	echo "Bad usage. Target directory should be passed by second argument." >&2
	exit 1
fi

mkdir --parents "${TARGET_DIR}"

KERNEL_SLUG=$(cd /usr/src/linux; basename $(pwd -LP) | cut -d- -f2-)

find "${SOURCE_DIR}" -type f -name "config-${KERNEL_SLUG}-*" -exec cp "{}" "${TARGET_DIR}" \;
