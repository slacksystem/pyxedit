import sys

print(sys.executable)
from rich import print  # noqa: E402

from pyxedit.xedit import XEdit  # noqa: E402
from pyxedit.xedit.base import XEditBase  # noqa: E402


def find_parent_record(element: XEditBase):
    if element.signature:
        return element
    else:
        return find_parent_record(element.parent)


setattr(XEditBase, "find_parent_record", find_parent_record)


def print_all_elements(element: XEditBase):
    try:
        value = element.value
    except NotImplementedError:
        value = None
    data = dict(
        element_name=element.name,
        element_value=value,
        element_num_child_elements=element.num_child_elements,
        element_signature=element.signature,
        element_parent_record=element.find_parent_record(),
    )
    print(data)
    if element.num_child_elements:
        print("Has child group")
        for subelement in element.child_elements:
            print_all_elements(subelement)


if __name__ == "__main__":
    with XEdit(plugins=["Dawnguard.esm"]).session() as xedit:
        skyrim = xedit["Skyrim.esm"]
        iron_shield = skyrim["ARMO\\ArmorIronShield"]

        print(dir(skyrim))
        print(dir(iron_shield))

        print(xedit.plugins)

        print_all_elements(iron_shield)
