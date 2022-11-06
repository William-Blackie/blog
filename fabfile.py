import datetime
import os
import subprocess
from shlex import quote, split

from invoke import run as local
from invoke.exceptions import Exit
from invoke.tasks import task

PROJECT_DIR = "/app"
LOCAL_DATABASE_NAME = LOCAL_DATABASE_USERNAME = "wagtail"
PRODUCTION_APP_INSTANCE = "william-blackie-website"
PRODUCTION_DATABASE_NAME = PRODUCTION_DATABASE_USERNAME = "william_blackie_website"

def dexec(cmd, service="web"):
    return local(f"docker compose exec -T {quote(service)} bash -c {quote(cmd)}")


def sudexec(cmd, service="web"):
    return local(f"docker compose exec --user=root -T {quote(service)} bash -c {quote(cmd)}")

########
# Local
########

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

def restore_database_dump(c, database_dump_path):
    """
    Restore a database dump in the docker container
    """
    print(f"Restoring database dump from {database_dump_path}")
    subprocess.call(
        [
            "docker",
            "compose",
            "exec",
            "db",
            "bash",
            "-c",
            f"psql < {database_dump_path}"
        ]
    )

def drop_docker_db(c):
    """
    Drop the local database
    """

    subprocess.call(
        [
            "docker",
            "compose",
            "exec",
            "db",
            "dropdb",
            "-h",
            "db",
            "-U",
            LOCAL_DATABASE_USERNAME,
            LOCAL_DATABASE_NAME,
        ]
    )
    subprocess.call(
        [
            "docker",
            "compose",
            "exec",
            "db",
            "createdb",
        ]
    )

@task
def pull_production_data(c, app_instance=PRODUCTION_APP_INSTANCE):
    """
    Pull production data from fly.io
    """
    print(f"Pulling production data from {app_instance}")
    drop_docker_db(c)
    database_dump = get_fly_database_dump(c, app_instance)
    restore_database_dump(c, database_dump)
    createsuperuser = input("Do you want to create a superuser? (y/n) ").lower()
    if createsuperuser == "y":
        create_superuser(c)
    else:
        print("Skipping superuser creation")
    local(command=f"rm {database_dump}")

@task
def create_superuser(c):
    """
    Create a superuser in the local database
    """
    subprocess.call(
            [
                "docker",
                "compose",
                "exec",
                "web",
                "python",
                "manage.py",
                "createsuperuser",
            ]
        )

########
# fly
########
def get_fly_database_dump(c, app_instance):
    """
    Download a database dump
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    database_dump_file = f"database_dumps/{now}.dump"
    db_url = get_fly_variable(c, app_instance, "DATABASE_URL") 
    local(f"fly ssh console -a {app_instance} -C 'pg_dump --no-owner {db_url}' > {database_dump_file}")
    local(f"chmod -R 775 {database_dump_file}")
    print(f"Database dump saved to {database_dump_file}")
    return database_dump_file

def get_fly_variable(c, app_instance, variable_name):
    """
    Get a variable from the fly app instance
    """
    text =  subprocess.check_output(["fly", "ssh", "console", "-a", app_instance, "-C", 'env'], encoding="utf-8").strip()
    variables = dict(line.split("=", 1) for line in text.splitlines())
    return variables[variable_name]


def open_fly_shell(c, app_instance):
    """
    Open a shell on the fly app instance
    """
    subprocess.call(
        [
            "fly",
            "ssh",
            "console",
            "-a",
            app_instance,
        ]
    )

def run_fly_shell_command(c, app_instance, command):
    """"
    Run a command on the fly app instance
    """
    subprocess.call(
        [
            "fly",
            "ssh",
            "console",
            "-a",
            app_instance,
            "-C",
            command,    
        ]
    )

def open_fly_proxy(c, app_instance):
    """
    Open a proxy to the fly app instance
    """
    subprocess.call(
        [
            "fly",
            "proxy",
            "3001",
            "-a",
            app_instance,
        ]
    )

def run_fly_proxy_command(c, app_instance, command):
    """"
    Run a command on the fly app instance
    """
    subprocess.call(
        [
            "fly",
            "proxy",
            "-a",
            app_instance,
            "-C",
            command,
        ]
    )