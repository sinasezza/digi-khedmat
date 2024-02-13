from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "importing the data"
    
    def handle(self, *args, **options):
        print("hello data")