#
# plugin.video.makemkvbluray - makemkvcon interaction
#
# Copyright (C) 2012 Adam Sutton <dev@adamsutton.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# Global imports
import os, sys, time
import urllib, re
import xbmc, xbmcaddon
from subprocess import Popen, PIPE, call

# Local imports
import plugin

# Addon info
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')

# State
MAKEMKVCON = None

#
# Check binary is installed
#
def installed ():
  path = plugin.get('makemkvcon_path', 'makemkvcon')
  plugin.log('makemkvcon_path = %s' % path)
  try:
    p = Popen(path, stdout=PIPE, stderr=PIPE)
    p = None
    return True
  except Exception, e:
    plugin.log('error = %s' % e)
  return False

#
# Kill instances
#
def kill ():
  global MAKEMKVCON
  if MAKEMKVCON:
    MAKEMKVCON.kill()
    MAKEMKVCON = None
  cmd = [ 'killall', '-KILL', 'makemkvcon' ]
  call(cmd)
  cmd[2] = cmd[2] + '.bin'
  call(cmd)

#
# Stream disc
#
# TODO: configurable disc number?
#
def start ():
  global MAKEMKVCON
  if MAKEMKVCON:
    return
  cmd        = plugin.get('makemkvcon_path', 'makemkvcon')
  cmd        = [ cmd, '-r', '--cache=128', 'stream', 'disc:0' ]
  MAKEMKVCON = Popen(cmd, stdout=PIPE, stderr=PIPE)
  return

#
# Check if stream is ready
#
def ready ():
  global MAKEMKVCON
  if not MAKEMKVCON: return False
  host = plugin.get('makemkv_host', 'localhost')
  port = int(plugin.get('makemkv_port', 51000))
  try:
    up   = urllib.urlopen('http://%s:%d' % (host, port))
    up.close()
    return True
  except Exception, e:
    #plugin.log('ERROR: %s' % e)
    pass
  return False
