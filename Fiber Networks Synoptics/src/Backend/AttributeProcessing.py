import re


def get_fibers(block, tag: str) -> int:  # Only for attribute value of type "\d+FO - \d+m"
    value = block.get_attrib(tag)
    numbers = re.findall(r'\d+', value)
    return int(numbers[0])


def get_length(block, tag: str) -> int:
    value = block.get_attrib(tag)
    numbers = re.findall(r'\d+', value)
    return int(numbers[1])


def get_houses(block, tag: str) -> int:
    value = block.get_attrib(tag)
    numbers = re.findall(r'\d+', value)
    return int(numbers[0])


def get_jso_from_pdo(block, tag: str) -> str:
    value = block.get_attrib(tag)
    number = int(re.findall(r'\d+', value)[0])
    return "JSO" + str(number-1)


def get_cable_network(block) -> str:
    value = block.dxf.layer
    network = re.split('-', value)
    return network[1]


def get_cable_type(block) -> str:
    value = block.dxf.layer
    network = re.split('-', value)
    return network[2]


def get_cable_id(cable: str) -> str:
    cable_id = re.split(' ', cable)
    return cable_id[0]


def get_block(idetifier: str, pdo_list: list):
    for pdo in pdo_list:
        if pdo.identifier == idetifier:
            return pdo

