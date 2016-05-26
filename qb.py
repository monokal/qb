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

        sp = parser.add_subparsers(dest='cmdstr')

        sp1 = sp.add_parser('machine')
        sp1.set_defaults(cmd=lambda: '_Machine')

        sp2 = sp.add_parser('container')
        sp2.set_defaults(cmd=lambda: '_Container')

        parser.parse_args(['machine']).cmd()

        # # Create a sub-parser for qb sub-commands.
        # subparsers = parser.add_subparsers()
        #
        # # qb machine sub-parser.
        # parser_machine = subparsers.add_parser('machine',
        #                                        aliases=['m'],
        #                                        help="Manage a qb machine.")
        #
        # parser_machine.add_argument('create', help="Create a qb machine.")
        # parser_machine.add_argument('start', help="Start a qb machine.")
        # parser_machine.add_argument('stop', help="Stop a qb machine.")
        # parser_machine.add_argument('remove', help="Remove a qb machine.")
        #
        # # qb container sub-parser.
        # parser_container = subparsers.add_parser('container',
        #                                        aliases=['c'],
        #                                        help="Manage a qb container.")
        #
        # parser_container.add_argument('create', help="Create a qb container.")
        # parser_container.add_argument('start', help="Start a qb container.")
        # parser_container.add_argument('stop', help="Stop a qb container.")
        # parser_container.add_argument('remove', help="Remove a qb container.")
        #
        # # Create a Config object.
        # config = Config()
        #
        # # Load configuration from file and make it available globally.
        # self.config = config.load(config_path)
        #
        # # Set functions for the sub-parsers to call.
        # parser_machine.set_defaults(func=_Machine)
        # parser_container.set_defaults(func=_Container)
        #
        # args = parser.parse_args()
        #
        # print(args)


class _Machine(object):
    """ Class to manage a qb machine. """

    def __init__(self):
        """ Function to manage qb machine operations. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        self.p.debug("In _Machine __init__")

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

