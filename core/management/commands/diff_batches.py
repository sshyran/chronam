from __future__ import absolute_import, print_function

from optparse import make_option

from django.core.management.base import CommandError

from chronam.core import models

from . import LoggingCommand


class Command(LoggingCommand):
    option_list = LoggingCommand.option_list + (
        make_option(
            '--skip-process-ocr',
            action='store_false',
            dest='process_ocr',
            default=True,
            help='Do not generate ocr, and index',
        ),
    )
    help = "Diff batches by name from a batch list file"  # NOQA: A003
    args = '<batch_list_filename>'

    def handle(self, batch_list_filename, *args, **options):
        if len(args) != 0:
            raise CommandError('Usage is diff_batch %s' % self.args)

        batches = set()
        batch_list = open(batch_list_filename)
        self.stdout.write("batch_list_filename: %s" % batch_list_filename)
        for line in batch_list:
            batch_name = line.strip()
            self.stdout.write("batch_name: %s" % batch_name)
            parts = batch_name.split("_")
            if len(parts) == 4 and parts[0] == "batch":
                batches.add(batch_name)
            else:
                self.stderr.write("invalid batch name '%s'" % batch_name)

        current_batches = set()
        for batch in models.Batch.objects.all().order_by('name'):
            current_batches.add(batch.name)

        all_batches = batches.union(current_batches)
        for batch in sorted(all_batches):
            if batch in batches:
                if batch in current_batches:
                    indicator = " "  # both
                else:
                    indicator = "-"
            else:
                assert batch in current_batches
                indicator = "+"

            self.stdout.write("%s%s" % (indicator, batch))
