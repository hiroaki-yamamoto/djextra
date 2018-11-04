#!/usr/bin/env python
# coding=utf-8

"""MDDatePicker Test."""

from datetime import datetime
from django import setup
from django.test import TestCase
from djextra.forms.angular1.widgets import MDDatePicker


setup()


class SimpleMDDatePickerTest(TestCase):
    """Simple MDDatePicker test."""

    def setUp(self):
        """Setup."""
        self.widget = MDDatePicker()

    def test_render(self):
        """The generated content should be correct."""
        result = str(self.widget.render("result", None)).replace("\n", "")
        data = (
            "<md-datepicker data-name=\"result\">"
            "</md-datepicker>"
        )
        self.assertEqual(result, data)

    def test_render_has_value(self):
        """The generated content should be correct."""
        now = datetime.utcnow().isoformat()
        result = str(self.widget.render("result", now)).replace("\n", "")
        data = (
            f"<md-datepicker data-name=\"result\" data-value=\"{now}\">"
            "</md-datepicker>"
        )
        self.assertEqual(result, data)
