#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extra functions for django."""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoExtra(AppConfig):
    """Extra functions for Django."""

    name = "djextra"
    label = "djextra"
    verbose_name = _("Extra functions for Django")
