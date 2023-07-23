from typing import Iterator, List
from textual.widget import Widget
from dooit.api.todo import Todo
from dooit.ui.widgets.inputs import (
    Description,
    Due,
    Effort,
    Recurrence,
    Status,
    Urgency,
)
from dooit.ui.widgets.simple_input import SimpleInput
from dooit.ui.widgets.utils import Padding
from .node import Node


class ExpandedHorizontal(Widget):
    DEFAULT_CSS = """
    ExpandedHorizontal {
        layout: horizontal;
        height: auto;
    }
    """

    def on_mount(self) -> None:
        self.styles.width = "1fr"


class TodoWidget(Node):
    ModelType = Todo

    def setup_children(self):
        self.status = Status(model=self.model)
        self.description = Description(model=self.model)
        self.effort = Effort(model=self.model)
        self.recurrence = Recurrence(model=self.model)
        self.due = Due(model=self.model)
        self.urgency = Urgency(model=self.model)

    def get_child_inputs(self) -> List[SimpleInput]:
        return [
            self.status,
            self.description,
            self.description,
            self.effort,
            self.recurrence,
            self.due,
            self.urgency,
        ]

    def _get_model_children(self) -> List[ModelType]:
        return self.model.todos

    async def increase_urgency(self):
        self.model.increase_urgency()
        await self.refresh_value()

    async def decrease_urgency(self):
        self.model.decrease_urgency()
        await self.refresh_value()

    async def toggle_complete(self):
        self.model.toggle_complete()

        parent = self.parent
        while parent:
            if not isinstance(parent, TodoWidget):
                break

            await parent.refresh_value()
            parent = parent.parent

        await self.refresh_value()

    def draw(self) -> Iterator[Widget]:
        with ExpandedHorizontal():
            yield self.pointer
            yield Padding(self.model.nest_level)

            with ExpandedHorizontal():
                yield self.status
                yield self.description
                yield self.effort
                yield self.recurrence

            yield self.due
            yield self.urgency
