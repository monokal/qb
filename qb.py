#!/usr/bin/env python3

""" A command-line client to manage qb environments. """

import argparse
import logging.handlers
import sys

__author__ = "Daniel Middleton"
__email__ = "d@monokal.io"
__status__ = "Prototype"
__version__ = "1.0.0"
__all__ = []

# Path to the pluslet client config file.
config_path = "config.yaml"


class Client(object):
    """ Class to wrap qb client functionality. """

    def __init__(self):
        """ Load config, configure logging, parse command-line arguments,
            provide usage and invoke functions. """

        # Have our own logger capture warnings so we can format them
        # appropriately.
        logging.captureWarnings(True)

        self.p = logging.getLogger('qb')
        self.p.setLevel(logging.DEBUG)

        # We just print to STDOUT for now as the qb client is primarily
        # intended to be used interactively.
        out = logging.StreamHandler(sys.stdout)
        out.setLevel(logging.DEBUG)

        formatter = logging.Formatter("(qb) %(message)s")

        out.setFormatter(formatter)
        self.p.addHandler(out)

        # Create the top-level parser.
        parser = argparse.ArgumentParser(
            prog="qb",
            description="A command-line client to manage qb environments.",
        )

        # Cr    eate a sub-parser for pluslet sub-commands.
        subparsers = parser.add_subparsers()


class Machine(object):
    """ Class to manage a qb machine. """

    def create(self):
        """ Function to create a qb machine. """

        pass


class Container(object):
    """ Class to manage a qb container. """

    def create(self):
        """ Function to create a qb container. """

        pass
