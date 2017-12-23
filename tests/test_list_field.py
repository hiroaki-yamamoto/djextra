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
        self.assertTrue(self.form.is_valid(), dict(self.form.errors))
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
                self.form.fields["families"].error_messages["invalid_list"]
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
        self.assertTrue(self.form.is_valid(), dict(self.form.errors))
        self.assertEqual(self.form.clean(), self.payload)


class ListFieldValidateAndCastSuccessTest(TestCase):
    """ListField field validation test."""

    class TestForm(forms.Form):
        """The form."""

        name = forms.CharField()
        numbers = extraforms.ListField(
            field=forms.IntegerField()
        )

    def setUp(self):
        """Setup."""
        self.payload = {
            "name": "Test",
            "numbers": ["10", "20", "30"]
        }
        self.form = self.TestForm(data=self.payload)

    def test_cleaned_data(self):
        """The cleaned data should be equal to payload."""
        expected_result = self.payload.copy()
        expected_result["numbers"] = [
            int(item) for item in expected_result["numbers"]
        ]
        self.assertTrue(self.form.is_valid(), dict(self.form.errors))
        self.assertEqual(self.form.clean(), expected_result)


class ListFieldCastFailureTest(TestCase):
    """ListField field cast failure test."""

    class TestForm(forms.Form):
        """The form."""

        name = forms.CharField()
        numbers = extraforms.ListField(field=forms.IntegerField())

    def setUp(self):
        """Setup."""
        self.payload = {
            "name": "Test",
            "numbers": ["10", "20", "xx"]
        }
        self.form = self.TestForm(data=self.payload)

    def test_error(self):
        """Should raise an error."""
        self.assertFalse(self.form.is_valid())
        self.assertEqual(dict(self.form.errors), {
            "numbers": [
                ("Index 2: {}").format(
                    self.form.fields["numbers"].field.error_messages["invalid"]
                )
            ]
        })


class ListFieldValidationErrorTest(TestCase):
    """ListField validation failure test."""

    class TestForm(forms.Form):
        """The form."""

        name = forms.CharField()
        emails = extraforms.ListField(field=forms.EmailField())

    def setUp(self):
        """Setup."""
        self.payload = {
            "name": "Test",
            "emails": ["test@example.com", "hello@example.com", "test"]
        }
        self.form = self.TestForm(data=self.payload)

    def test_error(self):
        """Should raise an error."""
        self.assertFalse(self.form.is_valid())
        self.assertEqual(dict(self.form.errors), {
            "emails": [
                ("Index 2: {}").format(
                    self.form.fields["emails"].field.validators[0].message
                )
            ]
        })
