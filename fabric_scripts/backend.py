from fabric import task

from ._common import project_path


@task()
def backend_run(ctx):
    with ctx.cd(project_path(".")):
        ctx.run("WERKZEUG_DEBUG_PIN=off python manage.py runserver_plus 127.0.0.1:8000", pty=True, replace_env=False)


@task()
def docker_backend_run(ctx):
    with ctx.cd(project_path(".")):
        ctx.run("cp core/.env.example core/.env")
        ctx.run("WERKZEUG_DEBUG_PIN=off python manage.py runserver_plus 0.0.0.0:8000", pty=True, replace_env=False)


@task()
def backend_shell(ctx):
    with ctx.cd(project_path(".")):
        ctx.run("./manage.py shell_plus", pty=True, replace_env=False)


@task()
def backend_clean_pyc(ctx):
    with ctx.cd(project_path(".")):
        ctx.run("find . -name \\*.pyc -delete")
        ctx.run("find . -name \\*.pyo -delete")
