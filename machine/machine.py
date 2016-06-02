#!/usr/bin/env python3

import logging
import sys

from vagrant import Vagrant  # https://github.com/todddeluca/python-vagrant


class Machine(object):
    """ Class to wrap Machine functionality. """

    def __init__(self, vagrantfile):
        """ Configure logging. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        self.p.debug("Using Vagrant config:\n"
                     "     Vagrantfile: %s" % vagrantfile)

        # Create a Vagrant object.
        self.vagrant = Vagrant(vagrantfile)

        return

    def create(self, name):
        """ Create a qb machine. """

        try:
            self.p.info("Creating %s..." % name)
            self.vagrant.up(vm_name=name)
            self.p.info('Done!')

        except Exception as e:
            self.p.debug(e)
            self.p.error("Failed to create machine.")
            sys.exit(1)

        return

    def start(self, name):
        """ Start a qb machine. """

        self.p.debug("Starting \"%s\"." % name)

        return

    def stop(self, name):
        """ Stop a qb machine. """

        self.p.debug("Stopping \"%s\"." % name)

        return

    def remove(self, name):
        """ Remove a qb machine. """

        self.p.debug("Removing \"%s\"." % name)

        return
