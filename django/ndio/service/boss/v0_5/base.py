﻿# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ndio.service.boss.baseversion import BaseVersion
from . import BOSS_VERSION

class Base(BaseVersion):
    """This is the common parent for all interfaces to the Boss v.05.

    Attributes:
        _token (string): Django Rest Framework token used for auth.
    """

    def __init__(self):
        super().__init__()
        self._token = None

    @property
    def version(self):
        """Version of the Boss API supported by this service instance.

        Returns:
            (string): Boss API version.
        """
        return BOSS_VERSION
