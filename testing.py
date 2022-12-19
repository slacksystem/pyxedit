import sys

print(sys.executable)
from rich import print  # noqa: E402

from pyxedit import XEdit  # noqa: E402
from pyxedit.xedit.base import XEditBase  # noqa: E402


def print_all_elements(element: XEditBase):
    print(element.name, element.value)
    if element.has_child_group():
        for subelement in element.child_elements():
            print_all_elements(subelement)


if __name__ == "__main__":
    with XEdit(plugins=["Dawnguard.esm"]).session() as xedit:
        skyrim = xedit["Skyrim.esm"]
        iron_shield = skyrim["ARMO\\ArmorIronShield"]

        print(dir(skyrim))
        print(dir(iron_shield))

        print(xedit.plugins)

        print_all_elements(iron_shield)
