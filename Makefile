# SPDX-License-Identifier: GPL-2.0-or-later

all: compdb
	$(MAKE) -C collector

clean:
	$(MAKE) -C collector clean

run_collector:
	$(MAKE) -C collector run
