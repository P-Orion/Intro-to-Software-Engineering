"""Welcome to Reflex! This file outlines the steps to create a basic app with proper structure."""
import reflex as rx
from typing import List, Dict, Any, Optional, Callable, TypeVar, Generic, Union
from enum import Enum
from dataclasses import dataclass, field

# --- Domain Models ---

class Priority(Enum):
    """Enumeration of priority levels for better type safety."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    
    @classmethod
    def get_all_values(cls) -> List[str]:
        """Return all priority values as strings."""
        return [p.value for p in cls]
    
    @classmethod
    def from_string(cls, value: str) -> 'Priority':
        """Convert string to Priority enum."""
        for priority in cls:
            if priority.value == value:
                return priority
        return cls.MEDIUM  # Default to medium if not found


@dataclass
class TodoItem:
    """Class representing a todo item with its properties."""
    text: str
    priority: Priority
    
    @classmethod
    def create(cls, text: str, priority_str: str) -> Optional['TodoItem']:
        """Factory method to create a TodoItem from raw values."""
        if not text or not text.strip():
            return None
            
        priority = Priority.from_string(priority_str)
        return cls(text=text.strip(), priority=priority)
    
    def to_dict(self) -> Dict[str, str]:
        """Convert TodoItem to dictionary for storage/display."""
        return {
            "text": self.text,
            "priority": self.priority.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'TodoItem':
        """Create TodoItem from dictionary."""
        return cls(
            text=data.get("text", ""),
            priority=Priority.from_string(data.get("priority", "Medium"))
        )


# --- State Management ---

class TodoStateManager(rx.State):
    """Class responsible for managing todo items state."""
    
    # Store items as dictionaries for compatibility with Reflex
    items: List[Dict[str, str]] = field(default_factory=lambda: [
        {"text": "Write Code", "priority": "Medium"},
        {"text": "Sleep", "priority": "High"},
        {"text": "Have Fun", "priority": "Low"},
    ])
    
    @property
    def todo_items(self) -> List[TodoItem]:
        """Convert stored dictionaries to TodoItem objects."""
        return [TodoItem.from_dict(item) for item in self.items]
    
    def add_todo_item(self, form_data: Dict[str, str]) -> None:
        """Add a new todo item with validation."""
        new_text = form_data.get("new_item", "")
        new_priority = form_data.get("priority", "Medium")
        
        # Create item using factory method with validation
        new_item = TodoItem.create(new_text, new_priority)
        
        if new_item:
            self.items.append(new_item.to_dict())
            self._sort_items_by_priority()
    
    def complete_todo_item(self, item: Dict[str, str]) -> None:
        """Mark a todo item as completed and remove it."""
        if item in self.items:
            self.items.remove(item)
    
    def _sort_items_by_priority(self) -> None:
        """Sort items by priority (High > Medium > Low)."""
        priority_order = {
            "High": 0,
            "Medium": 1,
            "Low": 2
        }
        self.items.sort(key=lambda x: priority_order.get(x.get("priority", "Medium"), 1))


# --- UI Components ---

class UIComponentLibrary:
    """Library of UI component creation functions."""
    
    @staticmethod
    def get_priority_color(priority: str) -> str:
        """Get the color scheme for a priority level."""
        if priority == Priority.HIGH.value:
            return "red"
        elif priority == Priority.MEDIUM.value:
            return "blue"
        else:
            return "gray"
    
    @staticmethod
    def create_priority_badge(priority: str) -> rx.Component:
        """Create a badge component for displaying priority."""
        return rx.badge(
            priority,
            color_scheme=UIComponentLibrary.get_priority_color(priority),
            variant="solid",
            border_radius="full",
            padding_x="0.75em",
        )
    
    @staticmethod
    def create_todo_item_component(item: Dict[str, str], on_complete: Callable) -> rx.Component:
        """Create a component for displaying a todo item."""
        return rx.list_item(
            rx.hstack(
                rx.button(
                    rx.icon(tag="check", size=20),
                    on_click=lambda: on_complete(item),
                    height="auto",
                    padding="0.25em",
                    variant="outline",
                    color_scheme="green",
                ),
                rx.text(item["text"], as_="span", margin_left="0.5em"),
                rx.spacer(),
                UIComponentLibrary.create_priority_badge(item["priority"]),
                align_items="center",
                width="100%",
            ),
            padding_y="0.25em",
        )
    
    @staticmethod
    def create_todo_list(items: List[Dict[str, str]], on_complete: Callable) -> rx.Component:
        """Create a component for displaying the todo list."""
        return rx.ordered_list(
            rx.foreach(
                items, 
                lambda item: UIComponentLibrary.create_todo_item_component(item, on_complete)
            ),
            list_style_type="none",
            padding_left="0",
            width="100%",
        )
    
    @staticmethod
    def create_new_item_form(on_submit: Callable, priority_levels: List[str]) -> rx.Component:
        """Create a form for adding new todo items."""
        return rx.form(
            rx.hstack(
                rx.input(
                    placeholder="Add a todo...",
                    name="new_item",
                    flex_grow=1,
                ),
                rx.select(
                    priority_levels,
                    placeholder="Priority",
                    name="priority",
                    default_value="Medium",
                ),
                rx.button(
                    "Add",
                    type="submit",
                    color_scheme="blue",
                ),
                align_items="center",
                spacing="3",
            ),
            on_submit=on_submit,
            reset_on_submit=True,
            width="100%",
        )


# --- Main Application ---

class TodoApp:
    """Main application class that ties everything together."""
    
    @staticmethod
    def create_page() -> rx.Component:
        """Create the main page of the application."""
        return rx.container(
            rx.vstack(
                rx.heading("Todo Manager", size="xl"),
                UIComponentLibrary.create_new_item_form(
                    TodoState.add_todo_item,
                    Priority.get_all_values()
                ),
                rx.divider(border_color="gray.200"),
                UIComponentLibrary.create_todo_list(
                    TodoState.items,
                    TodoState.complete_todo_item
                ),
                align_items="stretch",
                spacing="5",
                width="100%",
                max_width="600px",
                margin_top="2em",
                padding="1em",
                border="1px solid #ddd",
                border_radius="lg",
                box_shadow="md",
            ),
            center_content=True,
        )


# --- Application Setup ---

# Create the state class
class TodoState(TodoStateManager):
    """The application state."""
    pass


# Create app instance and add page
app = rx.App()
app.add_page(TodoApp.create_page, title="Todo Manager")
app.compile()
