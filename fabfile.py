from invoke import Collection  # isort:skip

from fabric_scripts.backend import (backend_clean_pyc, backend_run,
                                    backend_shell)
from fabric_scripts.compose import compose_collection
from fabric_scripts.djnago import django_collection
from fabric_scripts.pip_tools import pip_collection

namespace = Collection(
    compose_collection,
    pip_collection,
    django_collection,
)
namespace.add_task(backend_run, name="run")
namespace.add_task(backend_shell, name="shell")
namespace.add_task(backend_clean_pyc, name="clean-pyc")
