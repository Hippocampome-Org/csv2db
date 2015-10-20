# truncate.py

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

class Command(BaseCommand):
    help = 'truncate tables'

    def add_arguments(self, parser):
        parser.add_argument('table_id', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            cursor = connection.cursor()
            cursor.execute('truncate table Article')
            self.stdout.write('Successfully truncated Article')
            cursor.execute('truncate table ArticleAuthorRel')
            self.stdout.write('Successfully truncated ArticleAuthorRel')
            cursor.execute('truncate table ArticleEvidenceRel')
            self.stdout.write('Successfully truncated ArticleEvidenceRel')
            cursor.execute('truncate table article_not_found')
            self.stdout.write('Successfully truncated article_not_found')
            cursor.execute('truncate table ArticleSynonymRel')
            self.stdout.write('Successfully truncated ArticleSynonymRel')
            cursor.execute('truncate table Attachment')
            self.stdout.write('Successfully truncated Attachment')
            cursor.execute('truncate table Author')
            self.stdout.write('Successfully truncated Author')
            cursor.execute('truncate table Epdata')
            self.stdout.write('Successfully truncated Epdata')
            cursor.execute('truncate table EpdataEvidenceRel')
            self.stdout.write('Successfully truncated EpdataEvidenceRel')
            cursor.execute('truncate table Evidence')
            self.stdout.write('Successfully truncated Evidence')
            cursor.execute('truncate table EvidenceEvidenceRel')
            self.stdout.write('Successfully truncated EvidenceEvidenceRel')
            cursor.execute('truncate table EvidenceFragmentRel')
            self.stdout.write('Successfully truncated EvidenceFragmentRel')
            cursor.execute('truncate table EvidenceMarkerdataRel')
            self.stdout.write('Successfully truncated EvidenceMarkerdataRel')
            cursor.execute('truncate table EvidencePropertyTypeRel')
            self.stdout.write('Successfully truncated EvidencePropertyTypeRel')
            cursor.execute('truncate table Fragment')
            self.stdout.write('Successfully truncated Fragment')
            cursor.execute('truncate table FragmentTypeRel')
            self.stdout.write('Successfully truncated FragmentTypeRel')
            cursor.execute('truncate table Markerdata')
            self.stdout.write('Successfully truncated Markerdata')
            cursor.execute('truncate table Property')
            self.stdout.write('Successfully truncated Property')
            cursor.execute('truncate table Synonym')
            self.stdout.write('Successfully truncated Synonym')
            cursor.execute('truncate table SynonymTypeRel')
            self.stdout.write('Successfully truncated SynonymTypeRel')
            cursor.execute('truncate table Term')
            self.stdout.write('Successfully truncated Term')
            cursor.execute('truncate table Type')
            self.stdout.write('Successfully truncated Type')
            cursor.execute('truncate table TypeTypeRel')
            self.stdout.write('Successfully truncated TypeTypeRel')
        except Exception:
            raise CommandError('Failed to truncate table(s)')
