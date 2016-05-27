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

        # Have our own logger capture warnings so we can format them.
        logging.captureWarnings(True)

        self.p = logging.getLogger('qb')
        self.p.setLevel(logging.INFO)

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

        # Define top-level options.
        parser.add_argument('-d', '--debug',
                            action='store_true',
                            help='Output in debug verbosity.')

        # Create a sub-parser for qb sub-commands.
        subparsers = parser.add_subparsers()

        # qb machine sub-parser.
        parser_machine = subparsers.add_parser('machine',
                                               aliases=['m'],
                                               help="Manage a qb machine.")

        group_machine = parser_machine.add_mutually_exclusive_group(
            required=True)

        # qb machine commands.
        # TODO: Maybe generate the below args by looping through a FUNC_DICT as
        # there's a fair amount of duplication.
        group_machine.add_argument('--create',
                                   nargs=1,
                                   metavar='NAME',
                                   help="Create a qb machine.")

        group_machine.add_argument('--start',
                                   nargs=1,
                                   metavar='NAME',
                                   help="Start a qb machine.")

        group_machine.add_argument('--stop',
                                   nargs=1,
                                   metavar='NAME',
                                   help="Stop a qb machine.")

        group_machine.add_argument('--remove',
                                   nargs=1,
                                   metavar='NAME',
                                   help="Remove a qb machine.")

        # qb container sub-parser.
        parser_container = subparsers.add_parser('container',
                                                 aliases=['c'],
                                                 help="Manage a qb container.")

        group_container = parser_container.add_mutually_exclusive_group(
            required=True)

        # qb container commands.
        group_container.add_argument('--create',
                                     nargs=1,
                                     metavar='NAME',
                                     help="Create a qb container.")

        group_container.add_argument('--start',
                                     nargs=1,
                                     metavar='NAME',
                                     help="Start a qb container.")

        group_container.add_argument('--stop',
                                     nargs=1,
                                     metavar='NAME',
                                     help="Stop a qb container.")

        group_container.add_argument('--remove',
                                     nargs=1,
                                     metavar='NAME',
                                     help="Remove a qb container.")

        # Create a Config instance and load configuration from file.
        config = Config()
        self.config = config.load(config_path)

        # Set functions for the sub-parsers to call.
        parser_machine.set_defaults(func=_Machine)
        parser_container.set_defaults(func=_Container)

        # Print help if no arg was provided, otherwise parse args and call the
        # relevant function.
        if len(sys.argv) <= 1:
            parser.print_help()
            sys.exit(1)
        else:
            args = parser.parse_args()

            if args.debug:
                self.p.setLevel(logging.DEBUG)
                self.p.debug("Debug mode is on.")

            args.func(args)

        sys.exit(0)


class _Machine(object):
    """ Class to wrap qb machine functionality. """

    def __init__(self, args):
        """ Function to manage qb machine operations. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        # Create a Machine instance.
        self.machine = Machine()

        # Invoke the required function.
        if args.create is not None:
            self.create(args.create, 'testImage')

    def create(self, name, image):
        """ Function to create a qb machine. """

        self.machine.create(name, image)

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
    """ Class to wrap qb container functionality. """

    def __init__(self, args):
        """ Function to manage qb container operations. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        self.p.debug(args)

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


if __name__ == "__main__":
    Client()
