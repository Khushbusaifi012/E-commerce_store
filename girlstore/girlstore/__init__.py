# PyMySQL lets Django use django.db.backends.mysql on Windows without mysqlclient.
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass
