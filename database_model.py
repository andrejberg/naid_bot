"""
Under construction...
Place SQLlite database model here...
"""
__author__ = ["Andrej Berg"]
__date__ = "23.03.2020"

import sys, os
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

from config import db_config
from pprint import pprint # for debug


# ============================= MODEL =========================================
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer(), primary_key=True, index=True)
    added_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    title = Column(String(4096))                      # max length of telegram message
    description = Column(String(4096), nullable=True)
    location = Column(String(255), nullable=True)     # will be stored as google maps url

    # pending > posted > assigned > done  | ( > done_inadequate )
    status = Column(String(20), nullable=True, default="pending")

    # 3 states None, False, True
    confirmed_by_client = Column(Boolean(), nullable=True)
    confirmed_by_volunteer = Column(Boolean(), nullable=True)
    done_by_client = Column(Boolean(), nullable=True)
    done_by_volunteer = Column(Boolean(), nullable=True)

    # keep track which messages were used, needed for callbacks
    message_id_overview = Column(Integer(), nullable=True)
    message_id_post = Column(Integer(), nullable=True)
    message_id_client = Column(Integer(), nullable=True)
    message_id_volunteer = Column(Integer(), nullable=True)

    # relationships to users
    client_id = Column(Integer(), ForeignKey('users.id'))
    client = relationship(
        "User",
        back_populates="tasks_order",
        foreign_keys="Task.client_id"
    )

    volunteer_id = Column(Integer(), ForeignKey('users.id'))
    volunteer = relationship(
        "User",
        back_populates="tasks_fulfill",
        foreign_keys="Task.volunteer_id"
    )

    def __repr__(self):
        return "{}(id='{}', title='{}', description='{}')".format(
            self.__class__.__name__,
            self.id,
            self.title,
            self.description)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True) # telegram user id
    first_name = Column(String(255))

    last_name = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)

    tasks_order = relationship("Task", back_populates="client", foreign_keys="Task.client_id")
    tasks_fulfill = relationship("Task", back_populates="volunteer", foreign_keys="Task.volunteer_id")

    groups = relationship("GroupMembership", back_populates="user")

    fouls = relationship("Foul", back_populates="user", foreign_keys="Foul.user_id")

    def __repr__(self):
        return "{}(id='{}', first_name='{}', username='{}')".format(
            self.__class__.__name__,
            self.id,
            self.first_name,
            self.username)

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer(), primary_key=True) # telegram group id

    name = Column(String(255), nullable=True)

    users = relationship("GroupMembership", back_populates="group")

class GroupMembership(Base):
    __tablename__ = 'groupmemberships'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)

    is_admin = Column(Boolean(), nullable=True)

    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="users")

class Foul(Base):
    __tablename__ = 'fouls'

    id = Column(Integer(), primary_key=True) # telegram user id
    added_on = Column(DateTime(), default=datetime.now)

    user_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship(
        "User",
        back_populates="fouls",
        foreign_keys="Foul.user_id"
    )
# =============================================================================


# =============================== API =========================================

Session = sessionmaker()  # prepare session object
engine = create_engine(   # create engine
    'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(**db_config)
)

@contextmanager
def session_handler():
    """
    Context manager for sessions.
    Parameters
    ----------
    init_tables : bool False
        create all tables on first connection

    Yields
    ------
    session : sqlalchemy.orm.session.Session
        SQL Alchemy session

    Example
    -------
    with session_handler() as session:
        q = session.query(Tasks)

    """
    Session.configure(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        Session.configure(bind=None)
        session.close()

def reset_database(session):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# =============================================================================


# ============================= TEST ==========================================
if __name__ == '__main__':
    """
    Execute database_model.py to test functionality of database model.
    """

    with session_handler() as session:

        reset_database(session)

        # u1 = User(id = 1, first_name = "John", username = "john@greatwall")
        # session.add(u1)
        # u2 = User(id = 2, first_name = "Sam", username = "sam@greatwall")
        # session.add(u2)
        # session.flush()
        # t = Task(title = "Find wildlings.", client = u2, volunteer = u1)
        # session.add(t)
        # session.commit()
