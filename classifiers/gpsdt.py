#!/usr/bin/env python3

import random
# import guaranteed by scikit-learn
import scipy

with open("sizes.txt", "r") as f:
    dat0 = f.read()
with open("sizes-og.txt", "r") as f:
    dat1 = f.read()

og_dat = [int(x) for x in dat1.split("\n") if x not in ("", "\n")]
random.shuffle(og_dat)
after_dat = [int(x) for x in dat0.split("\n") if x not in ("", "\n")]
random.shuffle(after_dat)

sizes = [0 for n in range(1501)]
for ent in og_dat[len(og_dat)//5:]:
    sizes[ent] += 1
for i in range(len(sizes)):
    sizes[i] /= len(og_dat)
    sizes[i] *= 1000

def test_res(dataset: list[int], length: int) -> (int, int):
    cata, catb = 0,0
    for i in range(length):
        sizes_local = [0 for n in range(1501)]
        for j in range(1000):
            sizes_local[after_dat[i*1000+j]] += 1
        chisq = 0
        for s in range(1501):
            O = sizes_local[s]
            E = sizes[s]
            if E == 0:
                continue
            chisq += (O-E)**2/E
        if scipy.stats.chi2.sf(chisq, 1500) <= 0.0001: cata += 1
        else: catb += 1
    return (cata, catb)


tp, fp, tn, fn = 0,0,0,0
ra = test_res(after_dat, len(after_dat)//1000)
tp += ra[0]
fn += ra[1]
rb = test_res(og_dat, len(og_dat)//5000)
fp += rb[0]
tn += rb[1]
print(f"TP={tp},FP={fp},TN={tn},FN={fn}")

"""
for i in range(len(after_dat)//1000):
    sizes_local = [0 for n in range(1501)]
    for j in range(1000):
        sizes_local[after_dat[i*1000+j]] += 1
    chisq = 0
    for s in range(1501):
        O = sizes_local[s]
        E = sizes[s]
        if E == 0:
            # avoid DBZ
            continue
        chisq += (O-E)**2/E
    if scipy.stats.chi2.sf(chisq, 1500) <= 0.0001:
        tp += 1
    else:
        fn += 1
for i in range(len(og_dat)//5000):
    sizes_local = [0 for n in range(1501)]
    for j in range(1000):
        sizes_local[og_dat[i*1000+j]] += 1
    chisq = 0
    for s in range(1501):
        O = sizes_local[s]
        E = sizes[s]
        if E == 0:
            continue
        chisq += (O-E)**2/E
    if scipy.stats.chi2.sf(chisq, 1500) <= 0.0001:
        fp += 1
    else:
        tn += 1
"""
