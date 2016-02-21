"""
ifspeed.py

Usage:
  ifspeed.py (-h | --help)
  ifspeed.py --version
  ifspeed.py [--dev=<dev>]

Options:
  -h --help         Show this screen.
  --version         Show version.
  --dev=<dev>       if device. [default: eth0]


"""

import time
import docopt
import collections

STAT_FOLDER = "/sys/class/net/{}/statistics"
RX_BYTES = STAT_FOLDER + "/rx_bytes"
TX_BYTES = STAT_FOLDER + "/tx_bytes"


def get_bytes(dev):
    rx = int(get_rx_bytes(dev))
    tx = int(get_tx_bytes(dev))

    return rx, tx


def bytes_to_mbit(bytes):
    return (bytes * 8) / 1024**2


def get_rx_bytes(dev):
    with open(RX_BYTES.format(dev)) as f:
        content = f.readline()
    return content


def get_tx_bytes(dev):
    with open(TX_BYTES.format(dev)) as f:
        content = f.readline()
    return content


def main():
    arguments = docopt.docopt(__doc__, version='0.0.1')

    old_rx, old_tx = get_bytes(arguments["--dev"])
    t = 1
    n = 5

    rx = collections.deque(maxlen=n)
    tx = collections.deque(maxlen=n)

    while True:
        time.sleep(t)

        new_rx, new_tx = get_bytes(arguments["--dev"])

        rx.append(new_rx - old_rx)
        tx.append(new_tx - old_tx)

        tx_mbit = int(bytes_to_mbit(sum(tx)) / len(tx))
        rx_mbit = int(bytes_to_mbit(sum(rx)) / len(rx))

        print(rx_mbit)
        print(tx_mbit)

        old_rx, old_tx = new_rx, new_tx


if __name__ == "__main__":
    main()

