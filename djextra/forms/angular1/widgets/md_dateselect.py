#!/usr/bin/env python
# coding=utf-8

"""Date Select for Angular Material."""

from django import forms
from .mdselect import MDSelect


class MDDateSelect(forms.SelectDateWidget):
    """Date Select for Angular Material."""

    select_widget = MDSelect
