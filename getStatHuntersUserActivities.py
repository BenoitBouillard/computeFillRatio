from pprint import pprint
import argparse
import os
import json
from urllib.request import urlretrieve
from functools import wraps
import time

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry
    
@retry(Exception, tries=6, delay=60, backoff=2)
def myurlretrieve(url, filename=None, reporthook=None, data=None):
    return urlretrieve(url, filename, reporthook, data)

def getStatHuntersUserActivities(username, sharelink):
    if not os.path.exists(username):
        os.makedirs(username)
        
    page = 1
    while True:
        # https://www.statshunters.com/share/b83b3a6d86d5
        filepath = os.path.join(username, "activities_{}.json".format(page))
        url = sharelink+"/api/activities?page={0}".format(page)
        print("Get page {} ({})".format(page, url))
        myurlretrieve(url, filepath)
        with open(filepath) as f:
            d = json.load(f)
            if len(d['activities'])==0:
                break
        page += 1
        
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
    parser.add_argument('-n','--name', dest="username", help="User name for saving data")
    parser.add_argument('-s','--sharelink', dest="sharelink", help="Stathunters share link to recover data")
    args = parser.parse_args()

    username          = vars(args)['username']
    sharelink         = vars(args)['sharelink']
    
    getStatHuntersUserActivities(username, sharelink)

