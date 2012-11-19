#
# plugin.video.makemkvbluray - General helper routines
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
import xbmc, xbmcaddon

# Addon info
__addon__     = xbmcaddon.Addon()
__addonid__   = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__author__    = __addon__.getAddonInfo('author')
__version__   = __addon__.getAddonInfo('version')
__cwd__       = __addon__.getAddonInfo('path')

#
# Log message
#
def log ( msg ):
  xbmc.log('%s - %s' % (__addonname__, msg))
  
#
# Notify XBMC user
#
def notify ( msg, image = "", timeout = 3000 ):
  if not image:
    image = os.path.join(__cwd__, 'icon.png')
  xbmc.executebuiltin('Notification("%s", "%s", "%d", "%s")' % (__addonname__, msg, timeout, image))

#
# Get setting
#
def get ( key, default = None ):
  val = __addon__.getSetting(key)
  if val is None or val == '': val = default
  return val

#
# Get language string
#
def lang ( key ):
  return __addon__.getLocalizedString(key)

#
# Start the plugin (called from service)
#
def start ():
  cmd = 'RunAddon("%s")' % __addonid__
  log(cmd)
  xbmc.executebuiltin(cmd)
