#!/usr/bin/env python
# coding=utf-8

"""Forms Test."""

import json
import random
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock  # noqa
from django import forms, setup
from django.utils.timezone import now
from django.test import TestCase
from djextra.forms.angular1 import AngularForm

setup()


class SimpleAngularFormInitTest(TestCase):
    """Simply AngularJS Initialization test."""

    def setUp(self):
        """Setup."""
        class AngularExampleForm(AngularForm):
            """Example form for AngularJS."""

            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = AngularExampleForm

    def test_form(self):
        """All form field should have proper value at data-ng-model."""
        result = self.form_cls()
        for (name, field) in result.fields.items():
            self.assertTrue(
                set({"data-ng-model": "model.%s" % name}.items()).issubset(
                    set(field.widget.attrs.items())
                ),
                (
                    "Field %s doesn't have data-ng-model attribute"
                    " with proper value."
                ) % name
            )

    def test_get_context(self):
        """Attribute context shouldn't contain data-ng-init."""
        for (name, fld) in self.form_cls().fields.items():
            context = fld.widget.get_context(name, "test", {})["widget"]
            self.assertNotIn("data-ng-init", context["attrs"])


class CustomModelAngularFormInitTest(TestCase):
    """AngularJS Initialization test on custom model prefix."""

    def setUp(self):
        """Setup."""
        class AngularExampleForm(AngularForm):
            """Example form for AngularJS."""

            class Meta(object):
                ng_model_prefix = "pwn"

            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = AngularExampleForm

    def test_form(self):
        """All form field should have proper value at data-ng-model."""
        result = self.form_cls()
        for (name, field) in result.fields.items():
            self.assertTrue(
                set({
                    "data-ng-model": "%s.%s" % (
                        self.form_cls.Meta.ng_model_prefix, name
                    )
                }.items()).issubset(set(field.widget.attrs.items())),
                (
                    "Field %s doesn't have data-ng-model attribute"
                    " with proper value."
                ) % name
            )


class AngularFormHasValueTest(TestCase):
    """Angular form that has value test."""

    def setUp(self):
        """Setup."""
        class ClassValue(object):
            def __init__(self, value):
                self.value = value

        class TestForm(AngularForm):

            class Meta(object):
                handle_ng_init = True
                ng_init_format_func = {
                    "name3": lambda value: value.value
                }

            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            name3 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
            date = forms.DateTimeField(required=False)

        self.form = TestForm()
        self.class_value_cls = ClassValue

    def gen_value(self, name, fld):
        """Generate test value."""
        if isinstance(fld, forms.DateTimeField):
            return now()
        if isinstance(fld, forms.IntegerField):
            return random.randint(0, 10)
        if name == "name3":
            return self.class_value_cls(f"Test Value {name}")
        return f"Test Value {name}"

    def test_get_context(self):
        """The returned value from get_context should have ng-init event."""
        for (name, fld) in self.form.fields.items():
            value = self.gen_value(name, fld)
            context = fld.widget.get_context(name, value, {})["widget"]
            value = json.dumps(
                fld.widget.format_value(value)
                if isinstance(fld, forms.DateTimeField) else
                self.form.Meta.ng_init_format_func[name](value)
                if name == "name3" else
                value
            )
            expected = f"{self.form.ng_model_prefix}.{name} = {value}"
            self.assertEqual(
                expected, context["attrs"]["data-ng-init"],
                f"{name} is different ng-init event. "
                f"Expected: {expected}, "
                f'Actual: {context["attrs"]["data-ng-init"]}'
            )
