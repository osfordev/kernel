# Development Notes

## Update kernel configuration

For the task you may use base image [zxteamorg/gentoo-sources-bundle](https://hub.docker.com/r/zxteamorg/gentoo-sources-bundle). To do that, you have:

* start container from image [zxteamorg/gentoo-sources-bundle](https://hub.docker.com/r/zxteamorg/gentoo-sources-bundle) along with mount your latest kernel congiration
* execute `make oldconfig` along with [](https://www.kernel.org/doc/html/latest/kbuild/kconfig.html#kconfig-config)

## Example for update `x86` kernel config

Update from `5.10.76-gentoo-r1` to version `5.15.16`:

```shell
# Start a container
docker run --rm --interactive --tty --platform linux/386 \
  --mount type=bind,source="${PWD}/sites",target=/data \
  zxteamorg/gentoo-sources-bundle:5.15.16

# Inside containder
export KCONFIG_CONFIG=/data/asrockpv530aitx/x86/config-5.15.16-gentoo-asrockpv530aitx
cp /data/asrockpv530aitx/x86/config-5.10.76-gentoo-r1-asrockpv530aitx "${KCONFIG_CONFIG}"
make oldconfig
rm "${KCONFIG_CONFIG}.old"
```

## Example for update `amd64` kernel config

Update from `5.10.76-gentoo-r1` to version `5.15.16`:

```shell
# Start a container
docker run --rm --interactive --tty --platform linux/amd64 \
  --mount type=bind,source="${PWD}/sites",target=/data \
  zxteamorg/gentoo-sources-bundle:5.15.16

# Inside containder
export KCONFIG_CONFIG=/data/digitaloceanvm/amd64/config-5.15.16-gentoo-digitaloceanvm
cp /data/digitaloceanvm/amd64/config-5.10.76-gentoo-r1-digitaloceanvm "${KCONFIG_CONFIG}"
make oldconfig
rm "${KCONFIG_CONFIG}.old"
```