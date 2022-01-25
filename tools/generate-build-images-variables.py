#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys

def format_build_item(kernel_version: str, gentoo_arch: str, docker_platform: str) -> str:
	'''
	Format build item: <kernel_version>:<gentoo_arch>:<docker_platform>
	'''
	return "%s:%s:%s" % (kernel_version, gentoo_arch, docker_platform)

def format_manifest_item(kernel_version: str, docker_platforms: list[str]):
	'''
	Format manifest item: <kernel_version>:<docker_platform_1>,<docker_platform_2>,...,<docker_platform_N>
	'''
	comma_docker_platforms = ",".join(docker_platforms)
	return "%s:%s" % (kernel_version, comma_docker_platforms)

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

	target_versions: dict[str,list[str]] = {}
	latest_sites_kernel: dict[str, str] = {}

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
				if kernel_version not in target_versions:
					target_versions[kernel_version] = []
				target_archs = target_versions[kernel_version]
				if gentoo_arch not in target_archs:
					target_archs.append(gentoo_arch)
				if kernel_version not in latest_sites_kernel:
					latest_sites_kernel[kernel_version] = kernel_version
				else:
					latest_sites_kernel[kernel_version] = max(latest_sites_kernel[kernel_version], kernel_version)

	build_items: list[str] = []
	manifest_items: list[str] = []

	for kernel_version in target_versions:
		target_archs = target_versions[kernel_version]
		manifest_item = format_manifest_item(kernel_version, target_archs)
		manifest_items.append(manifest_item)
		for gentoo_arch in target_archs:
			docker_platform = translate_gentoo_arch_to_docker_platform(gentoo_arch)
			build_item = format_build_item(kernel_version, gentoo_arch, docker_platform)
			build_items.append(build_item)

	print("::set-output name=build_items::%s" % json.dumps(build_items))
	print("::set-output name=manifest_items::%s" % json.dumps(manifest_items))

	return 0

if __name__ == '__main__':
    sys.exit(main())
