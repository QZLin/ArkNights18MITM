import logging

import mitmproxy.http

logger = logging.getLogger('ark18')
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('[%(asctime)s-%(name)s-%(levelname)s] %(message)s')

fh = logging.FileHandler('log-ark.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(sh)

logger.info('ark18 start v1.18/0')


def strs(*values, midchar=' '):
    vs = [str(x) + midchar for x in values]
    return ''.join(vs)[:-1]


class Ark18:

    # def request(self, flow: http.HTTPFlow) -> None:
    #     pass

    @staticmethod
    def response(flow: mitmproxy.http.HTTPFlow):
        if 'hypergryph' in flow.request.pretty_host:
            logger.info(strs(flow.request.pretty_host, flow.request.pretty_url))
        else:
            logger.debug(strs(flow.request.pretty_host, flow.request.pretty_url))
        if flow.request.pretty_host == 'as.hypergryph.com' and \
                flow.request.pretty_url == 'https://as.hypergryph.com/online/v1/ping':
            logger.info('***Edit Minor Status***')
            logger.info(strs('->content', flow.response.data.content.decode()))
            flow.response.set_text('{"result":0,"message":"OK","interval":4649,"timeLeft":-1,"alertTime":600}')
            logger.info(strs('content->', flow.response.data.content.decode()))
            return


addons = [
    Ark18()
]
