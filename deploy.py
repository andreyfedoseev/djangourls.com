import os
from fabric.api import *
from fabric.contrib import files


CONFIG = {
    "production": dict(
        project_path="/srv/django/djangourls.com",
        git_branch="master",
        buildout_cfg="buildout.cfg",
        supervisor_program="djangourls.com",
#        supervisor_celery_program="djangourls.com-celery",
    ),
}


env.roledefs = {
    "production": [
        "djangourls.com",
    ],
}


HOSTS_TO_ROLES = {}
for role, hosts in env.roledefs.items():
    for host in hosts:
        HOSTS_TO_ROLES[host] = role


def get_config():
    return CONFIG[HOSTS_TO_ROLES[env.host]]


@task
def pull():
    config = get_config()
    with settings(user="django"):
        if not files.exists(config["project_path"]):
            run("mkdir {project_path}".format(**config))
            with settings(cwd=config["project_path"]):
                run("git init")
        with settings(cwd=config["project_path"]):
            files.upload_template(
                os.path.join(os.path.dirname(__file__), "configs", "git"),
                os.path.join(config["project_path"], ".git", "config")
            )
            run("git pull origin")
            run("git checkout {git_branch}".format(**config))


@task
def buildout():
    config = get_config()
    with settings(user="django"):
        with settings(cwd=config["project_path"]):
            if not files.exists(os.path.join(config["project_path"], "virtualenv")):
                run("virtualenv virtualenv")
            if not files.exists(os.path.join(config["project_path"], "bin", "buildout")):
                run("source ./virtualenv/bin/activate")
                run("python bootstrap.py")
            run("./bin/buildout -c %s" % config["buildout_cfg"])
            run("find . -name '*.pyc' -delete")


@task
def collectstatic():
    config = get_config()
    with settings(user="django"):
        with settings(cwd=config["project_path"]):
            run("./bin/django collectstatic -l --noinput")


@task
def restart_supervisor():
    config = get_config()
    with settings(user="django"):
        run("supervisorctl stop %s" % config["supervisor_program"])
        run("supervisorctl start %s" % config["supervisor_program"])


#@task
#def restart_supervisor_celery():
#    config = get_config()
#    with settings(user="django"):
#        run("supervisorctl stop %s" % config["supervisor_celery_program"])
#        run("supervisorctl start %s" % config["supervisor_celery_program"])


@task
def full():
    pull()
    buildout()
    collectstatic()
    restart_supervisor()
#    restart_supervisor_celery()


@task
def update_code():
    pull()
    restart_supervisor()
