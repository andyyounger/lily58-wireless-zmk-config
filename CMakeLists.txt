# Zephyr module build files for this config's custom ZMK behaviors.
# See zephyr/module.yml (module root is this repository).
#
# esc-to-base references keymap-engine symbols (zmk_keymap_layer_to et al)
# which are only compiled for the central split role (or non-split boards);
# the peripheral half only forwards scancodes over BLE. Same gate as ZMK's
# own app/CMakeLists.txt. If this gate is ever bypassed, the .c file itself
# #errors out at compile time.
if ((NOT CONFIG_ZMK_SPLIT) OR CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
  target_sources(app PRIVATE src/behavior_esc_to_base.c)
endif()
