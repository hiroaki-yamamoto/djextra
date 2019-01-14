# Additional code for Django

[![CI Image]][CI Link] [![Test Coverage]][Test Coverage Link]
[![Maintainability]][Maintainability Link]

[CI Image]: https://circleci.com/gh/hiroaki-yamamoto/djextra.svg?style=svg
[CI Link]: https://circleci.com/gh/hiroaki-yamamoto/djextra
[Test Coverage]: https://api.codeclimate.com/v1/badges/1ed2f1c354e6357d711c/test_coverage
[Test Coverage Link]: https://codeclimate.com/github/hiroaki-yamamoto/djextra/test_coverage
[Maintainability]: https://api.codeclimate.com/v1/badges/1ed2f1c354e6357d711c/maintainability
[Maintainability Link]: https://codeclimate.com/github/hiroaki-yamamoto/djextra/maintainability

## What this?
This repository contains additional code for Django.

## Why I create this?
Because I love Django, and usually using it. However, I found some essential
code was lacked for modern web development. For example, you might want to send
Ajax Payload like this:

```JSON
{
  "name": "John Doe",
  "age": 49,
  "email": "john@example.com",
  "email_aliases": [
    "john.due@example.com",
    "due_49@example.com",
    "john.1968@example.com"
  ]
}
```

In this case, you can validate name, age, and email field by using `Form`
layer on Django. However, email_aliases cannot be validated because it's a
list and it should validate each value whether it is email-formatted or not.

To support this case (and some other cases that Django can't handle), I wrote
some code to support List validation.

## How To Use It

### Forms

#### Angular form
As you can see above sections, you'll need to implement redundant code:

```Python
from django import forms
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # They are already implemented because UserInfoForm inherit ModelForm
    # and the target model has the fields.
    widgets = {
      "age": forms.NumberInput(attrs={"data-ng-model": "model.age"}),
      "phone": forms.TextInput(attrs={"data-ng-model": "model.phone"}),
      "street": forms.TextInput(attrs={"data-ng-model": "model.street"}),
      "city": forms.TextInput(attrs={"data-ng-model": "model.city"}),
      "state": forms.TextInput(attrs={"data-ng-model": "model.state"})
    }
```

However, you can implement simpler code by using `AngularForm`:

```Python
from django import forms
from djextra.forms.angular1 import AngularForm

class UserInfoForm(AngularForm, forms.ModelForm):
  ng_model_prefix = "model" # Change this if you want to use other than "model"
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Automatically generates AngularJS forms.
```

##### Data binding between AngularJS and Django
If you want put the value to scope model on initialization, you might have 2 ways:

1. Serialize your model into json by using `json.dumps` and
  `django.forms.model_to_dict`
2. Set `handle_ng_init` meta attribute

The first one is very clear, convert your model into dict with
`django.forms.model_to_dict`, and serialize the dict into JSON, and finally
put the text as `data-ng-init` to the form like this:

```HTML
<form data-ng-init="model = {{ view.model_dict | tojson }}">
  <!-- bla bla bla bla... -->
</form>
```

The second one is simple; just set `handle_ng_init` Meta attribute of the form to
`True` like this:

```Python
from django import forms
from djextra.forms.angular1 import AngularForm

class UserInfoForm(AngularForm, forms.ModelForm):
  ng_model_prefix = "model" # Change this if you want to use other than "model"
  handle_ng_init = True
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Automatically generates AngularJS forms.
```

If you want to specify what value to be set, you can use `ng_init_format_func`
meta attribute like this:

```Python
from django import forms
from djextra.forms.angular1 import AngularForm

class UserInfoForm(AngularForm, forms.ModelForm):
  ng_model_prefix = "model" # Change this if you want to use other than "model"
  handle_ng_init = True
  ng_init_format_func = {
    "age": lambda value: f"{value} years old"
  }
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Automatically generates AngularJS forms.
```

However, as you know, server-side is quite different from client side, so **to
keep that `age` is formatted, you might also need to write client-side code.**

#### All required forms
If you'd like to make all fields required on ModelForm, you will re-implement
entire fields like this:

```Python
from django import forms
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )

  # Assume that all fields are optional.
  age = forms.IntegerField(
    required=True,
    widget=forms.NumberInput(attrs={"data-ng-model": "model.age"})
  )
  phone = forms.CharField(
    required=True,
    widget=forms.TextInput(attrs={"data-ng-model": "model.phone"})
  )
  street = forms.CharField(
    required=True,
    widget=forms.TextInput(attrs={"data-ng-model": "model.street"})
  )
  city = forms.CharField(
    required=True,
    widget=forms.TextInput(attrs={"data-ng-model": "model.city"})
  )
  state = forms.CharField(
    required=True,
    widget=forms.TextInput(attrs={"data-ng-model": "model.state"})
  )
```

Moreover, you will not be able to check if the field is proper unless you
refer Django's code. To reduce this time consumption, I implemented
`AllReqiuredForm`:

```Python
from django import forms
from djextra.forms.angular1 import AllRequiredForm
from .models import UserInfo

class UserInfoForm(AllRequiredForm, forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Assume that all fields are optional.
```

By using `AllRequiredForm`, you can reduce your LOC like above. Of course,
you can put optional field as exceptions like this:

```Python
from django import forms
from djextra.forms.angular1 import AllRequiredForm
from .models import UserInfo

class UserInfoForm(AllRequiredForm, forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Assume that all fields are optional.
    # By specifying optional, the specified fields won't
    # become a required field.
    optional = ("phone", )
```

#### FieldAttributeForm

When you set attribute, especially with `ModelForm`, you might need to re-set
widget with `widget` Meta attribute like this:

```Python
from django.db import models as db
from django import forms


class NamePrice(db.Model):
  name = db.CharField()
  price = db.IntegerField()


class NameDescForm(forms.ModelForm):
  class Meta(object):
    model = NamePrice
    exclude = ("id", )
    widgets = {
      "price": forms.NumberInput(attrs={"max": "100"})
    }
```

This is okay when you know what widget is used and attribute `max` is the
fixed value. However, if you don't know what widget is used, or `max` is
the dynamic value by the server, Django might not have suitable solution.
To solve this problem, djextra has a form named `FieldAttributeForm` and
you can use it like this:

```Python
from django.db import models as db
from django import forms

from django.conf import settings


class NamePrice(db.Model):
  name = db.CharField()
  price = db.IntegerField()


class NameDescForm(FieldAttributeForm, forms.ModelForm):
  class Meta(object):
    model = NamePrice
    exclude = ("id", )
    fld_attrs = {
        "price": {
            # The point is the attribute can be callable.
            "max": lambda form, fld, name, value: 100 if value else "",
            "min": "0"
        },
    }
```

In addition to this, `FieldAttributeForm` can set attributes that can be applied
to all the fields by using `common_attrs` meta attribute:

```Python
from django.db import models as db
from django import forms

from django.conf import settings


class NamePrice(db.Model):
  name = db.CharField()
  price = db.IntegerField()


class NameDescForm(FieldAttributeForm, forms.ModelForm):
  class Meta(object):
    model = NamePrice
    exclude = ("id", )
    common_attrs = {
      # Also it can be callable.
      "data-on-delay": lambda form, fld, name, value: (
        f"delay('{name}',{value})"
      ),
      "data-on-load": "test()",
    }
    fld_attrs = {
        "price": {
            "max": lambda form, fld, name, value: 100 if value else "",
            "min": 0
        },
    }
```

### Form Fields

#### ListField

ListField is used to handle a list of values like above example.
To use ListField, you can write a form like this:

`forms.py`
```python
from django import forms
from djextra import forms as exforms


class ExampleForm(forms.Form):
  name = forms.CharField()
  age = forms.IntegerField()
  email = forms.EmailField()
  email_aliases = exforms.ListField(field=forms.EmailField())
```

Then, Inputting the data as usual, the validation will start.
If you don't specify `field` keyword argument, `django.forms.CharField` object
is specified.

### Widgets

#### Widgets for Angular Materials

If you like [Material Design], you'd also like to use [Angular Material], but
as you can see the doc. the components are using special tags. For example,
`select` and `option` input controllers should be replaced with `mdSelect` and
`mdOption` and they are not provided by built-in widgets.

This widget provides the widgets:

```Python
from django import forms
from djextra.forms.angular1 import (
  AngularForm, MDSelect, MDMultiSelect, MDDatePicker, MDDateSelect, MDCheckBox
)

from .models import ExampleModel

class ExampleForm(AngularForm, forms.ModelForm):
  class Meta(object):
    model = ExampleModel
    exclude = ("secret_field", )
    widgets = {
      "start_since": MDDateSelect(),
      "available_date": MDDatePicker(),
      "shape": MDSelect(choices=(
        ("F", "Fat"), ("N": "Normal"), ("T", "Thin")
      )),
      "needs_fill": MDCheckBox("Fill with border color?")
    }
```

[Material Design]: https://material.google.com/
[Angular Material]: https://material.angularjs.org


## Contribution
Contribution of code is welcome, and the code is tested with tox. Before
sending your pull request, please check you tested your code very well.

## License
This repository is licensed under the terms of MIT License. Please check
[LICENSE.md](LICENSE.md) for the detail.
