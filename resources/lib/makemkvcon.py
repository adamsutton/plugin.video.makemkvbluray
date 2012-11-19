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
import subprocess
import xbmc, xbmcaddon

# Local imports
import plugin

# Addon info
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')

# State
MAKEMKVCON = None

#
# Get binary path
#
def bin_path ():
  path = plugin.get('makemkvcon_path')
  if not path:
    path = 'makemkvcon'
  return path

#
# Check binary is installed
#
def installed ():
  path = bin_path()
  plugin.log('makemkvcon_path = %s' % path)
  try:
    p = subprocess.Popen(path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = None
    return True
  except Exception, e:
    plugin.log('error = %s' % e)
  return False

#
# Kill instances
#
def kill ():
  return
  if MAKEMKVCON:
    MAKEMKVCON.kill()
    MAKEMKVCON = None
  subprocess.call('killall -9 makemkvcon', shell=True)
  subprocess.call('killall -9 makemkvcon.bin', shell=True)

#
# Stream disc
#
def start ():
  return
  if MAKEMKVCON:
    pass # TODO error
    return
  cmd        = bin_path()
  cmd        = [ cmd, '-r', '--cache=128', 'disc:0' ]
  MAKEMKVCON = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  return

#
# Check if stream is ready
#
def ready ():
  if not MAKEMKVCON: return False
  # TODO: wait for output
  # TODO: check port
  return False
