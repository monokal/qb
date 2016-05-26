#!/usr/bin/env python3

""" A command-line client to manage qb environments. """

import argparse
import logging.handlers
import sys

from client.config import Config
from machine.machine import Machine
from container.container import Container

__author__ = "Daniel Middleton"
__email__ = "d@monokal.io"
__status__ = "Prototype"
__version__ = "1.0.0"
__all__ = []

# Path to the qb client config file.
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

        # Create a sub-parser for qb sub-commands.
        subparsers = parser.add_subparsers()

        # qb command sub-parsers.
        parser_machine = subparsers.add_parser('machine',
                                               aliases=['m'],
                                               help="Manage a qb machine.")

        parser_container = subparsers.add_parser('container',
                                               aliases=['c'],
                                               help="Manage a qb container.")

        # Create a Config object and load configuration from file.
        config = Config()
        self.config = config.load(config_path)

        # Set functions for the sub-parsers to call.
        parser_machine.set_defaults(func=_Machine)
        parser_container.set_defaults(func=_Container)

        # Print help if no arg was provided, otherwise parse and call the
        # relevant function.
        if len(sys.argv) <= 1:
            parser.print_usage()
            sys.exit(1)
        else:
            args = parser.parse_args()
            args.func(args)

        sys.exit(0)


class _Machine(object):
    """ Class to manage a qb machine. """

    def __init__(self, arg):
        """ Function to manage qb machine operations. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        self.p.debug("In _Machine __init__ and I got %s" % arg)

    def create(self):
        """ Function to create a qb machine. """

        pass

    def start(self):
        """ Start a qb machine. """

        pass

    def stop(self):
        """ Stop a qb machine. """

        pass

    def remove(self):
        """ Remove a qb machine. """

        pass


class _Container(object):
    """ Class to manage a qb container. """

    def __init__(self):
        """ Function to manage qb container operations. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        self.p.debug("In _Container __init__")

    def create(self):
        """ Function to create a qb container. """

        pass

    def start(self):
        """ Start a qb container. """

        pass

    def stop(self):
        """ Stop a qb container. """

        pass

    def remove(self):
        """ Remove a qb container. """

        pass

