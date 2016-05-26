#!/usr/bin/env python3

import argparse
import logging
import sys

import vagrant


class Machine(object):
    """ Class to wrap Machine functionality. """

    def __init__(self):
        """ Configure logging. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        # Create a Vagrant object.
        self.v = vagrant.Vagrant()

    def create(self):
        """ Create a qb machine. """

        # self.v.up(vm_name="%s" % args.NAME)

        pass
