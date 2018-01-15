# Additional code for Django

[![Travis CI Image]][Travis CI Link] [![Coveralls Image]][Coveralls Link]
[![Code Climate Maintainability Check Image]][Code Climate Maintainability Check Link]

[Travis CI Image]: https://travis-ci.org/hiroaki-yamamoto/djextra.svg?branch=master
[Travis CI Link]: https://travis-ci.org/hiroaki-yamamoto/djextra
[Coveralls Image]: https://coveralls.io/repos/github/hiroaki-yamamoto/djextra/badge.svg?branch=master
[Coveralls Link]: https://coveralls.io/github/hiroaki-yamamoto/djextra?branch=master
[Code Climate Maintainability Check Image]: https://api.codeclimate.com/v1/badges/1ed2f1c354e6357d711c/maintainability
[Code Climate Maintainability Check Link]: https://codeclimate.com/github/hiroaki-yamamoto/djextra/maintainability

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

#### Feature 2: All required forms
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
