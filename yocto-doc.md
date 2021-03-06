# Yocto

Before doing anything else, clone `poky`:

```shell
git clone git://git.yoctoproject.org/poky
```

You can choose the version that suits your needs on this [link](https://git.yoctoproject.org/cgit/cgit.cgi/poky/). Then, check it out. For example:

```shell
git checkout warrior
```

Before doing anything, be sure to position yourself in the `poky` folder and run:

```shell
source oe-init-build-dev
```

This will reposition you in the `poky/build` folder. The most important files here are `local.conf` and `bblayers.conf` in the `conf` subfolder.

## QEMU

After you build the image, you can run it in `qemu` using:

```shell
runqemu <machine> <image> [nographic]
```

The `<machine>` variable is the one you have set in `build/conf/local.conf` as the `MACHINE` variable. To be sure to be able to run `qemu`, you can use `qemuarm`, `qemuarm64` or `qemux86` for `MACHINE`, to name a few.

To exit, press `CTRL + a` followed by `x`.

Note: Further information on using QEMU can be found [here](https://qemu.weilnetz.de/doc/qemu-doc.html).

Note: You can configure the target machine for QEMU in the `meta/conf/machine` folder (use switches and options from the former link).

## Use `systemd`

To use `systemd` instead of `systemV`, just add these lines to `build/conf/local.conf`:

```shell
DISTRO_FEATURES_append += "systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"
DISTRO_FEATURES_BACKFILL_CONSIDERED += "sysvinit"
VIRTUAL-RUNTIME_initscripts = ""
```

## Yocto SDK

To generate Yocto SDK, run:

```shell
bitbake -c populate_sdk <IMAGE_NAME>
```

Bitbake will provide you with the path to the SDK installation script.

## Recipes

Recipe is any file with the `.bb` extension. You can build any recipe with:

```shell
bitbake <recipe_name>
```

We will discuss later how to add them to your target image.

## List Recipes

The following command will give you a list of recipes, along with their corresponding layer:

```shell
bitbake-layers show-recipes
```

### Add new recipe

To add a new recipe named "example" add the `example` subfolder in the layer of your choice and there add the file `example_01.bb`. There are multiple ways to write a recipe, so we will cover a few, depending on the build system used.

#### Common

An ordinary recipe should contain this as a header:

```shell
SUMMARY = "Short summary"
DESCRIPTION = "If description is empty, summary will be used."
AUTHOR = "Stjepan Poljak <stjepan.poljak@protonmail.com>"
HOMEPAGE = "https://github.com/StjepanPoljak"

SECTION = "examples"
DEPENDS = ""
PRIORITY = "optional"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"
```

You can check all these variables out on this [link](https://www.yoctoproject.org/docs/latest/ref-manual/ref-manual.html).

#### Kernel module

In our example, we will call our first module as `hello-mod`. Depending on the layer you want to use, you should create the `hello-mod` folder inside the `recipes-kernel` directory. There, in `recipes-kernel/hello-mod`, create a file called `hello-mod_0.1.bb` and a folder named `files`.

In `files` folder, put `hello.c` and `Makefile` (you can use the same from [hello world module](#hello-world-module)). You will also need a licence file which you can obtain from [GNU licenses](https://www.gnu.org/licenses/). Call it, for example, `COPYING` and get its checksum by using:

```shell
$ md5sum COPYING
```

After this, fill out the `hello-mod_0.1.bb` with following:

```shell
SUMMARY = "My first kernel module in Yocto"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

inherit module

SRC_URI = "file://Makefile"
SRC_URI += "file://hello-mod.c"
SRC_URI += "file://COPYING"

S = "${WORKDIR}"

RPROVIDES_${PN} += "kernel-module-hello-mod"
```

Note: Another way to provide a license is to use just:

```shell
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"
```

Then, in bitbake shell, you can see if everything went OK:

```shell
$ bitbake-layers show-recipes | grep hello-mod -A 1
```

You should see your kernel module, and below its name the name of the layer it resides in. Then, you can try building it:

```shell
$ bitbake hello-mod
```

If there are any error messages, handle them accordingly.

Once built, you can copy it to the target system and run with `sudo insmod <path_to_hello-mod.ko>`. Note that kernel versions have to match: `vermagic.o` is linked against the module to check this.

### Kernel Module via Yocto SDK

In order to be able to build an out-of-tree kernel module via Yocto SDK, it is neccessary to provide the SDK with kernel source. This can be done by adding the following line to the `local.conf` or `machine.conf` file:

```shell
TOOLCHAIN_TARGET_TASK_append = " kernel-devsrc"
```

After populating and installing the SDK, and after sourcing the SDK script, go to the following folder:

```
<SDK_PATH>/sysroots/<MACHINE>/usr/src/kernel
```

Then, run `make modules_prepare`. After that you can use this folder as the `KERNEL_SRC` variable in your `Makefile`.

## Layers

Layers in Yocto have only one purpose: to logically separate different functionalities of the operating system. This is only to ensure easier management later on, as the system grows or changes. For a naive example, you could have have this sort of layer structure:

```
meta-raspberrypi # BSP layer
meta-system-apps
meta-multimedia-apps
meta-games
```

All layers are stored in the `poky` folder and are named beginning withi the `meta-` keyword.

### Add new layer

To add new layer, after running `source oe-init-build-end`, return to the poky folder and run:

```shell
bitbake-layers create-layer <layer_name>
```

It is customary to prefix the layer name with `meta-` keyword. This will create a simple folder structure for your layer. To add the new layer to the build, type in the `build` subfolder:

```shell
bitbake-layers add-layer <layer_name>
```

Or, even better, edit the `build/conf/bblayers.conf` to include your layer.

### Add new BSP layer

Instead of adding everything manually, from firmware to other packages required to boot the device, it's better to find existing layers on [OpenEmbedded Layer Index](https://layers.openembedded.org).

## Images

Images are exactly what the name says. Recipes that define how an image ready to be installed on the system will look like, i.e. what it will contain. In `poky` there are two basic images you can include in your own image:

```
core-image-base
core-image-minimal
```

### Add new image

Here is an example of an image recipe that inherits `core-image` and includes `core-image-minimal`:

```shell
SUMMARY = "Custom image"

LICENSE = "MIT"

inherit core-image
require recipes-core/images/core-image-minimal.bb

CORE_IMAGE_EXTRA_INSTALL = "recipe1 recipe2"
```

It is customary to put the `<image_name>.bb` file in the `<layer>/recipes-core/images/<image_name>` folder. The path in `require` line is necessary if you are including an image from another layer.

Add your recipes to the `CORE_IMAGE_EXTRA_INSTALL` variable (here we only have two recipes named `recipe1` and `recipe2`).

### Package Groups

Instead of specifying `CORE_IMAGE_EXTRA_INSTALL` (which will only append to the `core-image`) it is best to keep packages to be installed inside a package group.

In the subfolder `<layer>/recipes-core/packagegroups` create a file called `packagegroup-mygroup.bb` and then fill it out with:

```shell
DESCRIPTION = "Packages to be installed as part of mygroup"
LICENSE = "MIT"

PR = "r0"

PACKAGE_ARCH = "all"

inherit packagegroup

RDEPENDS_${PN} += "recipe1"
RDEPENDS_${PN} += "recipe2"
```

The `PR` variable signifies package revision (initally `r0`). The `PACKAGE_ARCH` specifies architecture. If you want it to be target-specific, assign it the `${MACHINE_ARCH}` variable.

In this case, instead of `CORE_IMAGES_EXTRA_INSTALL` variable, as in previous example, you can use:

```shell
IMAGE_INSTALL += "packagegroup"
```

This is the preferred way.

## Configure Kernel

It is best to run menuconfig from bitbake:

```shell
bitbake <target>:do_menuconfig
```

If you made any changes and saved, you can use:

```shell
bitbake <target>:do_diffconfig
```

You will get a message telling you where the `.cfg` file has been output to. Then, copy this to the files folder of your target recipe and add it in the `SRC_URI`.

The same `.cfg` file can be obtained from Linux kernel repository by typing the following in the kernel folder:

```shell
scripts/diffconfig -m <oldconf> <newconf> > fragment.cfg
```

## Raspberry Pi Yocto

First, clone Poky and `meta-raspberrypi`:

```shell
git clone -b warrior git://git.yoctoproject.org/poky
cd poky
git clone -b warrior git://git.yoctoproject.org/meta-raspberrypi
```

Note: Instead of `warrior` you can use some other branch.

After running `source oe-init-build-env`, add `meta-raspberrypi` to `BBLAYERS` in `conf/bblayers.conf`. Then, in the `conf/local.conf` set the `MACHINE` variable to desired RPi machine; you can find the full list of supported Raspberry Pi machines in `meta-raspberrypi/docs/layer-contents.md`. In the same file, it may also be necessary to append:

```
GPU_MEM = "16"
```

