# 491-utils
Code used in *Efficacy of Full-Packet Encryption in Mitigating Protocol Detection for Evasive Virtual Private Networks*

## General Procedures

To replicate the results, follow these instructions.

### Prerequisites

You will need:
* A reasonably modern, 64-bit, glibc-based (untested on musl) Linux system
* Python >= 3.11
* Make (preferably GNU Make)
* A GCC-compliant C compiler (gcc or clang)
* A reasonably recent Rust toolchain (must support Rust 2021)
* libpcap
* libcap
* openssl/libressl
* libxml2
* libxslt
* libzip
* zlib
* jq
* pkg-config

Alternatively, if you have Nix, you can run `nix-shell` in the project root to install all the dependencies.

The paper's experiments were tested on a Proxmox 8.1.10 server's hypervisor interface.

If you aren't using `nix-shell`, you need to create a virtualenv and install the requirements:

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Collect Packets

```sh
cd classifiers
make run
cd ..
```

You will need to SIGINT (Ctrl-C) the `make run` task to stop collecting packets unless you set up notifications.

If you want to set a notification for when your packet collection is done and automatically stop the collection, modify and launch `collector/warning.py` with your SMTP information and target directory size. Note that the number put in will be substantially lower than the true size of data collected due to issues with how the size is calculated.

Please note that the collector may suddenly crash with a segmentation fault, particularly on smaller disks; this indicates that you have run out of inodes. If this happens, you must reduce the number of packets you collected by at least 1/4, preferably 1/8, to account for the random packets and post-translation packets. You can check how many free inodes are on your partition by running `df -i` for exact numbers, or `df -hi` for human-readable numbers.

### Encrypt the Packets with ACC

```sh
cd translator
cargo run --release
cd ..
```

### Generate the Random Packets

```sh
cd classifiers
./gen_sizes.sh
python3 gen_randoms.py
# Don't leave the directory!
```

### Start running tests

```sh
# Assuming you are still in the classifiers directory
# Available classifiers: c45, cnn, gpsdt, knn, logit, mlp, mlp-tf, pbdt, randomforest, rnn, svm
python3 CLASSIFIERNAME.py
```

## Run the Random tests

The code defaults to running the ACC vs Network tests. To run ACC vs Random, open `classifiers/universal.py` and complete the following steps:

1. Edit line 20 by changing `../collector/captures/` to `./randoms/`
2. Edit line 37 by changing `f.read()[jump:]` to `f.read()`
3. Delete lines 21-36 inclusive
