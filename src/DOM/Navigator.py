#!/usr/bin/env python
#
# Navigator.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA


import PyV8
import httplib2
import urlparse
import logging
from Personality import Personality
from Plugins import Plugins

log = logging.getLogger("Navigator")

class Navigator(PyV8.JSClass):
    def __init__(self, personality, window = None, debug = True):
        self.personality = Personality[personality]
        self.plugins     = Plugins  # An array of the plugins installed in the browser
        self._window     = window
        if debug:
            log.setLevel(logging.DEBUG)
      
    @property
    def window(self):
        return self._window

    @property
    def appCodeName(self):
        """
            The internal "code" name of the current browser
        """
        return self.personality['appCodeName']

    @property
    def appName(self):
        """
            The official name of the browser
        """
        return self.personality['appName']

    @property
    def appVersion(self):
        """
            The version of the browser as a string
        """
        return self.personality['appVersion']

    @property
    def userAgent(self):
        """
            The user agent string for the current browser
        """
        return self.personality['userAgent']

    @property
    def buildId(self):
        """
            The build identifier of the browser (e.g. "2006090803")
        """
        return ""               

    @property
    def cookieEnabled(self):
        """
            A boolean indicating whether cookies are enabled
        """
        return True

    @property
    def language(self):
        """
            A string representing the language version of the browser
        """
        return "en"

    @property
    def mimeTypes(self):
        """
            A list of the MIME types supported by the browser
        """
        return []

    @property
    def onLine(self):
        """
            A boolean indicating whether the browser is working online
        """
        return True

    @property
    def oscpu(self):
        """
            A string that represents the current operating system
        """
        return ""

    @property
    def platform(self):
        """
            A string representing the platform of the browser
        """
        return "Win32"

    @property
    def product(self):
        """
            The product name of the current browser (e.g. "Gecko")
        """
        return ""

    @property
    def productSub(self):
        """
            The build number of the current browser (e.g. "20060909")
        """
        return ""

    @property
    def securityPolicy(self):
        """
            An empty string. In Netscape 4.7x, returns "US & CA domestic policy" or "Export policy".
        """
        return ""

    @property
    def vendor(self):
        """
            The vendor name of the current browser (e.g. "Netscape6")
        """
        return ""

    @property 
    def vendorSub(self):
        """
            The vendor name of the current browser (e.g. "Netscape6")
        """
        return ""

    @property
    def appMinorVersion(self):
        return self.personality['appMinorVersion']

    @property
    def browserLanguage(self):
        return "en"

    @property
    def cpuClass(self):
        return "x86"

    @property
    def systemLanguage(self):
        return "en"

    @property
    def userLanguage(self):
        return "en"

    # Indicates whether the host browser is Java-enabled or not.
    def javaEnabled(self, *arg):
        return True

    # Lets code check to see if the document at a given URI is
    # available without using the network.
    def mozIsLocallyAvailable(self, *arg):
        return False

    # Sets a user preference.
    # self method is only available to privileged code, and you
    # should use XPCOM Preferences API instead.
    def preference(self, *arg):
        pass

    # Allows web sites to register themselves as a possible handler
    # for a given MIME type.
    def registerContentHandler(self, *arg):
        pass

    # New in Firefox 3
    # Allows web sites to register themselves as a possible handler
    # for a given protocol.
    def registerProtocolHandler(self, *arg):
        pass

    # Obsolete
    # Returns false. JavaScript taint/untaint functions removed in
    # JavaScript 1.2[1]
    def taintEnabled(self, *arg):
        return False

    def fetch(self, url):
        h = httplib2.Http('.cache')
        
        headers = {
            'cache-control' : 'no-cache',
            'user-agent'    :  self.userAgent,
            'referer'       :  self._window.url
        }
        
        if self._window.doc.cookie:
            headers['cookie'] = self._window.doc.cookie

        _url = urlparse.urlparse(url)
        if not _url.netloc:
            debug_msg = "[Navigator URL Translation] %s --> " % (url, )
            url = urlparse.urljoin(self._window.url, _url.path)
            debug_msg = "%s %s" % (debug_msg, url)
            log.debug(debug_msg)

        response, content = h.request(url, headers = headers)
        return response, content
