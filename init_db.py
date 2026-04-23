"""Compatibility wrapper for seeding the Django database from CSV."""
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django


django.setup()

from django.core.management import call_command


if __name__ == "__main__":
    call_command("migrate", interactive=False)
    call_command("seed_scores", reset=True)
