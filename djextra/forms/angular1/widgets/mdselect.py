#!/usr/bin/env python
# coding=utf-8

"""MDSelect widgets."""

from django.forms import Select

from .base import BaseWidget


class MDSelect(BaseWidget, Select):
    """MDSelect."""

    template_name = "md_select.html"
    option_template_name = "md_select_option.html"

    def __init__(self, disable_select=False, *args, **kwargs):
        """Init the class."""
        super().__init__(*args, **kwargs)
        self.disable_select = disable_select
        self.checked_attribute = {"data-selected": not self.disable_select}
