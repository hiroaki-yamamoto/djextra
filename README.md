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
code is lacked for modern web development. For example, you might want to send
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

### ListField
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

## Contribution
Contribution of code is welcome, and the code is tested with tox. Before
sending your pull request, please check you tested your code very well.

## License
This repository is licensed under the terms of MIT License. Please check
[LICENSE.md](LICENSE.md) for the detail.
