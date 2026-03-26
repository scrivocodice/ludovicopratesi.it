import os

bind = "unix:////home/ludovicopratesi/var/run/gunicorn.sock"
workers = (os.sysconf("SC_NPROCESSORS_ONLN") * 2) + 1
loglevel = "error"
proc_name = "ludovicopratesi.it"
