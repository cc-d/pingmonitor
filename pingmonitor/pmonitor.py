#!/usr/bin/env python3
import argparse
import re
import subprocess
import time
from decimal import Decimal as D
from typing import Dict

from rich.console import Console
from rich.table import Table

from utils import cmd


def ping(ip: str = '8.8.8.8') -> dict:
    """Pings the target IP and returns the ICMP sequence number, average latency,
    and packet loss percentage in a dictionary.

    Args:
        ip (str): The IP address to ping. Defaults Google DNS #1 (8.8.8.8)

    Returns:
        dict: A dictionary containing the ping results.
    """
    pstr = f'ping -c 1 {ip}'
    out, err = cmd(pstr)
    return out.stdout


class PingMonitor:

    RE_SEQ = re.compile(r"icmp_seq=(\d+)")
    RE_AVG_RTT = re.compile(r"avg/?mdev\s*=\s*([\d.]+)")
    RE_PLOSS = re.compile(r"(\d+)% packet loss")

    def __init__(self, interval: int, host: str):
        self.interval = interval
        self.host = host
        self.history = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


    def ping(self) -> Dict[str, D]:
        """Sends a single ping to the host and returns the ICMP sequence number,
        average latency, and packet loss percentage in a dictionary.

        Returns:
            Dict[str, D]: A dictionary containing the ping results.
        """
        ping_cmd = ["ping", "-c", "1", self.host]
        ping_output = subprocess.run(
            ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        icmp_seq_re = re.compile(r"icmp_seq=(\d+)")
        avg_rtt_re = re.compile(r"avg/?mdev\s*=\s*([\d.]+)")
        packet_loss_re = re.compile(r"(\d+)% packet loss")

        icmp_seq = int(icmp_seq_re.search(ping_output.stdout).group(1))
        avg_rtt = D(avg_rtt_re.search(ping_output.stdout).group(1))
        packet_loss = D(packet_loss_re.search(ping_output.stdout).group(1))

        result = {
            "icmp_seq": icmp_seq,
            "avg_rtt": avg_rtt,
            "packet_loss": packet_loss,
        }

        self.history.append(result)
        return result

    def display_history(self):
        """Displays the ping history using a rich table."""
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ICMP Sequence")
        table.add_column("Avg. Latency (ms)")
        table.add_column("Packet Loss (%)")

        for entry in self.history:
            table.add_row(
                str(entry["icmp_seq"]),
                str(entry["avg_rtt"]),
                str(entry["packet_loss"]),
            )

        console.clear()
        console.print(table)

    def run(self):
        """Continuously pings the host and updates the terminal display."""
        with self:
            while True:
                self.ping()
                self.display_history()
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