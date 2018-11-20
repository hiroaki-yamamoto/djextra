#!/usr/bin/env python
# coding=utf-8

"""MDSelect Tests."""

from django import setup
from django.test import TestCase

from djextra.forms.angular1.widgets import MDSelect

setup()


class SimpleMDSelectTest(TestCase):
    """Simple MDSelect Usage test."""

    def setUp(self):
        """Setup."""
        self.field = MDSelect(choices=(
            ("test", "Test"), ("test2", "Test2"), (None, "Test3")
        ))

    def test_render(self):
        """The generated html should be correct."""
        result = str(self.field.render("result", None)).replace("\n", "")
        data = (
            "<md-select data-name=\"result\">"
            "<md-option data-value=\"test\">Test</md-option>"
            "<md-option data-value=\"test2\">Test2</md-option>"
            "<md-option data-value=\"\" data-selected>Test3</md-option>"
            "</md-select>"
        )
        self.assertEqual(result, data)

    def test_render_has_value(self):
        """The generated html should be correct."""
        result = str(self.field.render("result", "test")).replace("\n", "")
        data = (
            "<md-select data-name=\"result\">"
            "<md-option data-value=\"test\" data-selected>"
            "Test</md-option>"
            "<md-option data-value=\"test2\">Test2</md-option>"
            "<md-option data-value=\"\">Test3</md-option>"
            "</md-select>"
        )
        self.assertEqual(result, data)

    def test_render_unselectable_value(self):
        """The generated html should be correct."""
        result = str(self.field.render("result", "test_a")).replace("\n", "")
        data = (
            "<md-select data-name=\"result\">"
            "<md-option data-value=\"test\">Test</md-option>"
            "<md-option data-value=\"test2\">Test2</md-option>"
            "<md-option data-value=\"\">Test3</md-option>"
            "</md-select>"
        )
        self.assertEqual(result, data)


class MDSelectGroupingTest(TestCase):
    """MDSelect Grouping test."""

    def setUp(self):
        """Setup."""
        self.field = MDSelect(
            choices=(
                ("test", (
                    ("testTest1", "Test Test 1"),
                    ("testTest2", "Test Test 2")
                )),
                ("test2", "Test2")
            )
        )

    def test_render(self):
        """The generated html should be correct."""
        result = str(self.field.render("result", None)).replace("\n", "")
        data = (
            "<md-select data-name=\"result\">"
            "<md-optgroup data-label=\"test\">"
            "<md-option data-value=\"testTest1\">Test Test 1</md-option>"
            "<md-option data-value=\"testTest2\">Test Test 2</md-option>"
            "</md-optgroup>"
            "<md-option data-value=\"test2\">Test2</md-option>"
            "</md-select>"
        )
        self.assertEqual(result, data)


class MDSelectEmptyFieldTest(TestCase):
    """MDSelect Test without any options."""

    def setUp(self):
        """Setup."""
        self.field = MDSelect()

    def test_render(self):
        """The generated html should be correct."""
        result = str(self.field.render("result", None)).replace("\n", "")
        data = "<md-select data-name=\"result\"></md-select>"
        self.assertEqual(result, data)


class MDSelectDisableSelectTest(TestCase):
    """MDSelect test with disabled selection."""

    def setUp(self):
        """Setup."""
        self.field = MDSelect(disable_select=True, choices=(
            ("test", "Test"), ("test2", "Test2"), (None, "Test3")
        ))

    def test_render(self):
        """The generated html should be correct."""
        result = str(self.field.render("result", None)).replace("\n", "")
        data = (
            "<md-select data-name=\"result\">"
            "<md-option data-value=\"test\">Test</md-option>"
            "<md-option data-value=\"test2\">Test2</md-option>"
            "<md-option data-value=\"\">Test3</md-option>"
            "</md-select>"
        )
        self.assertEqual(result, data)

    def test_render_has_value(self):
        """The generated html should be correct."""
        result = str(self.field.render("result", "test")).replace("\n", "")
        data = (
            "<md-select data-name=\"result\">"
            "<md-option data-value=\"test\">Test</md-option>"
            "<md-option data-value=\"test2\">Test2</md-option>"
            "<md-option data-value=\"\">Test3</md-option>"
            "</md-select>"
        )
        self.assertEqual(result, data)
