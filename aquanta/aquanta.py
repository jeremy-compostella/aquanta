# Author: Jeremy Compostella <jeremy.compostella@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer
#      in the documentation and/or other materials provided with the
#      distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

"""Aquanta water heater smart controller interface."""

import requests

class AquantaHelper:
    """GET, PUT and DELETE requests interface for Aquanta HTTP service."""

    API_BASE = 'https://api.aquanta.io'

    def __init__(self, session, timeout):
        self._session = session
        self._timeout = timeout

    def get(self, path):
        """GET HTTP request for aquanta.io PATH."""
        resp = self._session.get(self.API_BASE + path, timeout=self._timeout)
        if resp.ok:
            return resp.json()
        raise RuntimeError('Aquanta: Failed to GET %s, %s' % (path, resp))

    def put(self, path, value):
        """PUT HTTP request for aquanta.io PATH."""
        resp = self._session.put(self.API_BASE + path, json=value,
                                 timeout=self._timeout)
        if not resp.ok:
            raise RuntimeError('Aquanta: Failed to PUT %s' % path)

    def delete(self, path):
        """DELETE HTTP request for aquanta.io PATH."""
        resp = self._session.delete(self.API_BASE + path,
                                 timeout=self._timeout)
        if not resp.ok:
            raise RuntimeError('Aquanta: Failed to DELETE %s' % path)

class Aquanta():
    """Main interface to the Aquanta service.

    This class runs the authentication process with the aquanta server and
    provide a list of AquantaDevice objects to control aquanta devices
    independently.

    """
    GOOGLE_APIS = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty'
    KEY = 'AIzaSyBHWHB8Org9BWCH-YFzis-8oEbMaKmI2Tw'
    PORTAL_BASE = 'https://portal.aquanta.io/portal'

    def __init__(self, email, password, timeout = 5):
        self._timeout = timeout
        self._session = requests.Session()
        self._helper = AquantaHelper(self._session, self._timeout)
        self._devices = None
        self._authenticate(email, password)

    def _authenticate(self, email, password):
        resp = self._session.post(self.GOOGLE_APIS + '/verifyPassword?key=' +
                                  self.KEY,
                                  json=dict(email=email,
                                            password=password,
                                            returnSecureToken='true'),
                                  timeout=self._timeout)
        if not resp.ok:
            raise RuntimeError('Aquanta: Password verification failed')
        resp = self._session.post(self.PORTAL_BASE + '/login',
                                  json=dict(idToken=resp.json()['idToken']),
                                  timeout=self._timeout)
        if not resp.ok:
            raise RuntimeError('Aquanta: login failed')

    def devices(self):
        """Return the list of AquantaDevice of this account."""
        if not self._devices:
            devices = self._helper.get('/v2/devices')
            self._devices = {dev['id']:AquantaDevice(self._helper, dev['id']) \
                             for dev in devices}
        return self._devices

    def __len__(self):
        return len(self.devices())

    def __contains__(self, key):
        return key in self.devices().keys()

    def __iter__(self):
        return iter(self.devices().items())

    def __getitem__(self, key):
        return self.devices()[key]

class AquantaDevice:
    """Control and get information from an aquanta device."""

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, helper, device_id):
        self._helper = helper
        self._id = device_id

    def _path(self, name):
        return '/v2/devices/%d/%s' % (self._id, name)

    @property
    def water(self):
        """Return water tank information such as temperature or water level."""
        return self._helper.get(self._path('water'))

    @property
    def infocenter(self):
        """Return status information."""
        return self._helper.get(self._path('infocenter'))

    @property
    def advanced(self):
        """Return configuration settings."""
        return self._helper.get(self._path('advanced'))

    def set_boost(self, start, end):
        """Set boost mode time frame.

        START and END are two strings of UTC time formatted as
        "%Y-%m-%dT%H:%M:%S.000Z".

        """
        return self._helper.put(self._path('boost'),
                                {'start': start, 'end': end})

    def delete_boost(self):
        """Delete the boost time configuration."""
        self._helper.delete(self._path('boost'))

    def set_away(self, start, end):
        """Set away mode time frame.

        START and END are two strings of UTC time formatted as
        "%Y-%m-%dT%H:%M:%S.000Z".

        """
        print({'start': start, 'end': end})
        return self._helper.put(self._path('away'),
                                {'start': start, 'end': end})

    def delete_away(self):
        """Delete the away time configuration."""
        self._helper.delete(self._path('away'))

    @property
    def timer(self):
        """Return the timer configuration settings."""
        return self._helper.get(self._path('timer'))

    @timer.setter
    def timer(self, value):
        """Set the timer configuration settings."""
        self._helper.put(self._path('timer'), value)
