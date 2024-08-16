# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from .constants import JINJA2_DOCUMENTAITON_TEMPLATE
from .j2filters.add_md_toc import add_md_toc as filter_add_md_toc
from .templater import Templar


def get_device_doc(structured_config: dict, add_md_toc: bool = False) -> str:
    """
    Render and return the device documentation using AVD eos_cli_config_gen templates.

    Args:
        structured_config: Dictionary with structured configuration.
            Variables should be converted and validated according to AVD `eos_cli_config_gen` schema first using `pyavd.validate_structured_config`.
        add_md_toc: Add a table of contents for markdown headings.

    Returns:
        Device documentation in Markdown format.
    """

    templar = Templar()
    result: str = templar.render_template_from_file(JINJA2_DOCUMENTAITON_TEMPLATE, structured_config)
    if add_md_toc:
        return filter_add_md_toc(result, skip_lines=3)

    return result
