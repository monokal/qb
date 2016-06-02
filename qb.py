#!/usr/bin/env python3

""" A command-line client to manage qb environments. """

import argparse
import logging.handlers
import sys

from client.config import Config
from container.container import Container
from machine.machine import Machine

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
        # TODO: Maybe generate the below args by iterating through a
        # FUNC_DICT as there's a fair amount of duplication.
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
        group_container.add_argument('--list',
                                     action='store_true',
                                     help="List qb containers.")

        group_container.add_argument('--create',
                                     nargs=2,
                                     metavar=('NAME', 'IMAGE'),
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

            # Create a Config instance and load configuration from file.
            config = Config()
            self.config = config.load(config_path)

            # Invoke the required function, passing it the parsed arguments
            # and qb config.
            args.func(args, self.config)

        return


class _Machine(object):
    """ Class to wrap qb machine functionality. """

    def __init__(self, args, config):
        """ Function to manage qb machine operations. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        # Pull out the relevant values from config.
        self.vagrantfile = config['machine']['vagrantfile']

        # Create a Machine instance.
        self.machine = Machine(self.vagrantfile)

        # Invoke the required function based on the provided args.
        if args.create is not None:
            self.create(args.create[0])

        elif args.start is not None:
            self.start(args.start[0])

        elif args.stop is not None:
            self.stop(args.stop[0])

        elif args.remove is not None:
            self.remove(args.remove[0])

        else:
            self.p.error("Error invoking function.")
            sys.exit(1)

        return

    def create(self, name):
        """ Function to create a qb machine. """

        self.machine.create(name)

        return

    def start(self, name):
        """ Start a qb machine. """

        self.machine.start(name)

        return

    def stop(self, name):
        """ Stop a qb machine. """

        self.machine.stop(name)

        return

    def remove(self, name):
        """ Remove a qb machine. """

        self.machine.remove(name)

        return


class _Container(object):
    """ Class to wrap qb container functionality. """

    def __init__(self, args, config):
        """ Function to manage qb container operations. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        # Pull out the relevant values from config.
        self.url = config['container']['lxd_api']['url']
        self.cert = config['container']['lxd_api']['cert']
        self.key = config['container']['lxd_api']['key']

        # Create a Container instance.
        self.container = Container(self.url, self.cert, self.key)

        # Invoke the required function based on the provided args.
        if args.list:
            self.list()

        elif args.create is not None:
            self.create(args.create[0],  # Name.
                        args.create[1])  # Image.

        elif args.start is not None:
            self.start(args.start[0])

        elif args.stop is not None:
            self.stop(args.stop[0])

        elif args.remove is not None:
            self.remove(args.remove[0])

        else:
            self.p.error("Error invoking function.")
            sys.exit(1)

        return

    def list(self):
        """ Function to list a qb containers. """

        self.container.list()

        return

    def create(self, name, image):
        """ Function to create a qb container. """

        self.container.create(name, image)

        return

    def start(self, name):
        """ Start a qb container. """

        self.container.start(name)

        return

    def stop(self, name):
        """ Stop a qb container. """

        self.container.stop(name)

        return

    def remove(self, name):
        """ Remove a qb container. """

        self.container.remove(name)

        return


if __name__ == "__main__":
    Client()
