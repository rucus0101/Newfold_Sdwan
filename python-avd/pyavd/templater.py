# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, ModuleLoader, StrictUndefined

from .constants import JINJA2_EXTENSIONS, JINJA2_PRECOMPILED_TEMPLATE_PATH
from .j2filters.add_md_toc import add_md_toc
from .j2filters.convert_dicts import convert_dicts
from .j2filters.default import default
from .j2filters.generate_esi import generate_esi
from .j2filters.generate_route_target import generate_route_target
from .j2filters.hide_passwords import hide_passwords
from .j2filters.list_compress import list_compress
from .j2filters.natural_sort import natural_sort


class Undefined(StrictUndefined):
    """
    Allow nested checks for undefined instead of having to check on every level.
    Example "{% if var.key.subkey is arista.avd.undefined %}" is ok.

    Without this it we would have to test every level, like
    "{% if var is arista.avd.undefined or var.key is arista.avd.undefined or var.key.subkey is arista.avd.undefined %}"
    """

    def __getattr__(self, name):
        # Return original Undefined object to preserve the first failure context
        return self

    def __getitem__(self, key):
        # Return original Undefined object to preserve the first failure context
        return self

    def __repr__(self):
        return f"Undefined(hint={self._undefined_hint}, obj={self._undefined_obj}, name={self._undefined_name})"

    def __contains__(self, item):
        # Return original Undefined object to preserve the first failure context
        return self


class Templar:
    def __init__(self, searchpaths: list[str] = None):
        self.loader = ChoiceLoader(
            [
                ModuleLoader(JINJA2_PRECOMPILED_TEMPLATE_PATH),
                FileSystemLoader(searchpaths or []),
            ]
        )

        # Accepting SonarLint issue: No autoescaping is ok, since we are not using this for a website, so XSS is not applicable.
        self.environment = Environment(  # NOSONAR
            extensions=JINJA2_EXTENSIONS,
            loader=self.loader,
            undefined=Undefined,
            trim_blocks=True,
        )
        self.import_filters_and_tests()

    def import_filters_and_tests(self) -> None:
        # pylint: disable=import-outside-toplevel
        from .vendor.j2.filter.decrypt import decrypt
        from .vendor.j2.filter.encrypt import encrypt
        from .vendor.j2.filter.range_expand import range_expand
        from .vendor.j2.test.contains import contains
        from .vendor.j2.test.defined import defined

        # pylint: enable=import-outside-toplevel

        self.environment.filters.update(
            {
                "arista.avd.add_md_toc": add_md_toc,
                "arista.avd.convert_dicts": convert_dicts,
                "arista.avd.decrypt": decrypt,
                "arista.avd.default": default,
                "arista.avd.encrypt": encrypt,
                "arista.avd.generate_esi": generate_esi,
                "arista.avd.generate_route_target": generate_route_target,
                "arista.avd.hide_passwords": hide_passwords,
                "arista.avd.list_compress": list_compress,
                "arista.avd.natural_sort": natural_sort,
                "arista.avd.range_expand": range_expand,
            }
        )
        self.environment.tests.update(
            {
                "arista.avd.defined": defined,
                "arista.avd.contains": contains,
            }
        )

    def render_template_from_file(self, template_file: str, template_vars: dict) -> str:
        return self.environment.get_template(template_file).render(template_vars)

    def compile_templates_in_paths(self, searchpaths: list[str]) -> None:
        print(JINJA2_PRECOMPILED_TEMPLATE_PATH)
        self.environment.loader = FileSystemLoader(searchpaths)
        self.environment.compile_templates(
            zip=None,
            log_function=print,
            target=JINJA2_PRECOMPILED_TEMPLATE_PATH,
            ignore_errors=False,
        )
        self.environment.loader = self.loader
