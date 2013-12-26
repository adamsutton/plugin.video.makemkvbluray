#
# plugin.video.makemkvbluray - configuration/license processing
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

# Local imports
import plugin

# Settings
CONFPATH = os.path.expanduser('~/.MakeMKV/settings.conf')
CONF     = None
BETAURL  = 'http://www.makemkv.com/forum2/viewtopic.php?f=5&t=1053'
BETAEXP  = re.compile('<div class="codecontent">([^<]*)')

APP_KEY  = "app_Key"

#
# Load settings
#
def getAll ():
  global CONF
  if CONF is not None: return CONF
  ret = {}
  if os.path.exists(CONFPATH):
    exp = re.compile('([^ ]+) = "([^"]*)"')
    for l in open(CONFPATH):
      res = exp.search(l)
      if res:
        ret[res.group(1)] = res.group(2)
  CONF = ret
  return ret

#
# Get specific setting
#
def get ( key ):
  conf = getAll()
  if key in conf: return conf[key]
  return None

#
# Set setting
#
def set ( key, val ):

  # Create directories
  dirp = os.path.dirname(CONFPATH)
  if not os.path.exists(dirp):
    os.makedirs(dirp)

  # Create tmp file
  plugin.log('update makemkv config %s = %s' % (key, val))
  fp = open(CONFPATH + '.tmp', 'w')
  if os.path.exists(CONFPATH):
    for l in open(CONFPATH):
      if l.startswith(key): continue
      fp.write(l)
  fp.write('%s = "%s"\n' % (key, val))
  fp.close()

  # Replace
  if os.path.exists(CONFPATH):
    os.unlink(CONFPATH)
  os.rename(CONFPATH + '.tmp', CONFPATH)
  
#
# Get latest beta
#
def getBeta ():
  plugin.log('fetching beta key from %s' % BETAURL)
  for l in urllib.urlopen(BETAURL):
    res = BETAEXP.search(l)
    if res:
      plugin.log('latest beta key %s' % res.group(1))
      return res.group(1)
  plugin.log('no beta key found')
  return None

#
# Update the key
#
def updateLicense ():

  # Fetch latest key
  key = getBeta()

  # Nothing to update
  if not key: return False
  
  # Already up to date
  cur = get(APP_KEY)
  if cur == key: return False

  # Write tmpfile
  plugin.log('updating license key %s' % key)
  set(APP_KEY, key)
    
  return True
