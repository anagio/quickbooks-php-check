import urlparse
import requests
from checks import AgentCheck
from util import headers
from config import _is_affirmative

class QuickBooksConnected(AgentCheck):

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)
        self.assumed_url = {}

    def check(self, instance):

        if 'quickbooks_diagnostics_url' not in instance:
            raise Exception("Missing 'quickbooks_diagnostics_url' in config")

        url = self.assumed_url.get(instance['quickbooks_diagnostics_url'], instance['quickbooks_diagnostics_url'])

        connect_timeout = int(instance.get('connect_timeout', 5))
        receive_timeout = int(instance.get('receive_timeout', 15))

        disable_ssl_validation = _is_affirmative(instance.get('disable_ssl_validation', False))

        parsed_url = urlparse.urlparse(url)
        quickbooks_host = parsed_url.hostname
        quickbooks_port = parsed_url.port or 80
        service_check_name = 'quickbooks.connected'
        service_check_tags = ['host:%s' % quickbooks_host, 'port:%s' % quickbooks_port]

        auth = None
        try:
            self.log.debug('quickbooks check initiating request, connect timeout %d receive %d' %
                           (connect_timeout, receive_timeout))
            r = requests.get(url, auth=auth, headers=headers(self.agentConfig),
                             verify=not disable_ssl_validation, timeout=(connect_timeout, receive_timeout))
            r.raise_for_status()

        except Exception as e:
            self.log.warning("Caught exception %s" % str(e))
            self.service_check(service_check_name, AgentCheck.CRITICAL,
                               tags=service_check_tags)
            raise
        else:
            response = r.content

            test_status = 0
            for line in response.splitlines():
                values = line.strip().split(' => ')
                if len(values) == 2:
                    metric, value = values
                    if metric == '[test]' and value is '1':
                        print(metric, value)
                        test_status += 1

            if test_status == 0:
                self.service_check(service_check_name, AgentCheck.CRITICAL,
                                   tags=service_check_tags)
            else:
                self.service_check(service_check_name, AgentCheck.OK,
                                   tags=service_check_tags)

        self.log.debug("quickbooks check succeeded")