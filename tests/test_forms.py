#!/usr/bin/env python
# coding=utf-8

"""Forms Test."""

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock  # noqa
from django import forms, setup
from django.test import TestCase
from djextra.forms import AllRequiredForm, FieldAttributeForm

setup()


class FieldCommonAttributeFormTest(TestCase):
    """Field common attirbute form test."""

    def setUp(self):
        """Setup."""
        class TestForm(FieldAttributeForm):

            class Meta(object):
                common_attrs = {
                    "data-on-load": "test()",
                    "data-on-delay": MagicMock(return_value="hello()")
                }
                fld_attrs = {
                    "name1": {
                        "data-test": "test1"
                    },
                    "name2": {
                        "data-test": MagicMock(return_value="test2")
                    }
                }

            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = TestForm
        self.form_instance = self.form_cls()

    def test_not_evaluate(self):
        """
        The attributes shouldn't be evaluated.

        The attributes shouldn't be evaluated. until get_context is called.
        """
        for name, fld in self.form_instance.fields.items():
            for key in (
                list(self.form_instance.Meta.common_attrs.keys()) +
                list(self.form_instance.Meta.fld_attrs.get(name, {}).keys())
            ):
                self.assertNotIn(key, fld.widget.attrs)

    def test_evaluate(self):
        """Calling get context, the attrs should be evaluated."""
        for name, fld in self.form_instance.fields.items():
            value = ("test_{}").format(name)
            widget_attrs = fld.widget.get_context(
                name, value, {}
            )["widget"]["attrs"]
            for key, attr_val in (
                list(self.form_instance.Meta.common_attrs.items()) +
                list(self.form_instance.Meta.fld_attrs.get(name, {}).items())
            ):
                if isinstance(attr_val, MagicMock):
                    self.assertEqual(attr_val.return_value, widget_attrs[key])
                    attr_val.assert_called_with(
                        self.form_instance, fld, name, value
                    )
                else:
                    self.assertEqual(attr_val, widget_attrs[key])
        self.assertEqual(
            self.form_cls.Meta.common_attrs["data-on-delay"].call_count,
            len(self.form_instance.fields)
        )
        self.form_cls.Meta.fld_attrs[
            "name2"
        ]["data-test"].assert_called_once_with(
            self.form_instance, self.form_instance.fields["name2"],
            "name2", "test_name2"
        )


class AllRequiredFormSimpleTest(TestCase):
    """All required form simple initialization test."""

    def setUp(self):
        """Setup."""
        class TestForm(AllRequiredForm):
            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = TestForm

    def test_form(self):
        """The form should have required=True attr."""
        result = self.form_cls()
        for (name, fld) in result.fields.items():
            self.assertTrue(
                fld.required, "required flag of %s is Falsy" % name
            )


class AllRequiredFormExceptionTest(TestCase):
    """All required form initialization test with some exception."""

    def setUp(self):
        """Setup."""
        class TestForm(AllRequiredForm):
            class Meta(object):
                optional = ("name2", "name3")

            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            name3 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = TestForm

    def test_optional(self):
        """Any attrs that are in optional metadata shouldn't be required."""
        result = self.form_cls()
        for name in self.form_cls.Meta.optional:
            self.assertFalse(
                result.fields[name].required,
                "required flag of %s is Truthy" % name
            )

    def test_required(self):
        """Any attrs that aren't in optional metadata shouldn't be required."""
        result = self.form_cls()
        names = set(result.fields.keys()) - set(self.form_cls.Meta.optional)
        for name in names:
            self.assertTrue(
                result.fields[name].required,
                "required flag of %s is Falsy" % name
            )
