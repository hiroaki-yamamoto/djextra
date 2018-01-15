#!/usr/bin/env python
# coding=utf-8

"""Datepicker for Django."""

from django import forms

from .base import BaseWidget


class MDDatePicker(BaseWidget, forms.DateInput):
    """AngularJS Material DatePicker for Django."""

    template_name = "md_datepicker.html"
