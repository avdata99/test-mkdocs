# Common errors for the `build-config` command

Errors:

 - `jinja2.exceptions.UndefinedError: 'variable' is undefined`: You are using some `{{ variable }}`
   in your template that is not defined in your config file.
   - Is the `variable` is defined, check you are not using a `variable-with-dashes` in your template.
     You need to use `variable_with_underscore` instead.