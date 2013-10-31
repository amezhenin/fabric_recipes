"""
This recipe will help you to setup RabbitMQ for official repo.
usage:
    fab -f fab_rabbitmq.py -H <hostname> setup_rabbitmq
"""

from fabric.api import task, sudo, cd, prompt

@task
def setup_rabbitmq():
    """
    Setup and configure RabbitMQ
    """
    # add official repository to sources.list
    sudo('echo \'deb http://www.rabbitmq.com/debian/ testing main \' '\
         '> /etc/apt/sources.list.d/rabbitmq.list')
    with cd('/tmp'):
        sudo('wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc')
        sudo('apt-key add rabbitmq-signing-key-public.asc')
        sudo('rm rabbitmq-signing-key-public.asc')

    sudo('apt-get update')
    sudo('apt-get -y install rabbitmq-server')

    # Create new superuser, to replace old one (guest)
    login = prompt("RabbitMQ Administrator login: ")
    passwd = prompt("RabbitMQ Administrator password: ")
    sudo('rabbitmqctl add_user %s %s' % (login, passwd))
    sudo('rabbitmqctl set_user_tags karma administrator')
    sudo('rabbitmqctl set_permissions karma ".*" ".*" ".*"')
    sudo('rabbitmqctl delete_user guest')
    # ulimit -n 1024

    # Turn on web console(management plugin)
    sudo('rabbitmq-plugins enable rabbitmq_management')
    sudo('/etc/init.d/rabbitmq-server restart')
