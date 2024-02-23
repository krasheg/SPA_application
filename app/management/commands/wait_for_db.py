"""
Django command to wait postgres database availability for avoid error
"""
import time

from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg20pError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django wait for DB"""
    def handle(self, *args, **options):
        # log message about executing of code
        self.stdout.write('Waiting for DB')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg20pError, OperationalError):
                time.sleep(1)
                self.stdout.write('Database unavailable, wait 1 second')

        self.stdout.write(self.style.SUCCESS('Database available!'))
