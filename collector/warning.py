#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import os
import subprocess
from smtplib import SMTP
import socket
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
smtp = SMTP()
smtp.set_debuglevel(0)
smtp.connect("mail.amyip.net", 587)

from_addr = "491 Research Client <491@fullerton.tld>"
to_addr = "Amy Parker <amy@amyip.net>"
hostname = socket.gethostname()

while True:
    size = subprocess.check_output(["du","-sh","./captures/"]).split()[0].decode("utf-8")
    if size[-1] != "G":
        continue
    if float(size[:-1]) >= 25:
        break
    time.sleep(10)

smtp.sendmail(from_addr, to_addr, f"From: {from_addr}\n"
                                  f"To: {to_addr}\n"
                                  f"Subject: {hostname} hit 25 GiB limit\n\n"
                                  f"The 491 research server running on {hostname} hit its 25 GiB limit.\n"
                                  f"Packet collection has been suspended, and the results should be retrieved.\n"
                                  f"  - 491 utilities -\n")
smtp.quit()

os.system("tmux kill-server")
