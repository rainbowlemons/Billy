#!/usr/bin/python

#billy is a python script that downloads files
import sys
import requests
import logging
import math
import argparse

parser = argparse.ArgumentParser(description='Billy, the simple file downloader.')
parser.add_argument('url', metavar='URL', type=str, help='url to the file you wish to download')
parser.add_argument('-o', metavar='filename', type=str, help= 'specify the filename')
args = parser.parse_args()

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
    unit_prefix_id = int(math.floor(math.log(bytes, 1024)))
    size = round(bytes / math.pow(1024, unit_prefix_id), 2)
    return "%s%s" % (size, size_name[unit_prefix_id])

#sends the request and gets the url
logger.info("Ready to download!")
url = args.url
request = requests.get(url, stream = True)

#if there is an error connecting it logs it
if request.status_code != 200:
    logger.error("Status code: %s" % (request.status_code))

else:
    logger.info("Status code: %s" % (request.status_code))
    logger.info("Connection Sucessful")

#gets the filesize
    length = int(request.headers["Content-Length"])

#logs the converted filesize
    logger.info("The file size is " + convert_bytes(length))

    fname = ''

    if args.o is None:
    #gets the filename from the url
        if "Content-Disposition" in request.headers.keys():
            fname = re.findall("filename=(.+)", request.headers["Content-Disposition"])[0]
        else:
            fname = url.split("/")[-1]

    #sets filename to o argument
    else:
        fname = args.o

    #writes to the file
    with open(fname, "wb") as f:
        #variable for curent amount of bytes downloaded
        bytes_downloaded = 0
        #downloads the file in chunks
        for chunk in request.iter_content(chunk_size=1000000):
            bytes_downloaded += len(chunk)
            f.write(chunk)
            #download progress and progress bar
            done = int(50 * bytes_downloaded / length)
            sys.stdout.write("\r\033[K[%s%s]" % ('=' * done, ' ' * (50-done)) + convert_bytes(bytes_downloaded) + "/" + convert_bytes(length))
            sys.stdout.flush()

    print ("")
    logger.info("Sucessfully downloaded: %s." % (fname))
