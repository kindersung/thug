#!/usr/bin/env python
#
# Shellcode.py
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
import string
import struct
import logging
import pylibemu
from Debugger import Debugger

logging.basicConfig()

class Shellcode:
    log = logging.getLogger("Shellcode")
    emu = pylibemu.Emulator()

    def __init__(self, ctxt, ast, script, debug = False):
        self.script  = script
        self.ctxt    = ctxt
        self.ast     = ast
        self.offsets = set()

        if debug:
            self.log.setLevel(logging.DEBUG)
            
    def search_url(self, sc):
        offset = sc.find('http')
        
        if offset > 0:
            url = sc[offset:].split()[0]
            self.log.debug('[Shellcode] URL Detected: %s' % (url, ))

    def build_shellcode(self, s):
        try:
            shellcode = s.decode('utf-8')
        except:
            shellcode = s

        sc = b''
        try:
            for c in shellcode:
                sc += struct.pack('<H', ord(c))
        except:
            self.log.debug(traceback.print_exc())
            return None

        return sc

    def run(self):
        with Debugger() as dbg:
            vars = self.ctxt.locals
            #dbg.debugBreak()
            self.ctxt.eval(self.script)

            for name in self.ast.names:
                s      = None
                libemu = False

                if name in vars.keys():
                    s = vars[name]
                if not s:
                    continue
              
                self.log.debug("[Shellcode] Testing variable: %s" % (name, ))
                
                try:
                    shellcode = s.decode('utf-8')
                except:
                    shellcode = s

                sc = b''
                try:
                    for c in shellcode:
                        sc += struct.pack('<H', ord(c))
                except:
                    continue

                self.emu.run(sc)
                if self.emu.emu_profile_output:
                    self.log.warning(self.emu.emu_profile_output)
                    libemu = True

                self.emu.free()
                
                if not libemu:
                    self.search_url(sc)
