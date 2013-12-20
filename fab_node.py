"""
This recipe will help you to setup the most recent version of Node.js.
usage:
    fab -f fab_node.py -H <hostname> setup_node
"""

from fabric.api import task, sudo, cd


@task
def setup_node():
    """
    setup and configure Node.js
    https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager
    """

    sudo("apt-get -y install python g++ make checkinstall")
    # download and unzip Node
    with cd("/tmp"):
        sudo("wget -N http://nodejs.org/dist/node-latest.tar.gz")
        sudo("tar xzvf node-latest.tar.gz")

    # builf package and setup it
    with cd("/tmp/node-v*"):
        sudo("./configure")
        print '======================= IMPORTANT ============================='
        print 'remove the "v" in front of the version number in the dialog'
        print '==============================================================='
        sudo("checkinstall")
        sudo("dpkg -i node_*")  # can be deleted with: sudo dpkg -r node

