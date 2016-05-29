#!/usr/bin/env python3

import json
import logging
import sys

import requests


class Container(object):
    """ Class to wrap Container functionality. """

    def __init__(self, url, cert, key):
        """ Configure logging. """

        # Use the logger object created by Client.
        self.p = logging.getLogger('qb')

        # Make config available to functions.
        self.url = url
        self.cert = cert
        self.key = key

        self.p.debug("Using container config:\n"
                     "     URL: %s\n"
                     "     CERT: %s\n"
                     "     KEY: %s" % (self.url, self.cert, self.key))

    def check_http_status(self, response):
        """ Ensure a generic HTTP request status is OK. """

        # If the HTTP status is OK then return immediately.
        if response.ok:
            self.p.debug("%i - %s." % (response.status_code, response.text))
            return True

        # Otherwise, log the error and exit.
        self.p.error("%i - %s." % (response.status_code, response.text))

        sys.exit(1)

    def check_lxd_status(self, response):
        """ Check the LXD API response is OK. """

        # Ensure the generic HTTP response status is OK or exit.
        self.check_http_status(response)

        try:
            # Otherwise, parse the response text to JSON.
            response_json = json.loads(response.text)

            # Grab the LXD API status code and text.
            status_code = response_json["status_code"]
            status_text = response_json["status"]

        except:
            self.p.error("Failed to parse the LXD API response to JSON.")
            sys.exit(1)

        # Check the LXD API status code is good.
        self.p.debug("%i - %s." % (status_code, status_text))

        # 100 - 199: Resource state (started, stopped, ready, etc).
        if 100 <= status_code <= 199:
            return

        # 200 - 399: Positive result.
        elif 200 <= status_code <= 399:
            return

        # Log and exit on any failure or unexpected response.
        # 400 - 599: Negative result.
        # 600 - 999: Future use.
        else:
            self.p.error("%i - %s." % (status_code, status_text))

        sys.exit(1)

    def create(self, name, image):
        """ Create a qb container. """

        # TODO: Check to see if a container by "name" already exists.
        # TODO: Check to see if the payload exists.
        # TODO: Check to see if the image defined in the payload exists.
        # TODO: A mechanism to check system resources in Machine are suitable.

        self.p.debug("Creating \"%s\" from the \"%s\" image." % (name, image))

        headers = {'Content-Type': 'application/json'}

        # TODO: Pull the payload JSON from Git (or a DB?) based on 'image'.
        # Create the LXD API JSON payload.
        payload = {
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

        # Parse the payload to JSON.
        try:
            payload_json = json.dumps(payload)

        except:
            self.p.error("Error parsing LXD API payload to JSON.")
            sys.exit(1)

        # Execute the LXD API POST request.
        try:
            response = requests.post(
                "%s/containers" % self.url,
                verify=False,
                cert=(self.cert, self.key),
                data=payload_json,
                headers=headers
            )

        except:
            self.p.error('Failed to perform HTTP POST to LXD API.')
            sys.exit(1)

        self.check_lxd_status(response)

        self.p.info(
            "Created %s using the %s image." % (name, image))

    def start(self, name):
        """ Start a qb container. """

        pass

    def stop(self, name):
        """ Stop a qb container. """

        pass

    def remove(self, name):
        """ Remove a qb container. """

        pass
