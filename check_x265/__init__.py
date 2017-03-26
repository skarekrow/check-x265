#!/usr/bin/env python3
# Python 3 version of @steelbox's script at https://github.com/steelbox/check-x265
import sys
import glob
import os
import fnmatch
import itertools as it
import subprocess as su
import functools
from pymediainfo import MediaInfo
from datetime import datetime

def match_all(dir, match):
    for root_dir, dirnames, filenames in os.walk(dir):
        filter_partial = functools.partial(fnmatch.filter, filenames)

        for filename in it.chain(*map(filter_partial, match)):
            yield os.path.join(root_dir, filename)

def run(dir):
    matches = []
    date = datetime.utcnow().strftime("%Y-%m-%d")

    if not os.path.isdir(dir):
        exit("Directory doesn't exist.")

    print("Making list of files that are not x265.")
    for file in match_all(dir, ["*.mp4", "*.mkv"]):
        mediainfo = MediaInfo.parse(file)

        try:
            codec = [x.codec for x in mediainfo.tracks if x.track_type == "Video"][0]
        except IndexError:
            pass
        
        if "HEVC" not in codec:
            matches.append(file)

    if matches:
        home = os.environ.get("HOME")
        with open("{}/x265_report_{}.txt".format(home, date), encoding="utf-8", mode="w") as f:
            for match in matches:
                try:
                    match += "\n"
                    f.write(match)
                except UnicodeEncodeError:
                    match = "{}\n".format(match.encode("utf-8", "surrogateescape"))
                    f.write(match)

        print("Your report is ready at: {}/x265_report_{}.txt\n".format(home, date))
    else:
        print("All files found were encoded with x265 (HEVC)")

def main():
    if sys.version_info < (3,):
        exit("Please use Python 3")

    if len(sys.argv) >= 2:
        run(sys.argv[1:])
    else:
        print("Please supply a location to scan.")
        exit("Usage: check-x265 /the/path/to/scan")
