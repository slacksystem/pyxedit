from io import TextIOWrapper
from typing import Any, Callable, Iterable, Iterator, List

from rich.pretty import Pretty
from rich.console import Console

from pyxedit.xedit.object_classes import (  # noqa: F401
    ACHR,
    ARMA,
    ARMO,
    CELL,
    FLST,
    GLOB,
    HDPT,
    KYWD,
    NAVM,
    NPC_,
    OBND,
    RACE,
    REFR,
    TXST,
    VMAD,
)  # noqa: F401

from pyxedit.xedit import XEdit  # noqa: E402
from pyxedit.xedit.base import XEditBase  # noqa: E402
from pyxedit.xedit.generic import XEditGenericObject
from pyxedit.xedit.plugin import XEditPlugin


# logging.basicConfig(level="DEBUG", handlers=[logging.StreamHandler(), RichHandler(rich_tracebacks=True)])

#  logger = logging.getLogger(__name__)


def find_parent_record(element: XEditBase) -> XEditBase:
    if element.signature:
        return element
    else:
        return find_parent_record(element.parent)  # type: ignore


setattr(XEditBase, "find_parent_record", find_parent_record)


def get_all_elements(element: XEditBase) -> List | str:
    if element.num_child_elements:
        element_list = []
        for subelement in element.child_elements:
            element_list.append(get_all_elements(subelement))
        return [element.long_name, element_list]
    else:
        return_string = element.long_name
        try:
            if element.value:  # type: ignore
                return_string += f": {element.value}"  # type: ignore
        except NotImplementedError:
            pass
        return return_string


# This function with no parameters that returns a
# list of all subclasses of xEditBase
def list_types() -> Pretty:
    all_types = Pretty(XEditGenericObject.__subclasses__())
    return all_types


class ConsoleCollection:
    """
    A class that represents a collection of rich Console objects.
    """

    def __init__(self, *args: Console) -> None:
        self.consoles = [arg for arg in args if isinstance(arg, Console)]
        for method in [
            att for att in Console().__dir__() if callable(getattr(Console, att))
        ]:

            def wrapper(method) -> Callable[..., list[Any]]:
                def wrapped(self, *args, **kwargs) -> list[Any]:
                    return [
                        getattr(console, method)(*args, **kwargs)
                        for console in self.consoles
                    ]

                return wrapped

            setattr(self, method, wrapper(method))
        self.__dict__.update(dict([(c.__class__.__name__, c) for c in self.consoles]))

    def __repr__(self) -> str:
        return f"ConsoleCollection({self.consoles})"

    def __str__(self) -> str:
        return f"ConsoleCollection({self.consoles})"

    def __iter__(self) -> Iterator[Console]:
        return iter(self.consoles)

    def __getitem__(self, item: int) -> Console:
        return self.consoles[item]

    def __getslice__(self, i: int, j: int) -> "ConsoleCollection":
        return ConsoleCollection(*self.consoles[i:j])

    def __setslice__(self, i: int, j: int, value: Iterable[Console]) -> None:
        self.consoles[i:j] = value

    def __len__(self) -> int:
        return len(self.consoles)

    def __contains__(self, item: object) -> bool:
        return item in self.consoles

    def __add__(self, other: "ConsoleCollection") -> "ConsoleCollection":
        return ConsoleCollection(*self.consoles + other.consoles)

    def __iadd__(self, other: "ConsoleCollection") -> "ConsoleCollection":
        self.consoles += other.consoles
        return self

    def __mul__(self, other: int) -> "ConsoleCollection":
        return ConsoleCollection(*self.consoles * other)

    def __imul__(self, other: int) -> "ConsoleCollection":
        self.consoles *= other
        return self

    def __rmul__(self, other: int) -> "ConsoleCollection":
        return self * other


if __name__ == "__main__":
    with XEdit(
        plugins=["kxWhereAreYou.esp"],
    ).session() as xedit:
        skyrim = xedit["Skyrim.esm"]
        # iron_shield = skyrim["ARMO\\ArmorIronShield"]
        kxWAY: XEditPlugin = xedit["kxWhereAreYou.esp"]  # type: ignore

        # print(dir(skyrim))
        # print(dir(iron_shield))

        # print(xedit.plugins)
        try:
            logfile: TextIOWrapper = open("logs/pyxedit.log", "a")
            console: Console = Console()
            console_file: Console = Console(file=logfile)

            def print(*args, **kwargs) -> None:
                console.print(*args, **kwargs)
                console_file.print(*args, **kwargs)

            # console.rule(f"[bold cyan]{iron_shield.name}", align="left")  # type: ignore
            # pretty = Pretty(get_all_elements(iron_shield), expand_all=True)  # type: ignore
            # console.print(pretty)
            console.rule(f"[bold cyan]{kxWAY.name}", align="left")  # type: ignore
            kxWAY.ls
            print(get_all_elements(kxWAY))

            # for spell in spells:
            #     console.print(spell.name)
            # for item in xedit:
            #     console.print(item)
        finally:
            logfile.close()
