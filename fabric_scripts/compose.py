from fabric import task
from invoke import Collection

from ._common import project_path


@task()
def compose_up(ctx, daemon=False, rebuild=False):
    with ctx.cd(project_path(".")):
        command_prefix = "docker-compose"
        command_options = " --file docker-compose-local.yml --project-name=csv_statistics "
        command_suffix = "up"

        if daemon:
            command_suffix += " -d "

        if rebuild:
            command_suffix += " --build "

        command = command_prefix + command_options + command_suffix

        ctx.run(command, pty=True, replace_env=False)


@task()
def compose_down(ctx, volumes=False):
    with ctx.cd(project_path(".")):
        command = "docker-compose --file docker-compose-local.yml --project-name=csv_statistics down"
        if volumes:
            command = f"{command} -v"
        ctx.run(command, pty=True, replace_env=False)


compose_collection = Collection("compose")
compose_collection.add_task(compose_up, name="up")
compose_collection.add_task(compose_down, name="down")
