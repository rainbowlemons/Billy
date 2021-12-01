#!/usr/bin/python

#billy is a python script that downloads files
import sys
import requests
import logging
import math

#setting up the logger and formatting for it
logger = logging.getLogger('billy')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

#converts the filesize from bytes
def convert_bytes(bytes):
    if bytes == 0:
       return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(bytes, 1024)))
    p = math.pow(1024, i)
    s = round(bytes / p, 2)
    return "%s%s" % (s, size_name[i])

#sends the request and gets the url
logger.info("Ready to download!")
url = sys.argv[1]
r = requests.get(url, stream = True)

#if there is an error connecting it logs it
if r.status_code != 200:
    logger.error("Status code: %s" % (r.status_code))

else:
    logger.info("Status code: %s" % (r.status_code))
    logger.info("Connection Sucessful")

#gets the filesize
    length = int(r.headers["Content-Length"])

#logs the converted filesize
    logger.info("The file size is " + convert_bytes(length))

    fname = ''

#gets the filename from the url
    if "Content-Disposition" in r.headers.keys():
        fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
    else:
        fname = url.split("/")[-1]

#writes to the file
    with open(fname, "wb") as f:
        #variable for curent amount of bytes downloaded
        dl = 0
        #downloads the file in chunks
        for chunk in r.iter_content(chunk_size=1000000):
            dl += len(chunk)
            f.write(chunk)
            #download progress and progress bar
            done = int(50 * dl / length)
            sys.stdout.write("\r\033[K[%s%s]" % ('=' * done, ' ' * (50-done)) + convert_bytes(dl) + "/" + convert_bytes(length))
            sys.stdout.flush()

print ("")
logger.info("Sucessfully downloaded: %s." % (fname))
