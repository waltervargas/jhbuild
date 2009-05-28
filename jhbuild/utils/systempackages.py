# jhbuild - a build script for GNOME 1.x and 2.x
# Copyright (C) 2009  Codethink Ltd.
#
#   systempackage.py:  Infrastructure for interacting with installed packages
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Authors:
#   John Carr <john.carr@unrouted.co.uk>


class SystemPackages(object):

    def satisfiable(self, name, module):
        """ Returns true if a module is satisfiable by installing a system package """
        return self.is_available(name)

    def satisfied(self, name, module):
        """ Returns true if module is satisfied by an already installed system package """
        return self.is_installed(name)

    def is_installed(self, name, version=None):
        return False

    def is_available(self, name, version=None):
        return False

    def install(self, names):
        raise UnimplementedError

    def remove(self, names):
        raise UnimplementedError

    def supported(cls):
        return False
    supported = classmethod(supported)


class PackageKitPackages(SystemPackages):
    pass


class DebianPackages(SystemPackages):

    def install(self, names):
        buildscript.execute(['apt-get', 'install', ' '.join(name)])

    def remove(self, names):
        buildscript.execute(['apt-get', 'remove', ' '.join(name)])

    def supported(cls):
        return True
    supported = classmethod(supported)


def get_system_packages():
    for c in SystemPackages.__subclasses__():
        if c.supported():
            return c()
    return SystemPackages()


