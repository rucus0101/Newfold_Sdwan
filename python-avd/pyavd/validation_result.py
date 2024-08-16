# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .vendor.errors import AvdDeprecationWarning, AvdValidationError


class ValidationResult:
    """
    Object containing result of data validation

    Attributes:
        failed: True if data is not valid according to the schema. Otherwise False.
        validation_errors: List of AvdValidationErrors containing schema violations.
        deprecation_warnings: List of AvdDeprecationWarnings containing warning for deprecated inputs.
    """

    failed: bool
    validation_errors: list[AvdValidationError]
    deprecation_warnings: list[AvdDeprecationWarning]

    def __init__(self, failed: bool, validation_errors: list = None, deprecation_warnings: list = None):
        self.failed = failed
        self.validation_errors = validation_errors or []
        self.deprecation_warnings = deprecation_warnings or []
