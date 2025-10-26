#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env
from fabric.api import local, put, run
from datetime import datetime
import os

env.hosts = ['52.55.249.213', '54.157.32.137']
env.user = "ubuntu"


def do_pack():
    """Packs web_static into a .tgz archive"""
    if not os.path.exists("versions"):
        os.makedirs("versions")

    archive = "versions/web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S"))
    result = local("tar -cvzf {} web_static".format(archive))
    if result.failed:
        return None
    return archive


def do_deploy(archive_path):
    """Deploys an archive to the web servers"""
    if not os.path.exists(archive_path):
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

def deploy():
    """Creates and deploys archive"""
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive)
