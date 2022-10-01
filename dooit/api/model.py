from typing import Callable, Optional
from functools import partial


class Model:
    _ctype_counter: int = 0
    nomenclature: str = "Workspace"
    fields = []

    def __init__(
        self,
        name: str,
        parent: Optional["Model"] = None,
    ) -> None:
        self.name = name
        self.parent = parent
        self.children: list["Model"] = []
        self.ctype: Callable = type(self)

    def _get_child_index(self, name: str) -> int:

        for i, j in enumerate(self.children):
            if j.name == name:
                return i

        return -1

    def _get_child(self, name) -> "Model":
        return self.children[name]

    def edit(self, key: str, value: str):
        func = eval(f"self.set_{key}")
        callback = partial(func, value)
        return callback()

    def add_child(self, index: Optional[int] = None):

        self._ctype_counter += 1
        child = self.ctype(
            name=f"{self.name}/{self.nomenclature}#{self._ctype_counter}".lstrip(
                "Manager/"
            ),
            parent=self,
        )

        if index:
            self.children.insert(index, child)
        else:
            self.children.append(child)

    def remove_child(self, name: str):
        self._get_child_index(name)

    def drop(self):
        if self.parent:
            self.parent.remove_child(self.name)

    def sort_children(self, field: str):
        self.children.sort(key=lambda x: getattr(x, field))

    def get_export(self):
        return {getattr(child, "name"): child.get_export() for child in self.children}

    @classmethod
    def from_export(cls):
        pass
