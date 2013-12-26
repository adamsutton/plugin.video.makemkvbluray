#
# plugin.video.makemkvbluray
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

# ############################################################################
# Module Setup/Info
# ############################################################################

# Global imports
import os, sys, time
import urlparse
import xbmc, xbmcaddon, xbmcplugin, xbmcgui

# Addon info
__addon__     = xbmcaddon.Addon()
__cwd__       = __addon__.getAddonInfo('path')
sys.path.append(xbmc.translatePath(os.path.join(__cwd__, 'lib')))

# Local imports
import plugin, makemkv, makemkvcon

# Add directory
def addDir ( name, url, icon = '', folder = False):
  li = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
  li.setInfo(type='Video', infoLabels={ 'Title' : name })
  xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li)

# Add link
def addLink ( name, url, icon = '' ):
  url = sys.argv[0] + url
  li  = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
  li.setInfo(type='Video', infoLabels={ 'Title' : name })
  xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li)

# Add a title
def addTitle ( title, icon = 'DefaultVideo.png' ):
  name = 'Title %d [%s]' % (title['id'], title['duration'])
  url  = title['file0']
  li  = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
  li.setInfo(type='Video', infoLabels={ 'Title' : name })
  li.setProperty('IsPlayable', 'true')
  xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li)

# Parse query string
def parseQuery ():
  ret = {}
  if sys.argv[2].startswith('?'):
    tmp = urlparse.parse_qs(sys.argv[2][1:])
    for k in tmp:
      ret[k] = tmp[k][0]
  return ret

# Play a title
def playTitle ( title ):
  plugin.log('playing %s' % title['file0'])
  xbmc.executebuiltin('PlayMedia("%s")' % title['file0'])

# Check installed
plugin.log('checking makemkvcon installed')
if not makemkvcon.installed():
  plugin.notify(plugin.lang(50001))
  sys.exit(1)

# Start
if not plugin.get_bool('disc_autoload'):
  plugin.log('start makemkvcon')
  makemkvcon.start()
    
# Check that service is running
st = time.time()
ok = False
# TODO: dialog
while not ok and (time.time() - st) < plugin.get_int('disc_timeout'):
  plugin.log('waiting for makemkvcon')
  ok = makemkvcon.ready()
  time.sleep(0.5)
if not ok:
  plugin.notify(plugin.lang(50006))
  sys.exit(1)

# Process
params = parseQuery()

# Get titles
titles = makemkvcon.listTitles()
plugin.log('titles = %s' % str(titles))
if not titles:
  plugin.notify(plugin.lang(50007))

# List?
if not plugin.get_bool('disc_autoplay'):
  for t in titles:
    addTitle(t)
  xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Play longest
else:
  title = None
  for t in titles:
    if not title or t['length'] > title['length']:
      title = t
  playTitle(title)
