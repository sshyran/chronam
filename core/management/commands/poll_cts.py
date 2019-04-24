from __future__ import absolute_import

import logging

from django.core.management.base import CommandError

from chronam.core import tasks

from . import LoggingCommand

LOGGER = logging.getLogger(__name__)


class Command(LoggingCommand):
    help = "manual command to load new batches from CTS"  # NOQA: A003

    def handle(self, *args, **options):
        try:
            tasks.poll_cts.apply()
        except Exception:
            LOGGER.exception("Unable to load new batches from CTS")
            raise CommandError("unable to load batches from CTS")
