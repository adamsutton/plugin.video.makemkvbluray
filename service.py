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
import xbmc, xbmcaddon

# Addon info
__addon__     = xbmcaddon.Addon()
__cwd__       = __addon__.getAddonInfo('path')
sys.path.append(xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib')))

# Local imports
import plugin, makemkv, makemkvcon
plugin.log('starting service')

# Settings
BDDIR = 'BDMV'

# Check for makemkvcon
if not makemkvcon.installed():
  plugin.notify(plugin.lang(50001))

# Service loop
key_checked  = 0
disc_current = None
disc_started = 0
disc_ready   = False
while not xbmc.abortRequested:
  plugin.log('run')

  # Update fixed key
  key = plugin.get('license_key')
  if key:
    makemkv.set(makemkv.APP_KEY, key)

  # Check for beta key
  elif plugin.get('license_beta_auto'):
    period = int(plugin.get('license_beta_period')) * 3600
    now    = time.time()
    if now - key_checked > period:
      if makemkv.updateLicense():
        plugin.notify(plugin.lang(50002))
      key_checked = now

  # Disc removed
  if disc_current:
    path = os.path.join('/media', disc_current, BDDIR)
    if not os.path.exists(path):
      plugin.notify(plugin.lang(50005) % disc_current)
      makemkvcon.kill()
      disc_current = None
      disc_ready   = False

  # Check for disc
  if plugin.get('disc_autoload') and not disc_ready:

    # Wait
    if disc_current:
      if makemkvcon.ready():
        disc_ready = True
        plugin.notify(plugin.lang(50004) % disc_current)
        if plugin.get('disc_autostart'):
          plugin.start()
      elif (time.time() - disc_started) > int(plugin.get('disc_timeout')):
        plugin.notify(plugin.lang(50006) % disc_current)
        disc_ready = True # stop watching

    # Check for new
    else:
      for d in os.listdir('/media'):
        p = os.path.join('/media', d, BDDIR)
        if os.path.exists(p):
          try:
            makemkvcon.start()
            disc_current = d
            disc_started = time.time()
            plugin.notify(plugin.lang(50003) % disc_current)
          except Exception, e:
            plugin.log('ERROR: %s' % e)
          break

    # Wait
  xbmc.sleep(5000)
