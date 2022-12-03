from enum import Enum


class ActionChoices(Enum):
    START = 'start'
    STOP = 'stop'
    RESTART = 'restart'


class ServerChoices(Enum):
    UWSGI = 'uwsgi'
