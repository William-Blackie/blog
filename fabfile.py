import datetime
import os
import subprocess
from shlex import quote, split

from invoke import run as local
from invoke.exceptions import Exit
from invoke.tasks import task

PROJECT_DIR = "/app"
LOCAL_DATABASE_NAME = LOCAL_DATABASE_NAME = "wagtail"

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



########
# fly
########


def open_fly_shell(c, app_instance):
    subprocess.call(
        [
            "fly",
            "ssh",
            "console",
            "-a",
            app_instance,
        ]
    )
