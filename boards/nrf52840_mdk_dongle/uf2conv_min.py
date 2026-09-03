#!/usr/bin/env python3
#
# Minimal, self-contained bin -> UF2 converter for the Makerdiary
# nRF52840-MDK USB dongle bootloader.
#
# The ZMK zephyr fork prunes the upstream `tools/` directory, so
# tools/uf2/utils/uf2conv.py is not available in the CI workspace. This
# mirrors the exact block layout that makerdiary/uf2conv produces.
#
# Usage: uf2conv_min.py <input.bin> <base_address> <family_id> <output.uf2>
#   base_address : hex, e.g. 0x1000 (where the app partition starts)
#   family_id    : hex, e.g. 0xADA52840 (Makerdiary nRF52840 family)

import struct
import sys

UF2_MAGIC_START0 = 0x0A324655  # "UF2\n"
UF2_MAGIC_START1 = 0x9E5D5157  # Randomly selected
UF2_MAGIC_END = 0x0AB16F30  # Ditto


def convert_to_uf2(file_content, appstartaddr, familyid):
    datapadding = b""
    while len(datapadding) < 512 - 256 - 32 - 4:
        datapadding += b"\x00\x00\x00\x00"
    numblocks = (len(file_content) + 255) // 256
    outp = []
    for blockno in range(numblocks):
        ptr = 256 * blockno
        chunk = file_content[ptr : ptr + 256]
        flags = 0x0
        if familyid:
            flags |= 0x2000
        hd = struct.pack(
            "<IIIIIIII",
            UF2_MAGIC_START0,
            UF2_MAGIC_START1,
            flags,
            ptr + appstartaddr,
            256,
            blockno,
            numblocks,
            familyid,
        )
        while len(chunk) < 256:
            chunk += b"\x00"
        block = hd + chunk + datapadding + struct.pack("<I", UF2_MAGIC_END)
        assert len(block) == 512
        outp.append(block)
    return b"".join(outp)


def main():
    if len(sys.argv) != 5:
        sys.stderr.write(__doc__)
        return 2
    inp, base, family, outp = sys.argv[1:5]
    appstartaddr = int(base, 16)
    familyid = int(family, 16)
    with open(inp, "rb") as f:
        data = f.read()
    with open(outp, "wb") as f:
        f.write(convert_to_uf2(data, appstartaddr, familyid))
    return 0


if __name__ == "__main__":
    sys.exit(main())
