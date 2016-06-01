#!/usr/bin/env python3

import logging
import sys
import dateutil.parser

from pylxd import Client  # https://pylxd.readthedocs.io/
from tabulate import tabulate # https://pypi.python.org/pypi/tabulate


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

    def list(self):
        """ Function to list a qb containers. """

        # Define table headers and populate data.
        headers = ['Name', 'State', 'Architecture', 'Created']
        data = []

        for container in self.lxd.containers.all():
            # "container" is an impartial object so we must call fetch before
            # any operations.
            container.fetch()

            # Format the created_at.
            created_at = dateutil.parser.parse(container.created_at, )

            data.append([container.name,
                         container.status,
                         container.architecture,
                         created_at])

        # Print the populated table.
        print(tabulate(tabular_data=data,
                       headers=headers,
                       tablefmt='grid'))

    def create(self, name, image):
        """ Create a qb container. """

        # TODO: Pull config from elsewhere using 'name'.
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
                'alias': '14.04'
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
        try:
            self.p.info("Starting %s..." % name)
            container.start(wait=True)
            self.p.info("Done!")

        except:
            self.p.error("Failed to start container.")
            sys.exit(1)

        return container

    def start(self, name):
        """ Start a qb container. """

        self.p.info("Starting \"%s\"..." % name)

    def stop(self, name):
        """ Stop a qb container. """

        self.p.debug("Stopping \"%s\"..." % name)

    def remove(self, name):
        """ Remove a qb container. """

        self.p.debug("Removing \"%s\"..." % name)
