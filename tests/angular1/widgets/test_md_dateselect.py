#!/usr/bin/env python
# coding=utf-8

"""Date Selection for AngularMaterial test."""

from django import setup
from django.forms.widgets import SelectDateWidget
from django.test import TestCase
from djextra.forms.angular1.widgets import MDDateSelect, MDSelect


setup()


class SimpleMDDateSelectTest(TestCase):
    """Simple MDDateSelect Test."""

    def setUp(self):
        """Setup."""
        self.widget = MDDateSelect()

    def test_type(self):
        """The widget should inherit SelectDateWidget."""
        self.assertIsInstance(self.widget, SelectDateWidget)

    def test_selection_widget(self):
        """The select_widget should be MDSelect."""
        self.assertIs(self.widget.select_widget, MDSelect)
