#!/usr/bin/env python
# coding=utf-8

"""Selection Btn."""

from django import forms

from .base import BaseWidget


class MDCheckBox(BaseWidget, forms.CheckboxInput):
    """Material Checkbox."""

    template_name = "md_checkbox.html"

    def __init__(self, label="", help_text="", *args, **kwargs):
        """Init the instance."""
        super().__init__(*args, **kwargs)
        self.label = label
        self.help_text = help_text

    def get_context(self, name, value, attrs):
        """Override get_context."""
        ret = super().get_context(name, value, attrs)
        if "checked" in ret["widget"]["attrs"]:
            ret["widget"]["attrs"]["data-checked"] = \
                ret["widget"]["attrs"].pop("checked")
        ret["widget"]["label"] = self.label
        ret["widget"]["help_text"] = self.help_text
        return ret
