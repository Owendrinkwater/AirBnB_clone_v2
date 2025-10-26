#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives
"""

from fabric.api import env, local, run
from os import listdir
from os.path import join

env.hosts = ['142.44.167.228', '144.217.246.195']


def do_clean(number=0):
    """
    Deletes out-of-date archives.
    """
    number = int(number)

    # if number is 0 or 1, keep only the most recent archive
    if number <= 1:
        number = 1

    # --- Clean local archives in versions/ ---
    archives = sorted(listdir("versions"))
    archives_to_delete = archives[:-number]  # all except last N

    for archive in archives_to_delete:
        local("rm -f versions/{}".format(archive))

    # --- Clean remote releases on each server ---
    releases = run("ls -1t /data/web_static/releases").split()
    # Keep only folders starting with web_static_
    releases = [f for f in releases if f.startswith("web_static_")]
    releases_to_delete = releases[number:]  # skip latest N

    for release in releases_to_delete:
        run("rm -rf /data/web_static/releases/{}".format(release))
