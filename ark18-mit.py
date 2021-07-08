import logging
from random import choice, randint

import mitmproxy.http

DEBUG = True

logger = logging.getLogger('ark18')
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('[%(asctime)s-%(name)s-%(levelname)s] %(message)s')

fh = logging.FileHandler('log-ark.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)

if DEBUG:
    logger.addHandler(fh)
logger.addHandler(sh)

logger.info('ark18 start v1.18/0')


def strs(*values, mid_char=' '):
    vs = [str(x) for x in values]
    return mid_char.join(vs)


class Ark18:
    intervals = [1832, 2324, 3726, 4649, 4117, 4648, 5027]
    content = '{"result":0,"message":"OK","interval":4649,"timeLeft":-1,"alertTime":600}'

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if 'hypergryph' in flow.request.pretty_host:
            logger.info(strs(flow.request.pretty_host, flow.request.pretty_url))
        else:
            logger.debug(strs(flow.request.pretty_host, flow.request.pretty_url))
        if flow.request.pretty_host == 'as.hypergryph.com' and \
                flow.request.pretty_url == 'https://as.hypergryph.com/online/v1/ping':
            logger.info('***Edit Minor Status***')

            logger.info(strs('->content', flow.response.data.content.decode(), '-' * 9))
            flow.response.text = '{"result":0,"message":"OK","interval":%d,"timeLeft":-1,"alertTime":600}' % \
                                 randint(1500, 4700)
            logger.info(strs('-' * 9, flow.response.data.content.decode(), 'content->'))
            return


addons = [
    Ark18()
]
