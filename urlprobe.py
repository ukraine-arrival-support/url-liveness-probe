import contentful
import urllib.request
import validators
from urllib.error import HTTPError, URLError
import socket
import logging
import io
import os


def getlist():
    # Set logger
    logger = logging.getLogger('basic_logger')
    logger.setLevel(logging.DEBUG)

    # Setup the console handler with a StringIO object
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.DEBUG)

    # Optionally add a formatter
    formatter = logging.Formatter(
        '• %(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)
    client = contentful.Client(
        os.environ['CONTENTFUL_SPACE_ID'],
        os.environ['CONTENTFUL_ACCESS_TOKEN']
    )

    # Get All records
    entries = client.entries({'limit': '1000'})

    for i in entries:
        valid = validators.url(i.url)
        if valid == True:
            try:
                hdr = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
                req = urllib.request.Request(i.url, headers=hdr)
                response = urllib.request.urlopen(req).getcode()
            except HTTPError as error:
                # Exclude permission denied error in https://warmes-bett.de
                if "warmes-bett.de" in i.url and error.code == 403:
                    print("skipping a known issue with URL: %s (error: %s)" % (i.url, error))
                    pass
                else:
                    logger.error('failed to fetch URL %s. Error: %s' %
                             (i.url, error))
            except URLError as error:
                if isinstance(error.reason, socket.timeout):
                    logger.error('socket timed out - URL %s', i.url)
                else:
                    logger.error(
                        'url: %s - some other error happened: %s', i.url, error)
        else:
            logger.error("%s: Invalid url" % i.url)

    # Pull the contents back into a string and close the stream
    log_contents = log_capture_string.getvalue()
    log_capture_string.close()

    return log_contents
