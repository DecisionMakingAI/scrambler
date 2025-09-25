# -*- encoding: utf-8 -*-

import argparse
import errno
import os
import sys
import time


parser = argparse.ArgumentParser(description="Get simple receive/transmission" \
                     " statistics from network interface.")
parser.add_argument('--interface', '-i', action='append',
                     help="Network interface for which to compute statistics." \
                          " Can be specified multiple times.")
parser.add_argument('--sampling', '-s', default=60, type=int,
                    help="Max timespan in seconds for which to " \
                         "sample bandwidth rates. Default is 60.")
namespace = parser.parse_args()

NET_DIR = "/sys/class/net"
STAT_DIRS = list()
INTERFACES = namespace.interface

if not INTERFACES:
    # no interfaces specified, so examine all of them
    INTERFACES = list()
    for (dirpath, dirnames, filenames) in os.walk(NET_DIR):
        for dirname in dirnames:
            # add path to the network statistics for the interface
            STAT_DIRS.append(os.sep.join([dirpath, dirname, 'statistics']))
            # add interface name to the list of interfaces
            INTERFACES.append(dirname)
        break
else:
    # user specified one or more interfaces to monitor
    for i in INTERFACES:
        # check for valid interface
        d = os.sep.join([NET_DIR, i, 'statistics'])
        if not os.path.exists(d):
            sys.exit("Network interface '%s' does not exist. " \
                     " Program aborted." % i)
        # add path to the network statistics for the interface
        STAT_DIRS.append(d)

SAMPLING = namespace.sampling

TIMEPOINTS = [a for a in [1, 5, 15, 60] if a <= SAMPLING]
if SAMPLING not in TIMEPOINTS:
    TIMEPOINTS.append(SAMPLING) 

def main():
    allstats = dict([(i, list()) for i in INTERFACES])
    while True:
        out = ''
        for i in range(len(INTERFACES)):
            interface = INTERFACES[i]
            stat_dir = STAT_DIRS[i]
            with open(os.sep.join([stat_dir, 'rx_bytes'])) as f:
                rx_bytes = int(f.read())
            with open(os.sep.join([stat_dir, 'tx_bytes'])) as f:
                tx_bytes = int(f.read())
            (rx_thruput, tx_thruput, allstats[interface]) = \
                calc_thruput(rx_bytes, tx_bytes, allstats[interface])
            out += format(interface, rx_bytes, rx_thruput, tx_bytes, tx_thruput)
        if sys.stdout.isatty():
            print ("\033[H\033[J" + out)
        time.sleep(1)

def calc_thruput(rx_bytes, tx_bytes, stats):
    rx_thruput = list()
    tx_thruput = list()
    for p in TIMEPOINTS:
        if len(stats) >= p:
            delta = rx_bytes - stats[p - 1][0]
            rate = delta / p
            rx_thruput.append(int(rate))
        else:
            rx_thruput.append(None)
        if len(stats) >= p:
            delta = tx_bytes - stats[p - 1][1]
            rate = delta / p
            tx_thruput.append(int(rate))
        else:
            tx_thruput.append(None)
    stats = [(rx_bytes, tx_bytes)] + stats[:SAMPLING - 1]
    return rx_thruput, tx_thruput, stats

def format(interface, rx_bytes, rx_thruput, tx_bytes, tx_thruput):
    s = "%-20.20s %12.12s " % (interface + " thruput [b/s]", 'total')
    for i in range(len(TIMEPOINTS)):
        s += "%9.9s " % (str(TIMEPOINTS[i]) + "s")
    s += "\n%-20.20s %12.12s " % ('Receiving', rx_bytes)
    for i in range(len(TIMEPOINTS)):
        s += "%9.9s " % rx_thruput[i] if rx_thruput[i] else ''
    s += "\n%-20.20s %12.12s " % ('Transmitting', tx_bytes)
    for i in range(len(TIMEPOINTS)):
        s += "%9.9s " % tx_thruput[i] if tx_thruput[i] else ''
    s += '\n\n'
    return s

if __name__ == '__main__':
    main()

