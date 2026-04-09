"""
Keep the settings package import side-effect free.

Django imports `www.settings` before loading submodules such as
`www.settings.loc` or `www.settings.prod`. Importing a concrete settings module
here would force production-only environment variables during local runs.
"""
