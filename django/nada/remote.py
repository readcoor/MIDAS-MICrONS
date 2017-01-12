# Same as BossRemote, except defaults
# to loading the local project configuration file

import os
from intern.remote.boss import BossRemote

DIR = os.path.dirname(__file__)
CONFIG = os.path.join(DIR, '..', 'theboss.cfg')

class Remote(BossRemote):
    def __init__(self, config_file=CONFIG):
        BossRemote.__init__(self, config_file)
