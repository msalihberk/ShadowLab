from core.enums.msg_types import TYPE
from cli.printer import CLIPrinter
from tabulate import tabulate


def flatten_dict(data, parent_key: str = "", sep: str = "."):
    items = {}

    if isinstance(data, dict):
        iterable = data.items()
    elif isinstance(data, list):
        iterable = enumerate(data)
    else:
        return {parent_key: data}

    for key, value in iterable:
        if value is None or value == {}:
            continue

        new_key = f"{parent_key}{sep}{key}" if parent_key else str(key)

        if isinstance(value, (dict, list)):
            items.update(flatten_dict(value, new_key, sep=sep))
        else:
            items[new_key] = value

    return items


def print_response_table(response: dict, tablefmt: str = "fancy_grid"):
    flat_data = flatten_dict(response)

    table_rows = [[k, v] for k, v in flat_data.items()]

    print(tabulate(table_rows, headers=["Key", "Value"], tablefmt=tablefmt))


class ResponseProcessor:
    @staticmethod
    def process(data: dict):
        try:
            if data["msg_type"] == TYPE.JSON:
                ResponseProcessor._process_json(data)
            elif data["msg_type"] == TYPE.FILE:
                ResponseProcessor._process_file(data)
        except KeyError:
            CLIPrinter.error("msg_type not found in the data")

    @staticmethod
    def _process_file(data: dict):
        pass

    @staticmethod
    def _process_json(data: dict):
        print_response_table(data)


