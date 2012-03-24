from sqlalchemy.orm.session import sessionmaker
import MySQLdb
import core_config
import sqlalchemy

def connect_mysqldb():
    """
    Same as calling MySQLdb.connect(...)
    This func auto fill everything
    need to call ret.commit() and ret.close() to clean up
    
    @rtype:  MySQLdb.connections.Connection
    @return: MySQL connection to DB
    """
    return MySQLdb.connect(
                           host=core_config.DB_SERVER,
                           user=core_config.DB_USERNAME,
                           passwd=core_config.DB_PASSWORD,
                           db=core_config.DB_SCHEMATA,
                           charset="utf8",
                           use_unicode=True
                           )

def create_sqlalchemy_engine():
    """
    Same as calling sqlalchemy.create_engine(...)
    This func auto fill everything
    Seems no cleanup func
    
    @rtype: sqlalchemy.engine.base.Engine
    @return: the engine with proper settings
    """
    return sqlalchemy.create_engine(
                         "mysql+mysqldb://"
                         + core_config.DB_USERNAME
                         + ":"
                         + core_config.DB_PASSWORD
                         + "@"
                         + core_config.DB_SERVER
                         + "/"
                         + core_config.DB_SCHEMATA
                         + "?charset=utf8&use_unicode=1"
                         )

def create_sqlalchemy_session():
    """
    Same as calling sqlalchemy.orm.session.sessionmaker(...)()
    This func auto fill everything
    need to call ret.close() to clean up

    @rtype:  sqlalchemy.orm.session.Session
    @return: session object connected to DB
    """
    Session = sessionmaker(bind=create_sqlalchemy_engine())
    return Session()

def create_sqlalchemy_session_push(cleanup):
    """
    Same as calling create_sqlalchemy_session()
    But also put the session.close to the cleanup.
    
    @rtype:  sqlalchemy.orm.session.Session
    @return: session object connected to DB
    """
    session = create_sqlalchemy_session()
    cleanup.push(session.close)
    return session
