"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
from typing import List, Dict, Any # CHANGED: Imported Dict and Any for typing

class State(rx.State):
    """The app state."""

    # CHANGED: items is now a list of dictionaries, each containing 'text' and 'priority'.
    # Added initial priorities.
    items: List[Dict[str, str]] = [
        {"text": "Write Code", "priority": "Medium"},
        {"text": "Sleep", "priority": "High"},
        {"text": "Have Fun", "priority": "Low"},
    ]
    # ADDED: Define available priority levels
    priority_levels: List[str] = ["Low", "Medium", "High"]

    # CHANGED: add_item now accepts form_data which includes 'new_item' text and 'priority'.
    def add_item(self, form_data: Dict[str, str]):
        """Add a new item to the todo list with priority."""
        new_text = form_data.get("new_item", "").strip() # Get item text
        new_priority = form_data.get("priority", "Medium") # Get priority, default to Medium

        if new_text: # Only add if text is not empty
            # CHANGED: Append a dictionary with text and priority
            self.items.append({"text": new_text, "priority": new_priority})
            # Optional: Sort items after adding, e.g., by priority
            # self.sort_items()

    # CHANGED: finish_item now needs to find the correct dictionary to remove.
    # It receives the whole item dictionary as an argument.
    def finish_item(self, item: Dict[str, str]):
        """Mark an item as finished and remove it."""
        # Find the item in the list and remove it
        # This assumes the exact dictionary object is passed.
        # If Reflex passes a copy, a more robust find mechanism might be needed (e.g., by unique ID if added later)
        if item in self.items:
             self.items.remove(item)


# --- UI Components ---

# Improved todo item with better alignment and consistent spacing
def todo_item(item: Dict[str, str]) -> rx.Component:
    """Render a single todo item with its priority."""
    return rx.list_item(
        rx.hstack(
            # Checkmark button with consistent sizing
            rx.button(
                rx.icon(tag="check", size=16),
                on_click=lambda: State.finish_item(item),
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
            rx.spacer(), # Add spacer to push badge to the right
            # Priority badge with improved centering
            rx.badge(
                item["priority"],
                color_scheme=rx.cond(
                    item["priority"] == "Medium",
                    "blue",
                    rx.cond(
                        item["priority"] == "High",
                        "red",
                        "gray"
                    )
                ),
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
            ),
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

# CHANGED: todo_list passes the dictionary item to todo_item.
def todo_list() -> rx.Component:
    """Render the list of todo items."""
    return rx.ordered_list(
        # The lambda function now correctly passes the dictionary 'item'
        rx.foreach(State.items, lambda item: todo_item(item)),
        list_style_type="none", # Remove default list bullets
        padding_left="0", # Remove default list indentation
        width="100%",
    )

# Improved form layout with horizontal arrangement for better alignment
def new_item() -> rx.Component:
    """Render the form to add a new item."""
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
                    State.priority_levels,
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
                align_self="flex-start", # Align with the top input
            ),
            width="100%",
            align_items="flex-start", # Align items at the top
            spacing="3",
        ),
        on_submit=State.add_item,
        reset_on_submit=True,
        width="100%",
        margin_bottom="4",
    )

# --- Main App Definition ---
def index() -> rx.Component:
    """The main page of the app."""
    return rx.container(
        rx.vstack(
            # App header with improved styling and spacing
            rx.box(
                rx.heading(
                    "Todo App", 
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
            new_item(),
            
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
            
            # Todo list with proper spacing - centered as a whole
            rx.center(
                rx.box(
                    todo_list(),
                    width="100%",
                    padding="0.5rem 0", # Add vertical padding
                    max_width="500px", # Fixed width for the todo list
                    border_radius="md",
                ),
                width="100%",
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

# Create app instance and add page.
app = rx.App()
app.add_page(index, title="Todo App with Priority")
# Changed from app.compile() to fix the AttributeError
