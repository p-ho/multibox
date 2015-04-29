#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    MULTIBOX - This program is a frontend to DropboxD that
#     enables you to access more than one Dropbox at a time.
#    Copyright (C) 2015 Paul Hofmann
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#########################################################################################
#                                      Imports                                          #
#########################################################################################
from __future__ import print_function

import sys, os, subprocess, signal
from optparse import OptionParser
#########################################################################################
#                                      Globals                                          #
#########################################################################################
__version_info__ = ('0', '2', '1')
__version__ = '.'.join(__version_info__)

XAUTHORITY_FILENAME = '.Xauthority'
DROPBOX_CONF_FILENAME = '.dropbox'
HOME_VARNAME = 'HOME'
DISPLAY_VARNAME = 'DISPLAY'

EXIT_SUCCESS = 0
ERROR_HOME_VAR_NOT_SET = 50
ERROR_DROPBOX_LOCATION_DOES_NOT_EXIST = 51
ERROR_NEW_INSTANCE_IN_CONTENT_PATH = 52
ERROR_DROPBOX_LOCATION_SET_TO_HOME = 53

dropboxd_p = None
is_process_async = False
#########################################################################################
#                                  Helper Functions                                     #
#########################################################################################
def _normalize_path(path):
    return os.path.normcase(os.path.normpath(os.path.abspath(path)))

def _is_in_path_of_dropbox_content(path):
    curr_path = path
    curr_path_remainder = None
    while curr_path_remainder != '':
        dropbox_config_file = os.path.join(curr_path, DROPBOX_CONF_FILENAME)
        if os.path.isfile(dropbox_config_file):
            return True
        curr_path, curr_path_remainder = os.path.split(curr_path)
    return False

def _on_finalize(flag_async):
    global dropboxd_p
    if not flag_async:
        if dropboxd_p is not None:
            try:
                dropboxd_p.send_signal(signal.SIGTERM)
            except OSError:
                pass

def _on_signal(signum, frame):
    print("Interrupted by signal %i" % signum, file=sys.stderr)
    sys.exit(EXIT_SUCCESS)
#########################################################################################
#                                  Exposed Functions                                    #
#########################################################################################
def multibox_startup(dropbox_path, home_path, flag_force, flag_nogui, flag_async):
    global dropboxd_p
    dropbox_path = _normalize_path(dropbox_path)
    home_path = _normalize_path(home_path)

    dropbox_xauthority_path = os.path.join(dropbox_path, XAUTHORITY_FILENAME)
    home_xauthority_path = os.path.join(home_path, XAUTHORITY_FILENAME)

    if flag_force:
        print("[WARN] Issued force option. NO checks will be executed beforehand.", file=sys.stderr)
    else:
        if not os.path.exists(dropbox_path):
            print("[ERR] Dropbox location does not exist.", file=sys.stderr)
            sys.exit(ERROR_DROPBOX_LOCATION_DOES_NOT_EXIST)
        if not os.path.exists(home_path):
            print("[WARN] Home directory does not exist.", file=sys.stderr)
        if _is_in_path_of_dropbox_content(dropbox_path):
            print("[ERR] Do you really want to create a Dropbox instance inside another one? " +
                  "That might be a bad idea. If you're still sure you want to that, use the option '--force'.", file=sys.stderr)
            sys.exit(ERROR_NEW_INSTANCE_IN_CONTENT_PATH)
        if dropbox_path == home_path:
            print("[ERR] HOME cannot be a Dropbox location.", file=sys.stderr)
            sys.exit(ERROR_DROPBOX_LOCATION_SET_TO_HOME)

    if not flag_nogui:
        if (not os.path.exists(dropbox_xauthority_path)) and (os.path.exists(home_xauthority_path)):
            os.symlink(home_xauthority_path, dropbox_xauthority_path)

    dropboxd_env = os.environ.copy()
    dropboxd_env[HOME_VARNAME] = dropbox_path  
    if flag_nogui:
        del dropboxd_env[DISPLAY_VARNAME]
    dropboxd_p = subprocess.Popen(['dropboxd'], env=dropboxd_env)

    print("Started dropboxd...")

    if flag_async:
        return EXIT_SUCCESS
    else:
        return dropboxd_p.wait()

def main():
    global dropboxd_p, is_process_async
    signal.signal(signal.SIGTERM, _on_signal)
    try:
        parser = OptionParser("multibox [options] <box_location>\n" +
                              " <box_location> must be the path of an existing, but preferably empty folder\n"+
                              " OR an already initialized Dropbox location.")
        parser.add_option('-g', '--nogui', action='store_true', dest='nogui', default=False, help="deactivates usage of X (unsets $DISPLAY)")
        parser.add_option('-f', '--force', action='store_true', dest='force', default=False, help="disables plausibility checks.")
        parser.add_option('-a', '--async', action='store_true', dest='async', default=False, help="forks dropboxd to background and returns. (no daemonizing)")
        parser.add_option('-V', '--version', action='store_true', dest='version', default=False, help="prints version.")

        (options, args) = parser.parse_args()  

        if options.version:
            print("multibox %s" % __version__)
            sys.exit(EXIT_SUCCESS)

        if len(args) != 1:
            parser.error("You need to specify the Dropbox location as argument. Try -h for help.")

        dropbox_path = args[0]
        home_path = os.environ.get(HOME_VARNAME, None)

        if home_path is None:
            print("[ERR] $HOME environment variable required.", file=sys.stderr)
            sys.exit(ERROR_HOME_VAR_NOT_SET)

        is_process_async = options.async

        return multibox_startup(dropbox_path=dropbox_path,
                                home_path=home_path,
                                flag_force=options.force,
                                flag_nogui=options.nogui,
                                flag_async=options.async)
    except KeyboardInterrupt:
        print("Interrupted by user.", file=sys.stderr)
    finally:
        _on_finalize(is_process_async)
        
def main_wrap():
    sys.exit(main())

if __name__ == '__main__':
    main_wrap()
