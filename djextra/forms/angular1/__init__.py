#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""AngularJS (aka Angular1, Angular Legacy) forms."""

from .forms import AngularForm
from .widgets import (
    MDSelect, MDMultiSelect, MDDatePicker, MDDateSelect, MDCheckBox
)


__all__ = (
    "AngularForm", "MDSelect", "MDMultiSelect",
    "MDDatePicker", "MDDateSelect", "MDCheckBox"
)
