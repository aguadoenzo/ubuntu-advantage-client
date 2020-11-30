#!/usr/bin/env python3

"""
Some uaclient operations cannot be fully completed by running a single
command. For example, when upgrading uaclient from trusty to xenial,
we may have a livepatch change in the contract, allowing livepatch to be
enabled on xenial. However, during the upgrade we cannot install livepatch on
the system, only after a reboot.

To allow uaclient to postpone commands that need to be executed in a system boot,
we are using this script, which will basically try to reprocess contract deltas
on boot time.
"""
import logging
import os
import sys

from uaclient.util import subp, ProcessExecutionError
from uaclient.cli import setup_logging


CMDS_FILE_LOCATION = "/etc/ubuntu-advantage/reboot-cmds-needed"


def process_contract_deltas():
    setup_logging(logging.INFO, logging.DEBUG)

    if os.path.exists(CMDS_FILE_LOCATION):
        logging.debug(
            "Running process contract deltas on reboot ...".format(
                CMDS_FILE_LOCATION
            )
        )

        cmds = [
            "ua refresh",
            "/usr/bin/python3 /usr/lib/ubuntu-advantage/upgrade_lts_contract.py",
        ]

        for cmd in cmds:
            try:
                out, _ = subp(cmd.split())
                logging.debug("Successfully executed cmd: {}".format(cmd))
            except ProcessExecutionError as exec_error:
                msg = (
                    "Failed running cmd: {}\n"
                    "Return code: {}\n"
                    "Stderr: {}\n"
                    "Stdout: {}".format(
                        cmd,
                        exec_error.exit_code,
                        exec_error.stderr,
                        exec_error.stdout,
                    )
                )
                logging.debug(msg)
                sys.exit(1)


if __name__ == "__main__":
    process_contract_deltas()
