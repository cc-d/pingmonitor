#!/usr/bin/env python3
import argparse
import re
import subprocess
import time
from decimal import Decimal as D
from typing import Dict, Optional

from rich.console import Console
from rich.table import Table

from utils import cmd


class PingMonitor:
    def __init__(self, interval: int, host: str):
        self.interval = interval
        self.host = host
        self.history = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


    def ping(self) -> Optional[D]:
        """Sends a single ping to the host and returns the ICMP sequence number,
        average latency, and packet loss percentage in a dictionary.

        Returns:
            Dict[str, D]: A dictionary containing the ping results.
        """
        output, err = cmd(f'ping -c 1 {self.host}')
        reg = r'time=(\d+\.?\d+?)'

        rsearch = re.search(reg, output)
        if rsearch:
            self.history.append(D(str(rsearch.group(1))))
        else:
            self.history.append(None)
        return self.history[-1]


    def pingprint(self):
        hlen, htotal = D('0'), D('0')
        for h in self.history:
            hlen += 1
            if h is not None:
                htotal += h

        avg = D(str(htotal / hlen)).quantize(D('0.001'))

        ncount = self.history.count(None)
        if ncount == 0:
            ploss = D('0')
        else:
            ploss = D(hlen / ncount).quantize(D('0.01'))

        print(f'avg: {avg} ms | packet loss: {ploss}% | last pings: {[str(x) for x in self.history[-5:]]}')

    def run(self):
        """Continuously pings the host and updates the terminal display."""
        while True:
            self.ping()
            self.pingprint()
            time.sleep(self.interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ping a target IP at a regular interval.")
    parser.add_argument(
        "-i", "--interval", type=int, default=1, help="Interval between pings in seconds."
    )
    parser.add_argument(
        "-t", "--target", type=str, default="8.8.8.8", help="IP address to ping."
    )
    args = parser.parse_args()

    monitor = PingMonitor(args.interval, args.target)
    monitor.run()