# SPDX-License-Identifier: GPL-2.0-or-later

CC := cc
CFLAGS := -O3 -Wall -Werror -ggdb
INCLUDES += $(shell pkg-config --cflags libcap libpcap)
LIBS += $(shell pkg-config --libs libcap libpcap)

all: capture.run

capture.run: capture.c
	$(CC) -o capture.run $(CFLAGS) $(INCLUDES) capture.c $(LIBS)

run: capture.run
	./capture.run

clean:
	rm -rf captures/ capture.run
