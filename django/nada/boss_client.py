from ndio.remote.boss.remote import Remote, LATEST_VERSION
from ndio.ndresource.boss.resource import CollectionResource, ExperimentResource, ChannelResource

from django.conf import settings

# TheBoss connection requires a valid login token
# provided in '../theboss.cfg'
#
# Generate a new token at https://api.theboss.io/token/


class BossClient:
    def __init__(self):
        self.remote = self.create_remote()

    def create_remote(self):
        self.api_version = LATEST_VERSION
        rmt = Remote(settings.THEBOSS_CONFIG)
        rmt.group_perm_api_version = self.api_version

        # Turn off SSL cert verification.  This is necessary for interacting with
        # developer instances of the Boss.
        import requests
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        rmt.project_service.session_send_opts = { 'verify': False }
        rmt.metadata_service.session_send_opts = { 'verify': False }
        rmt.volume_service.session_send_opts = { 'verify': False }
        return rmt

    def remote_get(self, resource):
        return self.remote.project_get(resource)

    def get_collection(self, collection_name):
        collection = CollectionResource(collection_name, version=self.api_version)
        return self.remote_get(collection)

    def get_experiment(self, experiment_name, collection_name):
        experiment = ExperimentResource(experiment_name, collection_name, version=self.api_version)
        return self.remote_get(experiment)

    def get_channel(self, channel_name, collection_name, experiment_name):
        channel = ChannelResource(channel_name, collection_name, experiment_name, version=self.api_version)
        return self.remote_get(channel)
