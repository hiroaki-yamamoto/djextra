#!/usr/bin/env python
# coding=utf-8

"""MDMultiSelect module."""

from django.forms import SelectMultiple
from .mdselect import MDSelect


class MDMultiSelect(MDSelect, SelectMultiple):
    """MDSelect widget that allows multiple select."""

    allow_multiple_selected = True

    def get_context(self, name, value, attrs):
        """Override get_context."""
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['data-multiple'] = \
            bool(context['widget']['attrs'].pop("multiple"))
        return context
