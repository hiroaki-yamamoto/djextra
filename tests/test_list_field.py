#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ListField Test code."""

from django import forms
from django.test import TestCase

from djextra import forms as extraforms


class ListFieldFalsyBehaviorTest(TestCase):
    """ListField falsy value behavior test."""

    class TestForm(forms.Form):
        """The form."""

        name = forms.CharField()
        families = extraforms.ListField(required=False)

    def setUp(self):
        """Setup."""
        self.payload = {
            "name": "Test",
            "families": None
        }
        self.form = self.TestForm(data=self.payload)

    def test_cleaned_data(self):
        """The cleaned data should be equal to payload."""
        result = self.payload.copy()
        result["families"] = []
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.clean(), result)


class ListFieldNonListPayloadBehaviorTest(TestCase):
    """ListField non-list value behavior test."""

    class TestForm(forms.Form):
        """The form."""

        name = forms.CharField()
        families = extraforms.ListField()

    def setUp(self):
        """Setup."""
        self.payload = {
            "name": "Test",
            "families": {"hello": "world"}
        }
        self.form = self.TestForm(data=self.payload)

    def test_error(self):
        """Should raise an error."""
        self.assertFalse(self.form.is_valid())
        self.assertEqual(dict(self.form.errors), {
            "families": [
                extraforms.ListField.default_error_messages["invalid_list"]
            ]
        })


class ListFieldDefaultTest(TestCase):
    """ListField default behavior test."""

    class TestForm(forms.Form):
        """The form."""

        name = forms.CharField()
        families = extraforms.ListField()

    def setUp(self):
        """Setup."""
        self.payload = {
            "name": "Test",
            "families": ["Mother", "Father", "Brother"]
        }
        self.form = self.TestForm(data=self.payload)

    def test_cleaned_data(self):
        """The cleaned data should be equal to payload."""
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.clean(), self.payload)


class ListFieldValidateAndCastSuccessTest(TestCase):
    """ListField field validation test."""

    class TestForm(forms.Form):
        """The form."""

        name = forms.CharField()
        families = extraforms.ListField(
            fields=(
                forms.CharField(), forms.EmailField(), forms.IntegerField()
            )
        )

    def setUp(self):
        """Setup."""
        self.payload = {
            "name": "Test",
            "families": ["Mother", "mother@hysoftware.net", "49"]
        }
        self.form = self.TestForm(data=self.payload)

    def test_cleaned_data(self):
        """The cleaned data should be equal to payload."""
        expected_result = self.payload.copy()
        expected_result["families"][-1] = int(expected_result["families"][-1])
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.clean(), expected_result)
