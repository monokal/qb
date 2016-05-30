#!/usr/bin/env python3

import logging

import vagrant


class Machine(object):
    """ Class to wrap Machine functionality. """

    def __init__(self):
        """ Configure logging. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        # Create a Vagrant object.
        self.v = vagrant.Vagrant()

    def create(self, name):
        """ Create a qb machine. """

        self.p.debug("Creating \"%s\"." % name)

        # self.v.up(vm_name="%s" % args.NAME)

    def start(self, name):
        """ Start a qb machine. """

        self.p.debug("Starting \"%s\"." % name)

    def stop(self, name):
        """ Stop a qb machine. """

        self.p.debug("Stopping \"%s\"." % name)

    def remove(self, name):
        """ Remove a qb machine. """

        self.p.debug("Removing \"%s\"." % name)
