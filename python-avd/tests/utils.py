# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
import os
from json import JSONDecodeError
from json import loads as json_loads
from sys import stdin

from yaml import unsafe_load as yaml_load


def read_file(filename: str) -> str:
    if filename == "/dev/stdin" and stdin.isatty():
        print("Write variables in YAML or JSON format and end with ctrl+d to exit")
    with open(filename, "r", encoding="UTF-8") as file:
        return file.read()


def read_vars(filename: str):
    data = read_file(filename)

    try:
        return json_loads(data)
    except JSONDecodeError:
        pass

    return yaml_load(data) or {}


def write_result(filename, result):
    mode = "w+"
    if filename == "/dev/stdout":
        mode = "w"

    with open(filename, mode, encoding="UTF-8") as file:
        file.write(result)


def create_common_vars(common_varfiles):
    common_vars = {}
    for file in common_varfiles:
        common_vars.update(read_vars(file))
    return common_vars


def get_files_in_folder(folder_path):
    files = []
    for root, dir, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files
