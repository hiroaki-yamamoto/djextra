#!/usr/bin/env python
# coding=utf-8

"""MDCheckBox Test Case."""


from __future__ import unicode_literals
from django import setup
from django.test import TestCase

from djextra.forms.angular1.widgets import MDCheckBox

import htmlmin


setup()


class SimpleMDCheckBoxTest(TestCase):
    """Simple MDCheckBox Test."""

    def setUp(self):
        """Setup."""
        self.label = "This is a test"
        self.widget = MDCheckBox(self.label)

    def test_render(self):
        """Test render invokation."""
        result = self.widget.render("result", None)
        data = (
            "<md-checkbox data-name=\"result\"> {} </md-checkbox>"
        ).format(self.label)
        self.assertEqual(htmlmin.minify(result), htmlmin.minify(data))


class MDCheckBoxCheckedTest(TestCase):
    """MDCheckBox Checked test."""

    def setUp(self):
        """Setup."""
        self.label = "This is a test"
        self.widget = MDCheckBox(self.label)

    def test_render(self):
        """Test render invokation."""
        result = self.widget.render("result", True)
        data = (
            "<md-checkbox data-name=\"result\" data-checked> {} </md-checkbox>"
        ).format(self.label)
        self.assertEqual(htmlmin.minify(result), htmlmin.minify(data))


class MDCheckBoxHasClassTest(TestCase):
    """MDCheckBox test in the case that the widget has a value."""

    def setUp(self):
        """Setup."""
        self.label = "This is a test"
        self.widget = MDCheckBox(self.label)

    def test_render(self):
        """Test render invokation."""
        result = self.widget.render("result", "UWAAAAAHHH")
        data = (
            "<md-checkbox data-name=\"result\" data-value=\"UWAAAAAHHH\" "
            "data-checked> {} </md-checkbox>"
        ).format(self.label)
        self.assertEqual(htmlmin.minify(result), htmlmin.minify(data))


class MDCheckBoxHasHelpTextTest(TestCase):
    """MDCheckBox test in the case that the widget has a help text."""

    def setUp(self):
        """Setup."""
        self.label = "This is a test"
        self.help_text = "This is a help text."
        self.widget = MDCheckBox(self.label, help_text=self.help_text)

    def test_render(self):
        """Test render invokation."""
        result = self.widget.render("result", None)
        data = (
            "<md-checkbox data-name=\"result\">"
            " %s <md-tooltip>%s</md-tooltip> "
            "</md-checkbox>"
        ) % (self.label, self.help_text)
        self.assertEqual(htmlmin.minify(result), htmlmin.minify(data))
