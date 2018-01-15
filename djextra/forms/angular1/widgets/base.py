#!/usr/bin/env python
# coding=utf-8

"""Base classes."""

import os

from django.forms.widgets import Widget
from django.forms.renderers import Jinja2 as Jinja2Base
from django.utils.safestring import mark_safe
from django.utils.functional import cached_property


class Jinja2Engine(Jinja2Base):
    """Jinja2 template engine."""

    @cached_property
    def engine(self):
        """Return engine setting."""
        return self.backend({
            'DIRS': [
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    self.backend.app_dirname
                )
            ],
            'APP_DIRS': True,
            'NAME': "djextra-widgets",
            'OPTIONS': {}
        })


class BaseWidget(Widget):
    """Base widget to render the widget properly."""

    def _render(self, template_name, context, renderer=None):
        """Override render protected function."""
        renderer = Jinja2Engine()
        template = renderer.get_template(template_name)
        return mark_safe(template.render(context))
