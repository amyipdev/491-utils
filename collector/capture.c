// SPDX-License-Identifier: GPL-2.o-or-later

#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <sys/capability.h>
#include <sys/stat.h>

#include <netinet/if_ether.h>

#include <pcap/pcap.h>

typedef struct pcap_pkthdr pcap_pkthdr_t;
typedef struct ether_header ether_header_t;

static char pcapeb[PCAP_ERRBUF_SIZE];
static const char charset[] = "abcdefghijklmnopqrstuvwxyzABCEDFGHIJKLMNOPQRSTUVWXYZ0123456789";

const unsigned char IPNPROTO_UDP = 0x11;
const unsigned char IP6_ICMPV6 = 0x3a;
const unsigned char ICMPV6_RS = 133;
const unsigned char ICMPV6_NA = 136;

#define ERR_ON(r)                                      \
    do {                                               \
        if (r) {                                       \
           printf("%.*s\n", PCAP_ERRBUF_SIZE, pcapeb); \
           exit(1);                                    \
        }                                              \
    } while (0)

// Assumes packet is defined
// PDB probably isn't necessary, should be able to index directly,
// but it does make things look cleaner/more consistent with pds
#define pdb(off) (*(unsigned char *)(packet + off))
#define pds(off) (*(unsigned short *)(packet + off))

const char *CAPTURES_DIR = "./captures";

int main() {
    // Verify that CAP_NET_RAW and CAP_NET_ADMIN are held
    cap_t caps = cap_get_proc();
    if (caps == NULL) {
        printf("fatal: cannot check capabilities\n");
        exit(-errno);
    }
    cap_flag_value_t ret_raw;
    cap_flag_value_t ret_adm;
    if (cap_get_flag(caps, CAP_NET_RAW, CAP_EFFECTIVE, &ret_raw) || cap_get_flag(caps, CAP_NET_ADMIN, CAP_EFFECTIVE, &ret_adm)) {
        printf("fatal: internal argument error with libcap\n");
        exit(-EINVAL);
    }
    if (!ret_raw || !ret_adm) {
        printf("fatal: missing networking admin capabilities\n");
        exit(-EPERM);
    }
    cap_free(caps);


    // Check that the directory exists, if not create it
    struct stat dir;
    if (stat(CAPTURES_DIR, &dir) == 0) {
        if (!S_ISDIR(dir.st_mode)) {
            printf("fatal: captures exists, but is not a directory\n");
            exit(-ENOTDIR);
        }
    } else {
        if (errno != ENOENT) {
            printf("fatal: OS error %d: %s\n", errno, strerror(errno));
        }
        mkdir(CAPTURES_DIR, 0755);
    }

    // Initialization
    if (chdir(CAPTURES_DIR)) {
        printf("fatal: cannot enter captures directory: %s (%d)\n", strerror(errno), errno);
        exit(-errno);
    }
    srand(time(NULL));
    ERR_ON(pcap_init(0, pcapeb));

    // Select interface and load it
    pcap_if_t *ifs;
    ERR_ON(pcap_findalldevs(&ifs, pcapeb));
    while (ifs->next != NULL) {
        // Unfortunately there are no other flags than LOOPBACK that we can check
        // Thankfully the order is such that primary eth out should come first
        // Usually if#2, but things happen, so better to just search, plus pcap
        // wants an interface name and not number
        if (ifs->flags == PCAP_IF_LOOPBACK) {
            ifs = ifs->next;
        } else {
            // Hopefully this is general eth out and not a bridge
            break;
        }
    }
    if (ifs->next == NULL) {
        printf("fatal: no valid interfaces\n");
        exit(-EINVAL);
    }
    printf("info: capturing on interface %s\n", ifs->name);
    pcap_t *cap = pcap_open_live(ifs->name, BUFSIZ, 0, -1, pcapeb);

    // Run capture loop
    // NOTE: eth header = 14 bytes
    pcap_pkthdr_t pkthdr;
    const unsigned char *packet;
    while (true) {
        packet = pcap_next(cap, &pkthdr);
        if (packet == NULL)
            continue;
        ether_header_t *eptr = (struct ether_header *) packet;
        unsigned short len;
        switch (ntohs(eptr->ether_type)) {
            case ETHERTYPE_IP:
                len = ntohs(pds(16));
                // skip corosync from Proxmox nodes - drop node-node UDP
                if (pdb(27) == 0x1 && pdb(31) == 0x1 && pdb(23) == IPNPROTO_UDP)
                    continue;
                break;
            case ETHERTYPE_IPV6:
                unsigned char icmpv6t;
                if (pds(20) == IP6_ICMPV6
                    && ((icmpv6t = pdb(54)) >= ICMPV6_RS
                        || icmpv6t <= ICMPV6_NA)) {
                    continue;
                }
                len = ntohs(pds(18));
            default:
                continue;
        }
        // Reduce "bad data", take only 1280 - less processing in stage 2
        // This also addresses pooling at size=1500
        if (len > 1280)
            continue;
        char filename[65];
        filename[64] = 0;
        for (int i = 0; i < 64; ++i)
            filename[i] = charset[rand() % (sizeof(charset)-1)];
        FILE *fp = fopen(filename, "w");
        len += 14;
        for (int pos = 14; pos < len; ++pos)
            fputc(packet[pos], fp);
        fclose(fp);
    }
}
