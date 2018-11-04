#!/usr/bin/env python
# coding=utf-8

"""Django AngularJS Helper Froms."""

import json
from datetime import date
from functools import wraps
from django import forms


class AngularForm(forms.Form):
    """AngularJS Form."""

    def __wrap_ng_init(self, f, fld):
        """Wrap ng-init attribute."""
        @wraps(f)
        def inside(name, value, attrs):
            format_func = getattr(
                fld, "ng_init_format_func",
                lambda v: (
                    fld.widget.format_value(v)
                    if isinstance(v, (date, str)) else
                    v
                )
            )
            model_var = \
                fld.widget.attrs.get("data-ng-model") or attrs["data-ng-model"]
            attrs["data-ng-init"] = \
                f"{model_var} = {json.dumps(format_func(value))}"
            return f(name, value, attrs)
        return inside

    def __init__(self, *args, **kwargs):
        """Init the function."""
        super().__init__(*args, **kwargs)
        metaclass = getattr(self, "Meta", type("Meta", (object,), {}))
        handle_ng_init = getattr(metaclass, "handle_ng_init", False)
        ng_init_format_func = getattr(metaclass, "ng_init_format_func", {})
        self.ng_model_prefix = getattr(metaclass, "ng_model_prefix", "model")

        for (name, field) in self.fields.items():
            model = f"{self.ng_model_prefix}.{name}"
            field.widget.attrs.setdefault("data-ng-model", model)
            if handle_ng_init:
                if name in ng_init_format_func:
                    setattr(
                        field, "ng_init_format_func",
                        ng_init_format_func[name]
                    )
                tmp = field.widget.get_context
                field.widget.get_context = self.__wrap_ng_init(tmp, field)
