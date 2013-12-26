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
# Check for running process
#
def running ():
  import glob
  for f in glob.glob('/proc/*/cmdline'):
    try:
      cl = open(f).read()
      if cl.startswith('makemkvcon.bin'):
        return True
    except: pass
  return False

#
# Kill instances
#
def kill ():
  MAKEMKVCON = None
  plugin.log('killing makemkvcon')
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
  if running():
    plugin.log('makemkvcon already running')
    return
  cmd        = plugin.get('makemkvcon_path', 'makemkvcon')
  cmd        = [ cmd, '-r', '--cache=128', 'stream', 'disc:0' ]
  MAKEMKVCON = Popen(cmd, stdout=PIPE, stderr=PIPE)
  return

#
# Get remote address
#
def getHostPort ():
  host = plugin.get('makemkv_host', 'localhost')
  port = int(plugin.get('makemkv_port', 51000))
  return 'http://%s:%d' % (host, port)

#
# Connect
#
def connect ( path = '/' ):
  plugin.log('connect to %s' % (getHostPort() + path))
  return urllib.urlopen(getHostPort() + path)

#
# Check if stream is ready
#
def ready ():
  try:
    up = connect()
    up.close()
    return True
  except Exception, e:
    plugin.log('ERROR: %s' % e)
    pass
  return False

#
# Fetch URL and extra key/val data
#
def fetchUrl ( path ):
  ret = {}
  exp = re.compile('<tr><td>(.*?)</td><td>(.*?)</td></tr>')
  up  = connect(path)
  for l in up:
    r = exp.search(l)
    if r:
      ret[r.group(1)] = r.group(2)
  return ret

#
# List individual title
#
def listTitle(num):
  ret = {}
  dat = fetchUrl('/web/title%d' % num)
  if 'duration' in dat:
    p = dat['duration'].split(':')
    ret['duration'] = dat['duration']
    ret['length']   = (int(p[0]) * 3600) + (int(p[1]) * 60) + int(p[2])
  for k in [ 'formatcount', 'chaptercount', 'id' ]:
    if k in dat:
      ret[k] = int(dat[k])
  exp = re.compile('">([^<]*)')
  for k in dat:
    if k.startswith('file'):
      r = exp.search(dat[k])
      if r:
        ret[k] = getHostPort() + r.group(1)
  return ret

#
# Fetch all titles
#
def listTitles():

  # Get title count
  dat = fetchUrl('/web/titles')
  num = 0
  if 'titlecount' in dat:
    num = int(dat['titlecount'])

  # Process each title
  ret = []
  for t in range(num):
    ret.append(listTitle(t))
  return ret
