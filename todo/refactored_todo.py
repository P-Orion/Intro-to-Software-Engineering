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
        # Using direct string comparison since this is a static method with regular strings, not Var objects
        # This is safe because we're not in a reactive context here
        if priority == Priority.HIGH.value:
            return "red"
        elif priority == Priority.MEDIUM.value:
            return "blue"
        else:
            return "gray"
    
    @staticmethod
    def get_priority_color_reactive(priority: rx.Var) -> rx.Var:
        """Get the color scheme for a priority level in a reactive context."""
        # Using rx.cond for reactive contexts where priority might be a Var
        return rx.cond(
            priority == Priority.HIGH.value,
            "red",
            rx.cond(
                priority == Priority.MEDIUM.value,
                "blue",
                "gray"
            )
        )
    
    @staticmethod
    def create_priority_badge(priority: str) -> rx.Component:
        """Create a badge component for displaying priority."""
        return rx.badge(
            priority,
            # Use the reactive version for the badge since it's in a reactive context
            color_scheme=UIComponentLibrary.get_priority_color_reactive(priority),
            variant="solid",
            border_radius="full",
            padding_x="0.75rem",
            padding_y="0.25rem",
            font_weight="medium",
            font_size="0.8rem",
            min_width="4.5rem", # Fixed minimum width for consistency
            text_align="center", # Center text in badge
            align_self="center", # Center vertically
            display="flex", # Use flexbox for better centering
            justify_content="center", # Center horizontally
            align_items="center", # Center vertically
            height="1.75rem", # Fixed height for consistency
            line_height="1", # Tighter line height for better centering
        )
    
    @staticmethod
    def create_todo_item_component(item: Dict[str, str], on_complete: Callable) -> rx.Component:
        """Create a component for displaying a todo item."""
        return rx.list_item(
            rx.hstack(
                # Checkmark button with consistent sizing
                rx.button(
                    rx.icon(tag="check", size=16),
                    on_click=lambda: on_complete(item),
                    height="2rem",
                    width="2rem",
                    min_height="2rem",
                    min_width="2rem",
                    padding="0",
                    variant="outline",
                    color_scheme="green",
                    border_radius="full",
                    _hover={"bg": "green.50"},
                    transition="all 0.2s",
                    margin="0", # Remove any default margins
                ),
                # Task text with proper alignment
                rx.text(
                    item["text"], 
                    as_="span", 
                    margin_left="0.75rem",
                    font_size="1rem",
                    font_weight="medium",
                    line_height="1.5rem", # Consistent line height
                    overflow="hidden", # Prevent text overflow
                    text_overflow="ellipsis", # Add ellipsis for long text
                    align_self="center", # Center vertically
                ),
                rx.spacer(),
                # Priority badge with improved styling
                UIComponentLibrary.create_priority_badge(item["priority"]),
                align_items="center",
                width="100%",
                spacing="3", # Consistent spacing
                padding="0.25rem", # Add padding inside the hstack
            ),
            padding_y="0.5rem", # Consistent vertical padding
            padding_x="0.25rem", # Add horizontal padding
            border_bottom="1px solid",
            border_color="gray.100",
            _hover={"bg": "gray.50"},
            transition="all 0.2s",
            margin_y="0.25rem", # Add vertical margin between items
            width="100%", # Ensure full width
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
                rx.vstack(
                    # Input field with fixed height to prevent text cutting
                    rx.input(
                        placeholder="Add a todo...",
                        name="new_item",
                        size="2", # Medium size for better text display
                        border_width="1px",
                        border_color="gray.300",
                        _focus={"border_color": "blue.400"},
                        border_radius="md",
                        height="2.5rem", # Fixed height to prevent text cutting
                        min_height="2.5rem", # Ensure minimum height
                        padding_y="0", # Remove vertical padding that might cut text
                        padding_x="0.75rem", # Horizontal padding
                        width="100%",
                    ),
                    # Priority selector with consistent styling
                    rx.select(
                        priority_levels,
                        placeholder="Priority",
                        name="priority",
                        default_value="Medium",
                        size="2",
                        border_width="1px",
                        border_color="gray.300",
                        _focus={"border_color": "blue.400"},
                        border_radius="md",
                        height="2.5rem", # Fixed height to match input
                        min_height="2.5rem", # Ensure minimum height
                        width="100%",
                        margin_top="2",
                    ),
                    width="100%",
                    spacing="2",
                    flex_grow=1,
                ),
                # Add button with consistent height
                rx.button(
                    "Add",
                    type="submit",
                    color_scheme="blue",
                    size="2",
                    height="2.5rem", # Fixed height to match input
                    min_height="2.5rem", # Ensure minimum height
                    border_radius="md",
                    _hover={"bg": "blue.600"},
                    margin_left="3",
                    align_self="flex_start", # Align with the top input
                ),
                width="100%",
                align_items="flex_start", # Align items at the top
                spacing="3",
            ),
            on_submit=on_submit,
            reset_on_submit=True,
            width="100%",
            margin_bottom="4",
        )


# --- Main Application ---

class TodoApp:
    """Main application class that ties everything together."""
    
    @staticmethod
    def create_page() -> rx.Component:
        """Create the main page of the application."""
        return rx.container(
            rx.vstack(
                # App header with improved styling and spacing
                rx.box(
                    rx.heading(
                        "Todo Manager", 
                        size="1", 
                        color="blue.600",
                        font_weight="bold",
                        margin="0", # Remove default margin
                        padding="0", # Remove default padding
                        line_height="1.2", # Tighter line height
                    ),
                    rx.text(
                        "Manage your tasks with priorities",
                        color="gray.600",
                        font_size="1rem",
                        margin_top="0.5rem",
                        padding="0", # Remove default padding
                    ),
                    text_align="center",
                    width="100%",
                    padding_y="1rem",
                    margin_bottom="1rem", # Add bottom margin
                ),
                
                # Form to add new items
                UIComponentLibrary.create_new_item_form(
                    TodoState.add_todo_item,
                    Priority.get_all_values()
                ),
                
                # Visual separator with consistent styling
                rx.divider(
                    border_color="gray.200",
                    border_width="1px",
                    margin_y="1.5rem",
                    opacity="0.6", # Slightly transparent
                ),
                
                # Section header centered
                rx.box(
                    rx.heading(
                        "Your Tasks",
                        size="3",
                        color="gray.700",
                        margin="0", # Remove default margin
                        padding="0", # Remove default padding
                        font_size="1.25rem", # Explicit font size
                    ),
                    width="100%",
                    margin_bottom="0.75rem",
                    text_align="center", # Center the heading
                ),
                
                # Todo list with proper spacing
                rx.box(
                    UIComponentLibrary.create_todo_list(
                        TodoState.items,
                        TodoState.complete_todo_item
                    ),
                    width="100%",
                    padding="0.5rem 0", # Add vertical padding
                ),
                
                # Footer with consistent styling
                rx.text(
                    "Click the checkmark to complete a task",
                    color="gray.500",
                    font_size="0.8rem",
                    margin_top="1rem",
                    text_align="center",
                    padding="0", # Remove default padding
                ),
                
                align_items="stretch", # Stretch items to fill container width
                spacing="3", # Consistent spacing between elements
                width="100%", # Ensure vstack takes full width
                max_width="600px", # Limit max width for better readability
                margin="2rem auto", # Center horizontally with top/bottom margin
                padding="1.5rem", # Consistent padding
                border="1px solid #ddd", # Light border
                border_radius="lg", # Rounded corners
                box_shadow="md", # Lighter shadow for better appearance
                background_color="white", # White background
                overflow="hidden", # Prevent content overflow
            ),
            center_content=True, # Center the main vstack container
            padding="1rem", # Reduced padding for better mobile view
            max_width="100%", # Allow container to use full width
            min_height="100vh", # Minimum height to fill viewport
            background="linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)", # Gradient background
        )


# --- Application Setup ---

# Create the state class
class TodoState(TodoStateManager):
    """The application state."""
    pass


# Create app instance and add page
app = rx.App()
app.add_page(TodoApp.create_page, title="Todo Manager")
# Changed from app.compile() to fix the AttributeError
