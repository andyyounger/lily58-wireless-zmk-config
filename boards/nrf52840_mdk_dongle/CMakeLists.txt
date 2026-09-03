#
# Copyright (c) 2026 The ZMK Contributors
#
# SPDX-License-Identifier: MIT
#

# Convert the app image to UF2 (Makerdiary family id) so the ZMK build
# workflow's artifact contains a zmk.uf2 that can be copied straight onto
# the dongle's UF2 mass-storage drive (press reset to enter UF2 mode).
#
# The ZMK zephyr fork prunes upstream tools/, so use the self-contained
# converter shipped alongside this board instead of tools/uf2/uf2conv.py.
if(NOT DEFINED PYTHON_EXECUTABLE)
  find_package(Python3 REQUIRED COMPONENTS Interpreter)
  set(PYTHON_EXECUTABLE ${Python3_EXECUTABLE})
endif()

set_property(GLOBAL APPEND PROPERTY extra_post_build_commands
  COMMAND ${PYTHON_EXECUTABLE}
    ${CMAKE_CURRENT_LIST_DIR}/uf2conv_min.py
    ${PROJECT_BINARY_DIR}/${CONFIG_KERNEL_BIN_NAME}.bin
    0x1000
    0xADA52840
    ${PROJECT_BINARY_DIR}/${CONFIG_KERNEL_BIN_NAME}.uf2)
