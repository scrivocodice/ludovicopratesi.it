import os

from contextlib import contextmanager
from fabric.api import cd, env, hide, prefix, run as _run, sudo, task
from fabric.colors import yellow, green, blue, red
from fabric.context_managers import settings
from fabric.contrib.files import exists, upload_template
from getpass import getpass

# ---------------------
# Variables definition
# ---------------------
env.roledefs = {
    'loc': ['localhost'],
    'pro': ['146.185.167.231']
}
env.user = 'pratesi'
env.locale = "en_US.UTF-8"
env.fabfile_dir = os.path.dirname(os.path.abspath(__file__))

# paths
env.proj_name = 'ludovicopratesi.it'
env.home_dir = os.path.join('/home', env.proj_name)
env.etc_dir = os.path.join(env.home_dir, 'etc')
env.var_dir = os.path.join(env.home_dir, 'var')
env.var_run_dir = os.path.join(env.var_dir, 'run')
env.var_log_dir = os.path.join(env.var_dir, 'log')
env.media_dir = os.path.join(env.home_dir, 'media')
env.proj_dir = os.path.join(env.home_dir, 'project')
env.static_dir = os.path.join(env.home_dir, 'static')
env.venv_dir = os.path.join(env.home_dir, '.virtualenv')
env.pip_requirements_path = os.path.join(env.proj_dir, 'requirements.txt')
env.manage = "%s/bin/python %s/manage.py" % (env.venv_dir, env.proj_dir)

# database
env.db_name = 'ludovicopratesi_db'
env.db_user = 'pratesi'
env.db_pass = '6ipQMDjM40'

# repository
env.repo_repository = 'origin'
env.repo_refspec = 'master'
env.repo_url = 'git@bitbucket.org:xm3ron/ludovicopratesi.git'

# nginx
env.live_host = env.proj_name
env.nginx_log_dir = os.path.join('/var', 'log', 'nginx', env.proj_name)

# supervisor
env.supervisor_log_dir = os.path.join('/var', 'log', 'supervisor', env.proj_name)

# gunicorn
env.gunicorn_log_dir = os.path.join('/var', 'log', 'gunicorn', env.proj_name)

# ------------
# Common task
# ------------
@task
def apt(packages):
    """
    Installs one or more system packages via apt.
    """
    return sudo("apt-get install -y -q " + packages)

@task
def run(command, show=True):
    """
    Runs a shell comand on the remote server.
    """
    if show:
        print_command(command)
    with hide("running"):
        return _run(command)

@task
def pip(packages):
    """
    Installs one or more Python packages within the virtual environment.
    """
    with virtualenv():
        return run("pip install %s" % packages)

@task
def psql(sql, show=True):
    """
    Runs SQL against the project's database.
    """
    out = postgres('psql -c "%s"' % sql)
    if show:
        print_command(sql)
    return out

def postgres(command):
    """
    Runs the given command as the postgres user.
    """
    show = not command.startswith("psql")
    return run("sudo -u root sudo -u postgres %s" % command)

@task
def manage(command):
    """
    Runs a Django management command.
    """
    return run("%s %s" % (env.manage, command))

def _print(output):
    print()
    print(output)
    print()

def print_command(command):
    _print(blue("$ ", bold=True) +
           yellow(command, bold=True) +
           red(" ->", bold=True))

######################################
# Context for virtualenv and project #
######################################

@contextmanager
def virtualenv():
    """
    Runs commands within the project's virtualenv.
    """
    with cd(env.venv_dir):
        with prefix("source %s/bin/activate" % env.venv_dir):
            yield

@contextmanager
def project():
    """
    Runs commands within the project's directory.
    """
    with virtualenv():
        with cd(env.proj_dir):
            yield

#########
# Nginx #
#########
@task
def nginx_init():
    local_path = os.path.join(env.fabfile_dir, 'etc', 'server', 'ludovicopratesi.it.nginx')
    remote_path = os.path.join('/', 'etc', 'nginx', 'sites-enabled', env.proj_name+'.conf')
    with settings(user = 'root'):
        upload_template(local_path, remote_path, env, use_sudo=False, backup=False)
        if not exists(env.nginx_log_dir):
            run("mkdir -p %s" % env.nginx_log_dir)

@task
def nginx_restart():
    with settings(user = 'root'):
        run("service nginx configtest")
        run("service nginx restart")

#################
# Supervisorctl #
#################
@task
def supervisor_init():
    local_path = os.path.join(env.fabfile_dir, 'etc', 'server', 'gunicorn.conf')
    remote_path = os.path.join('/', 'etc', 'supervisor', 'conf.d', env.proj_name+'.conf')
    upload_template(local_path, remote_path, env, use_sudo=True, backup=False)
    with settings(user = 'root'):
        if not exists(env.supervisor_log_dir):
            run("mkdir -p %s" % env.supervisor_log_dir)

def supervisor_start():
    with settings(user = 'root', warn_only=True):
        run("service supervisor start")

@task
def supervisor_reload():
    with settings(user = 'root'):
        run("supervisorctl reread")
        run("supervisorctl reload")

############
# Gunicorn #
############
@task
def gunicorn_init():
    if not exists(env.gunicorn_log_dir):
        sudo("mkdir -p %s" % env.gunicorn_log_dir)
        # TOFIX: remove pratesi and parametrize it!
        sudo("chown -R pratesi: %s" % env.gunicorn_log_dir)
    local_path = os.path.join(env.fabfile_dir, 'etc', 'server', 'conf.py')
    remote_path = os.path.join(env.etc_dir, 'conf.py')
    upload_template(local_path, remote_path, env, use_sudo=True, backup=False)

# -----------
# Init tasks
# -----------
@task
def init_apt_packages():
    """
    Installs the base system and Python requirements for the entire server.
    """
    env.user = 'root'
    locale = "LC_ALL=%s" % env.locale
    with hide("stdout"):
        if locale not in sudo("cat /etc/default/locale"):
            sudo("update-locale %s" % locale)
            run("exit")
    with settings(warn_only=True):
        run("adduser %s" % env.user)
    run("apt-get update --assume-yes --quiet")
    apt("git-core")
    apt("libjpeg-dev")
    apt("libpq-dev")
    apt("postgresql")
    apt("python-dev")
    apt("python-virtualenv")
    apt("nginx")
    apt("supervisor")

# -------------
# First Deploy
# -------------
@task
def first_deploy():
    prompt = input("\nAre you sure is your first deploy? If answer " + 
        "yes everythings will be destroyed before continue. (yes/no) \n")
    if prompt.lower() == 'yes':
        drop_folder_tree()
        drop_database()
        create_folder_tree()
        create_database()
        create_virtualenv()
        with cd(env.home_dir):
            run("git clone -b %s %s %s" % (env.repo_refspec, env.repo_url, env.proj_dir))
        with project():
            pip("-r %s" % (env.pip_requirements_path))
            manage("collectstatic -v 0 --noinput")
            # compress static files to create a unique versioned cache file
            manage("compress")
            manage("syncdb --noinput --all")
        servers_init()
        servers_run()
        create_log_symlinks()

def create_folder_tree():
    """
    Create project folder tree
    """
    run("mkdir %s" % env.media_dir)
    run("mkdir %s" % env.proj_dir)
    run("mkdir %s" % env.static_dir)
    run("mkdir %s" % env.venv_dir)
    run("mkdir %s" % env.var_dir)
    run("mkdir %s" % env.var_log_dir)
    run("mkdir %s" % env.var_run_dir)
    run("mkdir %s" % env.etc_dir)

def drop_folder_tree():
    """
    Drop project folder tree
    """
    run("rm -rf %s" % env.media_dir)
    run("rm -rf %s" % env.proj_dir)
    run("rm -rf %s" % env.static_dir)
    run("rm -rf %s" % env.venv_dir)
    run("rm -rf %s" % env.var_dir)
    run("rm -rf %s" % env.var_log_dir)
    run("rm -rf %s" % env.var_run_dir)
    run("rm -rf %s" % env.etc_dir)

def create_database():
    """
    Create db and db user
    """
    with settings(user = 'root'):
        pw = db_pass()
        user_sql_args = (env.db_user, pw.replace("'", "\'"))
        user_sql = "CREATE USER %s WITH CREATEDB ENCRYPTED PASSWORD '%s';" \
            % user_sql_args
        psql(user_sql, show=False)
        shadowed = "*" * len(pw)
        print_command(user_sql.replace("'%s'" % pw, "'%s'" % shadowed))
        psql("CREATE DATABASE %s WITH OWNER %s ENCODING = 'UTF8' "
            "LC_CTYPE = '%s' LC_COLLATE = '%s' TEMPLATE template0;" %
            (env.db_name, env.db_user, env.locale, env.locale))

def db_pass():
    """
    Prompts for the database password if unknown.
    """
    if not env.db_pass:
        env.db_pass = getpass("Enter the database password: ")
    return env.db_pass

def drop_database():
    """
    Drop db and db user
    """
    with settings(user = 'root'):
        psql("DROP DATABASE IF EXISTS %s;" % env.db_name)
        psql("DROP USER IF EXISTS %s;" % env.db_user)

def create_virtualenv():
    with cd(env.venv_dir):
        run("virtualenv %s --distribute" % env.venv_dir)

@task
def servers_init():
    nginx_init()
    supervisor_init()
    gunicorn_init()

@task
def servers_run():
    supervisor_start()
    supervisor_reload()
    nginx_restart()

def create_log_symlinks():
    with cd(env.var_log_dir):
        run("rm -rf nginx && mkdir nginx")
        run("rm -rf supervisor && mkdir supervisor")
        run("rm -rf gunicorn && mkdir gunicorn")
        run("ln -s /var/log/nginx/%s/ nginx" % env.proj_name)
        run("ln -s /var/log/supervisor/%s/ supervisor" % env.proj_name)
        run("ln -s /var/log/gunicorn/%s/ gunicorn" % env.proj_name)

# -------
# Deploy
# -------
@task
def deploy():
    with project():
        # pull branch master of project
        run("git pull %s %s"  % (env.repo_repository, env.repo_refspec))
        # install pip requirements
        pip("-r %s" % (env.pip_requirements_path))
        # collect static files in a single location
        manage("collectstatic -v 0 --noinput")
        # compress static files to create a unique versioned cache file
        manage("compress")
        manage("migrate --all --no-initial-data")
        supervisor_reload()
