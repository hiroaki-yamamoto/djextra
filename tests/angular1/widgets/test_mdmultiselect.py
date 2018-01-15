#!/usr/bin/env python
# coding=utf-8

"""MDMultiSelect Tests."""

from django import setup
from django.forms.widgets import SelectMultiple
from django.test import TestCase
from djextra.forms.angular1.widgets import MDMultiSelect, MDSelect


setup()


class SimpleMDMultiSelectTest(TestCase):
    """Simple MDMultiSelect Test."""

    def setUp(self):
        """Setup."""
        self.widget = MDMultiSelect(choices=(
            ("test1", "Test1"), ("test2", "Test2"), ("test3", "Test3")
        ))

    def test_inheritance(self):
        """The widget should inherit MDSelect and SelectMultiple."""
        self.assertIsInstance(self.widget, MDSelect)
        self.assertIsInstance(self.widget, SelectMultiple)

    def test_render(self):
        """The generated code should have data-multiple."""
        result = str(self.widget.render("result", None)).replace("\n", "")
        data = (
            "<md-select data-name=\"result\" data-multiple>"
            "<md-option data-value=\"test1\">Test1</md-option>"
            "<md-option data-value=\"test2\">Test2</md-option>"
            "<md-option data-value=\"test3\">Test3</md-option>"
            "</md-select>"
        )
        self.assertEqual(result, data)

    def test_render_has_values(self):
        """The generated code should have data-multiple."""
        result = str(
            self.widget.render("result", ["test1", "test2"])
        ).replace("\n", "")
        data = (
            "<md-select data-name=\"result\" data-multiple>"
            "<md-option data-value=\"test1\" data-selected>"
            "Test1</md-option>"
            "<md-option data-value=\"test2\" data-selected>"
            "Test2</md-option>"
            "<md-option data-value=\"test3\">Test3</md-option>"
            "</md-select>"
        )
        self.assertEqual(result, data)


class MDMultiSelectNoChoiceTest(TestCase):
    """MDMultiSelect without no options Test."""

    def setUp(self):
        """Setup."""
        self.widget = MDMultiSelect()

    def test_render(self):
        """The generated code should have data-multiple."""
        result = str(self.widget.render("result", None)).replace("\n", "")
        data = (
            "<md-select data-name=\"result\" data-multiple></md-select>"
        )
        self.assertEqual(result, data)
