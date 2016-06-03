#!/usr/bin/env python3

import logging
import sys

import yaml


class Config(object):
    """ Class to wrap qb configuration functionality. """

    def __init__(self):
        """ Configure logging. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        return

    def load(self, path):
        """ Load qb config from file. """

        try:
            # Open the config file, parse the contents to YAML and close it.
            config_file = open(path)
            config_dict = yaml.safe_load(config_file)
            config_file.close()

            # TODO: Check to ensure all required keys and values are present
            # and valid.

            return config_dict

        except Exception as e:
            self.p.debug(e)
            self.p.error("Failed to load config file (%s)." % path)
            sys.exit(1)

        return
