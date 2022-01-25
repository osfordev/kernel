#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import filecmp
import os
import sys

def is_equals_files_content(left_file: str, right_file: str) -> bool:
	return filecmp.cmp(left_file, right_file)

def format_kernel_to_build_item(site: str, kernel_version: str, gentoo_arch: str, docker_platform: str) -> str:
	'''
	Format build item: <site>:<kernel_version>:<gentoo_arch>:<docker_platform>
	'''
	return "%s:%s:%s:%s" % (site, kernel_version, gentoo_arch, docker_platform)

def parse_kernel_version_from_config_file_name(config_file_name: str) -> str:
	parts = config_file_name.split("-")
	parts_len = len(parts);
	if parts_len == 4:
		return parts[1]
	elif parts_len == 5:
		return "%s-%s" % (parts[1], parts[3])
	else:
		raise Exception("Cannot parse kernel version from name '%s'" % config_file_name)

def translate_gentoo_arch_to_docker_platform(gentoo_arch: str) -> str:
	if gentoo_arch == "amd64":
		return "linux/amd64"
	elif gentoo_arch == "x86":
		return "linux/386"
	elif gentoo_arch == "arm32v5":
		return "linux/arm32/v5"
	elif gentoo_arch == "arm32v6":
		return "linux/arm32/v6"
	elif gentoo_arch == "arm32v7":
		return "linux/arm32/v7"
	elif gentoo_arch == "arm64v8":
		return "linux/arm64/v8"
	else:
		raise Exception("Cannot translate Gentoo arch '%s' into Docker platform" % gentoo_arch)

def main() -> int:
	sites_directory = sys.argv[1]
	binaries_directory = sys.argv[2]

	kernels_to_build: list[str] = []

	for site in os.listdir(sites_directory):
		site_directory = os.path.join(sites_directory, site)
		if not os.path.isdir(site_directory):
			continue
		for gentoo_arch in os.listdir(site_directory):
			arch_directory = os.path.join(site_directory, gentoo_arch)
			if not os.path.isdir(arch_directory):
				continue
			for config_file_name in os.listdir(arch_directory):
				config_file_path = os.path.join(arch_directory, config_file_name)
				if not os.path.isfile(config_file_path):
					continue
	
				kernel_version = parse_kernel_version_from_config_file_name(config_file_name)
				docker_platform = translate_gentoo_arch_to_docker_platform(gentoo_arch)
	
				binary_config_file_path = os.path.join(binaries_directory, site, gentoo_arch, config_file_name)
				if not os.path.isfile(binary_config_file_path):
					# binary_config_file_path is not exists (or not file), so we have to build this kernel version
					kernel_to_build = format_kernel_to_build_item(site, kernel_version, gentoo_arch, docker_platform)
					kernels_to_build.append(kernel_to_build)
				else:
					# so, binary_config_file_path is exist, try to compare it with configuration item
					if not is_equals_files_content(config_file_path, binary_config_file_path):
						# config in sites is differ to binary version. We have to rebuild this kernel version
						kernel_to_build = format_kernel_to_build_item(site, kernel_version, gentoo_arch, docker_platform)
						kernels_to_build.append(kernel_to_build)

	print("::set-output name=kernels_to_build::%s" % json.dumps(kernels_to_build))

	return 0

if __name__ == '__main__':
    sys.exit(main())
