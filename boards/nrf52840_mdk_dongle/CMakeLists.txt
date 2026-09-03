#
# Copyright (c) 2026 The ZMK Contributors
#
# SPDX-License-Identifier: MIT
#

# Convert the app image to UF2 (Makerdiary family id) so the ZMK build
# workflow's artifact contains a zmk.uf2 that can be copied straight onto
# the dongle's UF2 mass-storage drive (press reset to enter UF2 mode).
set_property(GLOBAL APPEND PROPERTY extra_post_build_commands
  COMMAND ${PYTHON_EXECUTABLE} ${ZEPHYR_BASE}/../tools/uf2/utils/uf2conv.py
    -c
    -b 0x1000
    -f 0xADA52840
    -o ${PROJECT_BINARY_DIR}/${CONFIG_KERNEL_BIN_NAME}.uf2
    ${PROJECT_BINARY_DIR}/${CONFIG_KERNEL_BIN_NAME}.bin)
