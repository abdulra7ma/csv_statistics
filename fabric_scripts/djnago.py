from fabric import task
from invoke import Collection

from ._common import project_path


@task()
def makemigrations(ctx, app_name=""):
    with ctx.cd(project_path(".")):
        ctx.run("python ./manage.py makemigrations", pty=True, replace_env=False)


@task()
def migrate(ctx):
    with ctx.cd(project_path(".")):
        ctx.run("python manage.py migrate", pty=True, replace_env=False)


@task()
def run_commnad(ctx, name):
    with ctx.cd(project_path(".")):
        ctx.run(f"python manage.py {name}", pty=True, replace_env=False)


django_collection = Collection("django")
django_collection.add_task(makemigrations, name="migrations")
django_collection.add_task(migrate, name="migrate")
django_collection.add_task(run_commnad, name="run")
