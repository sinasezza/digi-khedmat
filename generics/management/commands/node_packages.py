import os
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Manage node package modules"

    def add_arguments(self, parser):
        parser.add_argument(
            'action', nargs='?', default='install', type=str,
            help='Specify the action to perform (e.g., "install", "update")'
        )

    def handle(self, *args, **options):
        action = options['action']
        if action == 'install':
            self.install_node_packages()
        elif action == 'update':
            self.update_node_packages()
        else:
            raise CommandError(f"Unknown action: {action}")

    def install_node_packages(self):
        os.chdir('static/node_packages')
        os.system('npm install')
        self.stdout.write(self.style.SUCCESS("Node packages installed successfully"))

    def update_node_packages(self):
        os.chdir('static/node_packages')
        os.system('npm update')
        self.stdout.write(self.style.SUCCESS("Node packages updated successfully"))
