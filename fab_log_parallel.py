"""
This recipe will read logs from several servers in parallel in real time
usage:
fab -f fab_log_parallel.py -R www log
"""

from fabric.api import env, task, sudo, settings, parallel

env.roledefs = {
    # production servers
    'www': ['srv1.com', 'srv2.com']
}

env.remote_interrupt = True
env.LOG = '<path to log>'
    
@parallel
def log():
    assert(env.remote_interrupt == True)
    with settings(warn_only=True):
        sudo("tail -n 50 -f " + env.LOG)
