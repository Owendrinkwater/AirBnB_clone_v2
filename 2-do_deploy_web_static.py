#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['54.174.248.63', '18.206.206.78']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Deploys an archive to the web servers
    """
    if not exists(archive_path):
        return False
    
    file_name = archive_path.split("/")[-1]
    folder_name = file_name.split(".")[0]
    release_path = "/data/web_static/releases/{}".format(folder_name)

    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        return True
    except Exception:
        return False
