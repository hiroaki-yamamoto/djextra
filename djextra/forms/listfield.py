#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""List field implementation code."""

from django import forms
from django.utils.translation import ugettext_lazy as _


class ListField(forms.Field):
    """List Field."""

    default_error_messages = {
        "invalid_list": _("Enter a list of values.")
    }

    def __init__(self, *args, **kwargs):
        """Init."""
        self.field = kwargs.pop("field", None) or forms.CharField()
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """Normalize the value into python format with specified field."""
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise forms.ValidationError(
                self.error_messages["invalid_list"], code="invalid_list"
            )
        errors = []
        normalize_values = []
        for (index, item) in enumerate(value):
            try:
                normalize_values.append(self.field.to_python(item))
            except forms.ValidationError as exc:
                errors.append(forms.ValidationError(
                    "Index %(index)d: %(err_msg)s", params={
                        "index": index,
                        "err_msg": ("").join(exc.messages),
                        "exception": exc
                    }
                ))
        if errors:
            raise forms.ValidationError(errors, code="invalid")
        return normalize_values

    # validate(self, value) function is reserved for the subclass of this
    # class.

    def run_validators(self, value):
        """Validate the value."""
        errors = []
        for (index, item) in enumerate(value):
            try:
                self.field.run_validators(item)
            except forms.ValidationError as exc:
                errors.append([
                    forms.ValidationError(
                        "Index %(index)d: %(err_msg)s", params={
                            "index": index,
                            "err_msg": ("").join(exc.messages),
                            "exception": exc
                        }
                    )
                ])
        if errors:
            raise forms.ValidationError(errors, code="invalid")
