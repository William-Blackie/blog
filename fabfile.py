import datetime
import os
import subprocess
from shlex import quote, split

from invoke import run as local
from invoke.exceptions import Exit
from invoke.tasks import task

# Process .env file
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue
            var, value = line.strip().split("=", 1)
            os.environ.setdefault(var, value)

PROJECT_DIR = "/app"

PRODUCTION_APP_INSTANCE = ""
STAGING_APP_INSTANCE = ""

LOCAL_MEDIA_FOLDER = "{0}/media".format(PROJECT_DIR)
LOCAL_IMAGES_FOLDER = "{0}/media/original_images".format(PROJECT_DIR)
LOCAL_DATABASE_NAME = PROJECT_NAME = "wagtail"
LOCAL_DATABASE_USERNAME = "wagtail"
LOCAL_DATABASE_DUMPS_FOLDER = "{0}/database_dumps".format(PROJECT_DIR)


############
# Production
############


def dexec(cmd, service="web"):
    return local(f"docker compose exec -T {quote(service)} bash -c {quote(cmd)}")


def sudexec(cmd, service="web"):
    return local(f"docker compose exec --user=root -T {quote(service)} bash -c {quote(cmd)}")


@task
def build(c):
    """
    Build the development environment (call this first)
    """
    group = subprocess.check_output(["id", "-gn"], encoding="utf-8").strip()
    local("mkdir -p media database_dumps")
    local(f"chown -R $USER:{group} media database_dumps")
    local("chmod -R 775 media database_dumps")
    local("docker compose build web")
    local("docker compose stop")


@task
def start(c):
    """
    Start the development environment
    """
    local("docker compose up -d web")

    print(
        "Use `fab ssh` to enter the web container and run `djrun` to start the dev server"
    )


@task
def stop(c):
    """
    Stop the development environment
    """
    local("docker compose stop")


@task
def restart(c):
    """
    Restart the development environment
    """
    stop(c)
    start(c)


@task
def destroy(c):
    """
    Destroy development environment containers (database will lost!)
    """
    local("docker compose down")


@task
def ssh(c):
    """
    Run bash in the local web container
    """
    subprocess.run(["docker", "compose", "exec", "web", "bash"])


@task
def ssh_root(c):
    """
    Run bash as root in the local web container
    """
    subprocess.run(["docker", "compose", "exec", "--user=root", "web", "bash"])


@task
def psql(c, command=None):
    """
    Connect to the local postgres DB using psql
    """
    cmd_list = [
        "docker",
        "compose",
        "exec",
        "db",
        "psql",
        *["-d", LOCAL_DATABASE_NAME],
        *["-U", LOCAL_DATABASE_USERNAME],
    ]

    if command:
        cmd_list.extend(["-c", command])

    subprocess.run(cmd_list)
