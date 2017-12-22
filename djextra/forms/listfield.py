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
        self.fields = kwargs.pop("fields", None) or super(ListField, self)
        super(ListField, self).__init__(*args, **kwargs)

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
        if isinstance(self.fields, (list, tuple)):
            for (index, el) in enumerate(value):
                try:
                    normalize_values.append(
                        self.fields[index % len(self.fields)].clean(el)
                    )
                except forms.ValidationError as exc:
                    for message in exc.messages:
                        errors.append(
                            forms.ValidationError(
                                "Index %(index)s: %(error_msg)s", params={
                                    "index": index,
                                    "error_msg": message,
                                    "error": exc
                                }, code="invalid"
                            )
                        )
        else:
            normalize_values = [self.fields.to_python(item) for item in value]
        if errors:
            raise forms.ValidationError(errors, code="invalid")
        return normalize_values
