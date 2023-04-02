#!/usr/bin/emv python3
import argparse
import re
import subprocess
import time
from decimal import Decimal as D
from typing import *


def cmd(command: str) -> Tuple[str, str]:
    """Runs a command on the host system and returns its output and error (if any).

    Args:
        command (str): The command to be executed on the host system.

    Returns:
        Tuple[str, str]: A tuple containing the command's output (stdout) and error (stderr).
    """
    process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    return str(process.stdout), str(process.stderr)