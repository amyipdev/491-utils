#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

from pathlib import Path
import string
import random
import os

with open("sizes.txt", "r") as f:
    dat = f.read()

Path("./randoms").mkdir(exist_ok=True)

for n in [int(x) for x in dat.split("\n") if x not in ("", "\n")]:
    outname = "./randoms/" + "".join(random.choices(string.ascii_letters + string.digits, k=64))
    with open(outname, "wb") as g:
        g.write(os.urandom(n))
