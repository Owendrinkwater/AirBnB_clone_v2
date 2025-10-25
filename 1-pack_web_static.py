#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder.
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from web_static directory
    Stores the archive in versions directory
    Archive name format:
    web_static_<year><month><day><hour><minute><second>.tgz
    Returns: archive path if successful, otherwise None
    """
    # Create versions directory if not exists
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    # Format timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Archive name
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    # Create the archive
    result = local("tar -cvzf {} web_static".format(archive_path))

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_path
    return None
