"""
This recipe will help you to manage your services. You can specify service by
name or by index.
usage:
    fab -f fab_services.py -H <hostname> status:1
    fab -f fab_services.py -H <hostname> status:nginx
    fab -f fab_services.py -H <hostname> status:asdf --> will show you help

"""

from fabric.api import env, task, sudo


SERVICES = {
            'nginx': '/etc/init.d/nginx %s',
            'mongo': '/etc/init.d/mongodb %s',
            'postgresql': '/etc/init.d/postgresql %s',
            'redis': '/etc/init.d/redis-server %s',
            # other services
           }
SERVICES_LIST = ['nginx',
                 'mongo',
                 'postgresql',
                 'redis']


def _clean(service):

    try:
        # -1 --> we use one based indexes in console
        service = SERVICES_LIST[int(service) - 1]
    except (ValueError, IndexError):
        pass

    if service not in SERVICES:
        print "Bad argument. Should be one of " + str(SERVICES.keys())
        print "You can use int for service number: "
        for i in enumerate(SERVICES_LIST):
            print "%s) %s" % (i[0] + 1, i[1])
        exit()
    return service

@task
def stop(service):
    """
    Stop service execution
    """
    service = _clean(service)
    sudo(SERVICES[service] % ("stop",))


@task
def start(service):
    """
    Start service
    """
    service = _clean(service)
    sudo(SERVICES[service] % ("start",))


@task
def restart(service):
    """
    Restart service
    """
    service = _clean(service)
    sudo(SERVICES[service] % ("restart",))


@task
def status(service):
    """
    Check service execution status
    """
    service = _clean(service)
    sudo(SERVICES[service] % ("status",))