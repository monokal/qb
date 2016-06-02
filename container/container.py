#!/usr/bin/env python3

import logging
import sys

import dateutil.parser
from pylxd import Client  # https://pylxd.readthedocs.io/
from tabulate import tabulate  # https://pypi.python.org/pypi/tabulate


class Container(object):
    """ Class to wrap Container functionality. """

    def __init__(self, url, cert, key):
        """ Configure logging. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        self.p.debug("Using LXD API config:\n"
                     "     URL: %s\n"
                     "     Cert: %s\n"
                     "     Key: %s" % (url, cert, key))

        # Create an LXD client instance.
        self.lxd = Client(
            endpoint=url,
            cert=(cert, key),
            verify=False
        )

        return

    def list(self):
        """ Function to list a qb containers. """

        # Define table headers and populate data.
        headers = ['NAME', 'IMAGE', 'STATE', 'CREATED']
        data = []

        for container in self.lxd.containers.all():
            # "container" is an impartial object so we must call fetch before
            # any operations.
            container.fetch()

            # Parse and format the "created_at" timestamp.
            parsed_created_at = dateutil.parser.parse(str(container.created_at))
            formatted_created_at = parsed_created_at.strftime(
                "%d/%m/%Y at %H:%M:%S")

            data.append([container.name,
                         'tbc',
                         container.status,
                         formatted_created_at])

        # Print the populated table.
        print(tabulate(tabular_data=data,
                       headers=headers,
                       tablefmt='simple'))

        return

    def create(self, name, image):
        """ Create a qb container. """

        # TODO: Pull config from elsewhere using 'image'.
        # Create the LXD API JSON payload.
        config = {
            'name': '%s' % name,
            'architecture': 'x86_64',
            'profiles': [
                'default'
            ],
            'ephemeral': False,
            'config': {
                'limits.cpu': '2'
            },
            'source': {
                'type': 'image',
                'mode': 'pull',
                'protocol': 'simplestreams',
                'server': 'https://cloud-images.ubuntu.com/releases',
                'alias': '%s' % image
            }
        }

        # Create the container.
        try:
            self.p.info(
                "Creating %s from the %s image..." % (name, image))
            container = self.lxd.containers.create(config, wait=True)
            self.p.info("Done!")

        except:
            self.p.error("Failed to create container.")
            sys.exit(1)

        # Start the container.
        self.start(name)

        return

    def start(self, name):
        """ Start a qb container. """

        try:
            container = self.lxd.containers.get(name)

        except:
            self.p.error("Failed to get container.")
            sys.exit(1)

        try:
            self.p.info("Starting %s..." % name)
            container.start(wait=True)
            self.p.info("Done!")

        except:
            self.p.error("Failed to start container.")
            sys.exit(1)

        return

    def stop(self, name):
        """ Stop a qb container. """

        try:
            container = self.lxd.containers.get(name)

        except:
            self.p.error("Failed to get container.")
            sys.exit(1)

        try:
            self.p.info("Starting %s..." % name)
            container.start(wait=True)
            self.p.info("Done!")

        except:
            self.p.error("Failed to start container.")
            sys.exit(1)

        return

    def remove(self, name):
        """ Remove a qb container. """

        self.p.debug("Removing \"%s\"..." % name)

        return
