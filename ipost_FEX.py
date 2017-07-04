#!/usr/bin/env python

# Copyright (c) 2013 Insieme Networks, Inc. All rights reserved.

from __future__ import print_function
from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import TerminalFormatter
from jinja2 import Environment, FileSystemLoader
import argparse
import logging
import os
import shlex
import subprocess
import sys
import re
import requests
import time
import yaml

logging.basicConfig()
logger = logging.getLogger(__name__)


def pprint_xml(xml_str, color=False):
    proc = subprocess.Popen(shlex.split('xmllint --format -'),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    (stdout, stderr) = proc.communicate(xml_str)
    if color:
        text = highlight(stdout, XmlLexer(), TerminalFormatter())
    else:
        text = stdout
    print(text)


class RestError(Exception):
    pass


class ParseError(Exception):
    pass


class BatchError(Exception):
    pass


class RestServer(object):
    def __init__(self, host, port, color=False, dry_run=False):
        self._host = host
        self._port = port
        self._session = None
        self._color = color
        self._dry_run = dry_run

    def login(self, user, password):
        auth_data = '<aaaUser name="{user}" pwd="{password}"/>'.format(
            user=user, password=password)
        self._session = requests.Session()
        self.post('aaa_FEX.xml', auth_data, quiet=True)

    def post(self, url, data, quiet=False):
        full_url = 'http://{host}:{port}/{url}'.format(
            host=self._host, port=self._port, url=url)
        if not quiet:
            print('POST', full_url)
            print()
            pprint_xml(data, color=self._color)

        if not self._dry_run:
            r = self._session.post(full_url, data=data)
            if r.status_code != requests.codes.ok:
                print('Failed to post using URL:', full_url, file=sys.stderr)
                print('Response:', r.text, file=sys.stderr)
                raise RestError('Failed to post')

    def get(self, url, quiet=False):
        full_url = 'http://{host}:{port}/{url}'.format(
            host=self._host, port=self._port, url=url)
        if not quiet:
            print('GET', full_url)
            print()

        if not self._dry_run:
            r = self._session.get(full_url)
            if r.status_code != requests.codes.ok:
                print('Failed to get URL:', full_url, file=sys.stderr)
                print('Response:', r.text, file=sys.stderr)
                raise RestError('Failed to get')
            if not quiet:
                pprint_xml(r.text, color=self._color)

    def post_from_file(self, filename, quiet=False,
                       template_values={}):
        global jinja_env
        template = jinja_env.get_template(filename)
        rendered = template.render(**template_values)
        lines = rendered.split('\n')

        if len(lines) < 3:
            raise ParseError('Less lines')
        match = re.search('<!-- (.*) -->', lines[1])
        if not match:
            raise ParseError('No comment')
        url = match.group(1)
        self.post(url, '\r\n'.join(lines), quiet=quiet)

    def get_from_file(self, filename, quiet=False,
                      template_values={}):
        global jinja_env
        template = jinja_env.get_template(filename)
        rendered = template.render(**template_values)
        lines = rendered.split('\n')

        if len(lines) != 1:
            raise ParseError('More or less lines')
        url = lines[0].strip()
        self.get(url, quiet=quiet)
        
    def set_jinja_env(self, jinja_env_value):
        global jinja_env
        jinja_env = jinja_env_value
        
class BatchProcessor(object):
    def __init__(self, filename, dry_run=False, template_values=None):
        self._dry_run = dry_run
        self._template_values = template_values
        template = jinja_env.get_template(filename)
        rendered = template.render(**template_values)
        self.batch_data = yaml.load(rendered)
        if not ('posts' in self.batch_data or
                'gets' in self.batch_data or
                'actions' in self.batch_data):
            raise BatchError('No actions, posts or gets in the batch file')

    def process(self, server, quiet=False):
        if 'actions' in self.batch_data:
            self._process_actions(server, self.batch_data['actions'],
                                  quiet=quiet)
            return

        if 'posts' in self.batch_data:
            posts = self.batch_data['posts']
            if not isinstance(posts, list):
                raise BatchError('posts should contain a list of files')
            delay = self.batch_data.get('delay', 0)
            for count, post in enumerate(posts):
                if not quiet:
                    print('Posting from file', post)
                    print()
                server.post_from_file(post, quiet=quiet,
                                      template_values=self._template_values)
                if delay > 0 and count != len(posts) - 1:
                    if not quiet:
                        print('\nSleeping for {delay} seconds...'.
                              format(delay=delay))
                    time.sleep(delay)
                    if not quiet:
                        print()

        if 'gets' in self.batch_data:
            gets = self.batch_data['gets']
            delay = self.batch_data.get('delay', 0)
            for count, get in enumerate(gets):
                if not quiet:
                    print('Getting from file', get)
                    print()
                server.get_from_file(get, quiet=quiet,
                                     template_values=self._template_values)
                if delay > 0 and count != len(gets) - 1:
                    if not quiet:
                        print('\nSleeping for {delay} seconds...'.
                              format(delay=delay))
                    time.sleep(delay)
                    if not quiet:
                        print()

    def _post(self, server, file_name, quiet=False):
        if not quiet:
            print('Posting from file', file_name)
            print()
            server.post_from_file(file_name, quiet=quiet,
                                  template_values=self._template_values)

    def _get(self, server, file_name, quiet=False):
        if not quiet:
            print('Getting from file', file_name)
            print()
        server.get_from_file(file_name, quiet=quiet,
                             template_values=self._template_values)

    def _sleep(self, delay, predicate=None, quiet=False):
        if delay > 0 and (predicate is None or predicate()):
            if not quiet:
                print('\nSleeping for {delay} seconds...'.
                      format(delay=delay))
            if not self._dry_run:
                time.sleep(delay)
            if not quiet:
                print()

    def _process_actions(self, server, actions, quiet=False):
        for action in actions:
            sleep_before = action.get('sleep-before', 0)
            sleep_after = action.get('sleep-after', 0)
            self._sleep(sleep_before, quiet=quiet)
            assert action.get('type', None) is not None
            assert action.get('file', None) is not None
            if action['type'] == 'get':
                self._get(server, action['file'], quiet=False)
            elif action['type'] == 'post':
                self._post(server, action['file'], quiet=False)
            else:
                print('Unknown action', action['type'])
            self._sleep(sleep_after, quiet=quiet)


# TODO: Revisit this algorithm.
def merge_dict(master, other):
    """
    Merge the given two dictionaries recursively and return the result.
    """
    if isinstance(master, dict) and isinstance(other, dict):
        for key, value in other.iteritems():
            if isinstance(value, dict):
                if key not in master:
                    master[key] = value
                else:
                    master[key] = merge_dict(master[key], value)
            else:
                master[key] = value
    return master

if __name__ == '__main__':
    host = '10.52.248.234'
    port = 80
    user = 'admin'
    password = 'C1sco123'

    parser = argparse.ArgumentParser(
        description='Communicate with Insieme REST service')
    parser.add_argument('-L', '--list-profiles',
                        help='list available profiles', action="store_true")
    parser.add_argument('-o', '--profile', type=str,
                        help='name of the profile to use')

    parser.add_argument('-H', '--host', type=str,
                        help='hostname of the service')
    parser.add_argument('-P', '--port', type=int,
                        help='port of the service')

    parser.add_argument('-u', '--user', type=str,
                        help='authentication username')
    parser.add_argument('-p', '--password', type=str,
                        help='authentication password')

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument('-g', '--get', type=str,
                              help='filename containing GET URL')
    action_group.add_argument('-s', '--post', type=str,
                              help='filename containing POST URL and data')
    action_group.add_argument('-b', '--batch', type=str,
                              help='filename containing batch information')

    parser.add_argument('-t', '--template-values-string', type=str,
                        metavar='STRING',
                        help='template values as YAML string')
    parser.add_argument('-T', '--template-values-file', type=str,
                        metavar='FILE', help='template values as YAML file')

    parser.add_argument('-c', '--color',
                        help='colorize output', action='store_true')
    parser.add_argument('-i', '--interactive',
                        help='interactive mode', action='store_true')
    parser.add_argument('-q', '--quiet',
                        help='silent mode', action='store_true')
    parser.add_argument('-N', '--dry-run',
                        help='dry run mode', action='store_true')

    parser.add_argument('-r', '--repository', type=str,
                        help='repository path')

    args = parser.parse_args()

    # FIXME (2013-08-23, praveek6): Handle file not found error.
    with open(os.path.expanduser('~/.ipostrc'), 'r') as rc:
        rc_data = yaml.load(rc)

    profiles = rc_data.get('profiles', {})
    if args.list_profiles:
        if profiles:
            for profile in sorted(profiles.keys()):
                print(profile)
        else:
            print('No profiles found')
        sys.exit(0)

    current_profile = rc_data.get('default-profile', None)
    if args.profile is not None:
        current_profile = args.profile
    if current_profile is not None:
        profile = profiles.get(current_profile, None)
        if profile is None:
            print('Profile {profile} unavailable'.
                  format(profile=current_profile))
            sys.exit(1)
        host = '10.52.248.234'
        port = profile.get('port', port)
        user = profile.get('user', user)
        password = profile.get('password', password)

    repository = rc_data.get('repository', '.')

    if args.host is not None:
        host = args.host
    if args.port is not None:
        port = args.port
    if args.user is not None:
        user = args.user
    if args.password is not None:
        password = args.password

    if args.repository is not None:
        repository = args.repository
    repository = os.path.realpath(os.path.expanduser(repository))
    if not os.path.isdir(repository):
        print('Repository doesn\'t exist:', repository, file=sys.stderr)
        sys.exit(1)
    else:
        global jinja_env
        jinja_env = Environment(loader=FileSystemLoader(repository))

    template_values = {}
    if args.template_values_file is not None:
        with open(os.path.expanduser(args.template_values_file), 'r') as f:
            template_values = yaml.load(f)

    if args.template_values_string is not None:
        override_values = yaml.load(args.template_values_string)
        template_values = merge_dict(template_values, override_values)

    server = RestServer(host, port, color=args.color, dry_run=args.dry_run)
    server.login(user, password)

    if args.get is not None:
        file_name = os.path.realpath(os.path.expanduser(args.get))
        relative_file_name = file_name.replace(repository + os.sep, '')
        server.get_from_file(relative_file_name, quiet=args.quiet,
                             template_values=template_values)
    elif args.post is not None:
        file_name = os.path.realpath(os.path.expanduser(args.post))
        relative_file_name = file_name.replace(repository + os.sep, '')
        #import pdb; pdb.set_trace()
        server.post_from_file(relative_file_name,
                              template_values=template_values)
        if args.interactive is not False:
            raw_input( 'Hit return to process' )
    elif args.batch is not None:
        file_name = os.path.realpath(os.path.expanduser(args.batch))
        relative_file_name = file_name.replace(repository + os.sep, '')
        processor = BatchProcessor(relative_file_name,
                                   dry_run=args.dry_run,
                                   template_values=template_values)
        processor.process(server, quiet=args.quiet)
    else:
        print('No action specified', file=sys.stderr)
        print()
        parser.print_help()
        sys.exit(1)
