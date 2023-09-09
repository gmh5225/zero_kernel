# s0nh_kernel — an Android kernel w/ Kali NetHunter support

## **Disclaimer**

**This kernel is made for educational purposes only.**

**I am not responsible for anything that may happen to your device by installing any custom ROMs and/or kernels.**

**Anything you do with this kernel you do at your own risk. By using it, you take the responsibility upon yourself and in case of any issue you are not to blame me or other related contributors.**

## **Contents**

- [s0nh\_kernel — an Android kernel w/ Kali NetHunter support](#s0nh_kernel--an-android-kernel-w-kali-nethunter-support)
  - [**Disclaimer**](#disclaimer)
  - [**Contents**](#contents)
  - [**Kernel Features**](#kernel-features)
  - [**Supported ROMs**](#supported-roms)
  - [**Supported devices**](#supported-devices)
  - [**Usage**](#usage)
    - [**Prerequisites**](#prerequisites)
    - [**Kernel**](#kernel)
    - [**Assets**](#assets)
    - [**Bundle**](#bundle)
  - [**Examples**](#examples)
  - [**See also**](#see-also)

## **Kernel Features**

The kernel has the following features:

- Kali NetHunter support;
- RTL8812/21AU + RTL8814AU + RTL8187 Wi-Fi drivers;
- packet injection support for internal Wi-Fi chipset;
- KernelSU support.

## **Supported ROMs**

- LineageOS;
- ParanoidAndroid* (partially, some of the features do not work).

## **Supported devices**

- OnePlus 5;
- OnePlus 5T.

## **Usage**

The custom build wrapper consists of 3 main parts:

- kernel builder;
- assets collector;
- kernel + assets bundler.

```help
$ python3 wrapper --help
usage: wrapper [-h] [--clean] {kernel,assets,bundle} ...

A custom wrapper for the s0nh_kernel.

positional arguments:
  {kernel,assets,bundle}
    kernel              build the kernel
    assets              collect assets
    bundle              build the kernel + collect assets

optional arguments:
  -h, --help            show this help message and exit
  --clean               clean the root directory
```

### **Prerequisites**

**It is highly recommended to use `docker` option to run this tool.** For that you need Docker Engine or Docker Desktop, depending on your OS.

To run this tool in a `local` environment, you will need:

- a Debian-based Linux distribution (other types of distros are untested);
- packages installed via apt: `libssl-dev`, `wget`, `git`, `make`, `gcc`, `zip`.

You will also need a few Python packages. To install them, use:

```sh
python3 -m poetry install
```

To install `poetry`, use `python3 -m pip install poetry`.

### **Kernel**

Kernel build process can be launched by using the `python3 wrapper kernel <arguments>` command.

For more options you can refer to the help message below.

```help
$ python3 wrapper kernel --help
usage: wrapper kernel [-h] [-c] [--clean-image]
                      [--log-level {normal,verbose,quiet}] [-o OUTLOG] [--ksu]
                      {local,docker,podman} {los,aospa} codename

positional arguments:
  {local,docker,podman}
                        select build environment
  {los,aospa}           select a ROM for the build
  codename              select device codename

optional arguments:
  -h, --help            show this help message and exit
  -c, --clean           don't build anything, just clean the environment
  --clean-image         remove Docker/Podman image from the host machine after
                        build
  --log-level {normal,verbose,quiet}
                        select log level
  -o OUTLOG, --output OUTLOG
                        save logs to a file
  --ksu                 add KernelSU support
```

### **Assets**

As mentioned, there is also an asset downloader, which can collect latest versions of ROM, TWRP, Magisk and it's modules, Kali Chroot etc.

```help
$ python3 wrapper assets --help
usage: wrapper assets [-h] [--extra-assets EXTRA_ASSETS] [--rom-only]
                      [--clean-image] [--clean]
                      [--log-level {normal,verbose,quiet}] [-o OUTLOG] [--ksu]
                      {local,docker,podman} {los,aospa} codename
                      {full,minimal}

positional arguments:
  {local,docker,podman}
                        select build environment
  {los,aospa}           select a ROM for the build
  codename              select device codename
  {full,minimal}        select Kali chroot type

optional arguments:
  -h, --help            show this help message and exit
  --extra-assets EXTRA_ASSETS
                        select a JSON file with extra assets
  --rom-only            download only the ROM as an asset
  --clean-image         remove Docker/Podman image from the host machine after
                        build
  --clean               autoclean 'assets' folder if it exists
  --log-level {normal,verbose,quiet}
                        select log level
  -o OUTLOG, --output OUTLOG
                        save logs to a file
  --ksu                 add KernelSU support
```

### **Bundle**

There is an option named `bundle` which combines build artifacts of both `kernel` and `assets` modules into a single package.

This is especially useful for linking the kernel version with the appropriate ROM version.

There are cases when an old kernel version is used with the newer ROM version (adapted for the *newer* version of kernel). Such cases can ultimately lead to your system working improperly or breaking down completely, which is why it is important to use a specific kernel build with a corresponding ROM build.

Currently, there are three types of packaging available:

- `conan`;
- `slim`;
- `full`.

Options `full` and `conan` collect all of the assets required to successfuly flash the kernel onto your device. The difference between the two is that `full` option places everything into a local directory, while `conan` organizes everything as a Conan package.

An option named `slim` is a much lighter version of `full` packaging, as only the ROM is collected from the asset list. This is done to reduce package sizes while ensuring the kernel+ROM compatibility.

```help
$ python3 wrapper bundle --help
usage: wrapper bundle [-h] [--conan-upload] [--clean-image]
                      [--log-level {normal,verbose,quiet}] [-o OUTLOG] [--ksu]
                      {local,docker,podman} {los,aospa} codename
                      {conan,slim,full}

positional arguments:
  {local,docker,podman}
                        select build environment
  {los,aospa}           select a ROM for the build
  codename              select device codename
  {conan,slim,full}     select package type of the bundle

optional arguments:
  -h, --help            show this help message and exit
  --conan-upload        upload Conan packages to remote
  --clean-image         remove Docker/Podman image from the host machine after
                        build
  --log-level {normal,verbose,quiet}
                        select log level
  -o OUTLOG, --output OUTLOG
                        save logs to a file
  --ksu                 add KernelSU support
```

## **Examples**

Here are some examples of commands:

- **(Recommended)** Build kernel and collect ROM via Docker:
  - `python3 wrapper bundle docker los dumpling slim`;
- Build kernel locally:
  - `python3 wrapper kernel local los dumpling`;
- Collect all the assets locally:
  - `python3 wrapper assets local los dumpling full`.

## **See also**

- [FAQ](docs/FAQ.md);
- [TODO List](docs/TODO.md);
- [Kernel Flashing Instructions](docs/FLASHING.md).
