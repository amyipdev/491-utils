#!/usr/bin/env sh
# SPDX-License-Identifier: GPL-2.0-or-later

ls -l ../translator/postacc/ | awk '{print $5}' > sizes.txt
