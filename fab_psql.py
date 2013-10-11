"""
This recipe will help you to setup and manage PostgreSQL (9.1).
usage:
    fab -f fab_psql.py -H <hostname> setup_postgresql
    fab -f fab_psql.py -H <hostname> psql_report
    fab -f fab_psql.py -H <hostname> psql_connections
    fab -f fab_psql.py -H <hostname> psql_connections:true
"""

from fabric.api import task, sudo, put
from fabric.contrib.console import confirm


@task
def setup_postgresql():
    """
    Setup and configure PostgreSQL
    """
    sudo("apt-get -y install postgresql-9.1")
    sudo('cp /etc/postgresql/9.1/main/postgresql.conf '\
            '/etc/postgresql/9.1/main/postgresql.conf.bak')
	# file postgresql.conf.pgtune_1Gb was tuned by pgtune
    put('configs/postgresql.conf.pgtune_1Gb',
        '/etc/postgresql/9.1/main/postgresql.conf',
        use_sudo=True)
    # increase SHMMAX - Maximum size of shared memory segment (bytes)
    # new settings need this tuning
    sudo('cp /etc/sysctl.conf /etc/sysctl.conf.bak')
    # this setting will be applyed after execution, but will be lost on restart
    sudo('sysctl -w kernel.shmmax=300000000')
    # change shmmax so, that this setting would not lost after restart
    sudo("echo 'kernel.shmmax=300000000' | tee -a /etc/sysctl.conf")
    sudo('/etc/init.d/postgresql restart')
    sudo("psql -c \"ALTER USER postgres WITH PASSWORD '123456';\"",
         user='postgres')
    sudo("psql -c \"CREATE USER karma WITH PASSWORD '123456';\"",
         user='postgres')
    sudo("psql -c \"CREATE DATABASE karma WITH ENCODING='UTF8' OWNER=karma;\"",
         user='postgres')


#===============================================================================
# Reports
#===============================================================================

@task
def psql_connections(verbose='false'):
    """
    Show active connections. optional param verbose=(true|false)
    verbose=True show full details,
    verbose=False show only connection number
    """

    print "=========================================="
    print "============== Connections ==============="
    print "=========================================="
    verbose = verbose.lower()
    if verbose == 'false':
        sudo("psql -c 'select count(*) from pg_stat_activity;'",
             user='postgres')
    else:
        sudo("psql -c 'select * from pg_stat_activity;'",
             user='postgres')


@task
def psql_data_hitrate():
    """
    Show cache hit rate for data in PostgreSQL.
    """

    print "=========================================="
    print "============== Data hitrate =============="
    print "=========================================="
    query = "SELECT "\
                "sum(heap_blks_read) as heap_read, "\
                "sum(heap_blks_hit)  as heap_hit, "\
                "sum(heap_blks_hit) / "\
                    "(sum(heap_blks_hit) + sum(heap_blks_read)) as ratio "\
            "FROM pg_statio_user_tables;"

    sudo("psql -c '%s' karma" % (query,), user='postgres')
    confirm("Hitrate value should be more than 99.99%")


@task
def psql_index_hitrate():
    """
    Show cache hit rate for index in PostgreSQL.
    """

    print "==========================================="
    print "============== Index hitrate =============="
    print "==========================================="
    query = "SELECT "\
                "sum(idx_blks_read) as idx_read, "\
                "sum(idx_blks_hit)  as idx_hit, "\
                "sum(idx_blks_hit) / "\
                    "(sum(idx_blks_hit) + sum(idx_blks_read)) as ratio "\
            "FROM pg_statio_user_indexes;"

    sudo("psql -c '%s' karma" % (query,), user='postgres')
    confirm("Hitrate value should be more than 99%")


@task
def psql_report():
    """
    Show all available reports.
    """
    psql_index_hitrate()
    psql_data_hitrate()
    psql_table_stats()
    psql_connections()


@task
def psql_table_stats():
    """
    Show % of requests that uses index to satisfy queries to different tables.
    """
    print "==========================================="
    print "=============== Table stats ==============="
    print "==========================================="
    query = 'SELECT relname, idx_scan, seq_scan, 100 * idx_scan / '\
            '(seq_scan + idx_scan) "index_used, %", n_live_tup '\
            'rows_in_table FROM pg_stat_user_tables WHERE '\
            'seq_scan + idx_scan > 0 ORDER BY n_live_tup DESC;'
    sudo("psql -c '%s' karma" % (query,), user='postgres')
