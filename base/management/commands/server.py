from dataclasses import dataclass
import os
import signal
from typing import List

from django.core.management.base import BaseCommand, CommandError

from base.choices.management import ActionChoices, ServerChoices


@dataclass
class ServerArguments:
    action_choices: List[ActionChoices]
    server_choices: List[ServerChoices]


SERVER_ARGUMENTS = ServerArguments(
    action_choices=[
        ActionChoices.START,
        ActionChoices.STOP,
        ActionChoices.RESTART
    ],
    server_choices=[
        ServerChoices.UWSGI,
    ]
)


class Command(BaseCommand):
    help = 'Stops the server'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=[action.value for action in SERVER_ARGUMENTS.action_choices]
        )
        parser.add_argument(
            '-s',
            '--server',
            type=str,
            choices=[action.value for action in SERVER_ARGUMENTS.server_choices],
            required=True
        )
        parser.add_argument(
            '-f',
            '--force',
            action='store_true'
        )

    def handle(self, *args, **options):
        server = options.get('server')
        force = options.get('force')
        action = options.get('action')

        if action == ActionChoices.STOP.value:
            self.stop(server, force)
        elif action == ActionChoices.RESTART.value:
            self.restart(server)
        else:
            raise NotImplementedError('Action %s not implemented' % action)

    def restart(self, server):
        if server == ServerChoices.UWSGI.value:
            self.restart_uwsgi()

    def restart_uwsgi(self):
        try:
            import uwsgi
        except ImportError:
            raise CommandError('uWSGI not found')

        self.stdout.write('uWSGI reload started')

        uwsgi.reload()

    def stop(self, server, force):
        master_pid = self.get_master_pid(server)

        signal_number = signal.SIGKILL if force else signal.SIGTERM

        try:
            os.kill(master_pid, signal_number)
        except ProcessLookupError:
            raise CommandError('No process=%s' % master_pid)

    def get_master_pid(self, server):
        if server == ServerChoices.UWSGI.value:
            return self.get_uwsgi_pid()
        else:
            raise CommandError('Server %s not found' % server)

    def get_uwsgi_pid(self):
        try:
            import uwsgi
        except ImportError:
            raise CommandError('uWSGI not found')

        pid = uwsgi.masterpid()

        self.stdout.write('uwsgi pid=%s' % pid)

        return pid
