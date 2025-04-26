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

# CHANGED: todo_item now accepts a dictionary and displays priority.
def todo_item(item: Dict[str, str]) -> rx.Component:
    """Render a single todo item with its priority."""
    return rx.list_item(
        rx.hstack(
            rx.button(
                rx.icon(tag="check", size=20),
                on_click=lambda: State.finish_item(item), # Pass the whole item dict
                height="auto", # Adjust button height
                padding="0.25em", # Smaller padding
                variant="outline",
                color_scheme="green",
            ),
            # CHANGED: Display item text
            rx.text(item["text"], as_="span", margin_left="0.5em"),
            rx.spacer(), # Pushes priority to the right
            # ADDED: Display priority with some styling
            rx.badge(
                item["priority"],
                color_scheme="blue" if item["priority"] == "Medium" else ("red" if item["priority"] == "High" else "gray"),
                variant="solid",
                border_radius="full", # Make badge rounded
                padding_x="0.75em", # Horizontal padding
            ),
            align_items="center", # Vertically align items in the row
            width="100%", # Ensure hstack takes full width
        ),
        padding_y="0.25em", # Vertical padding for the list item
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

# CHANGED: new_item form now includes a priority selector.
def new_item() -> rx.Component:
    """Render the form to add a new item."""
    return rx.form(
        rx.hstack(
            rx.input(
                placeholder="Add a todo...",
                name="new_item", # Input field for item text
                flex_grow=1, # Allow input to take available space
            ),
            # ADDED: Dropdown selector for priority
            rx.select(
                State.priority_levels, # Options from state
                placeholder="Priority",
                name="priority", # Form field name for priority
                default_value="Medium", # Default selection
            ),
            rx.button(
                "Add",
                type="submit", # Submit the form on click
                color_scheme="blue",
             ),
            align_items="center", # Align items vertically
            spacing="3", # Spacing between elements
        ),
        # CHANGED: on_submit still calls State.add_item, which now handles the dictionary
        on_submit=State.add_item,
        reset_on_submit=True, # Clear form after submission
        width="100%", # Make form take full width
    )

# --- Main App Definition ---
def index() -> rx.Component:
    """The main page of the app."""
    return rx.container(
        rx.vstack(
            rx.heading("Todos", size="xl"), # Larger heading
            new_item(), # Form to add items
            rx.divider(border_color="gray.200"), # Visual separator
            todo_list(), # The list of items
            align_items="stretch", # Stretch items to fill container width
            spacing="5", # Spacing between vstack elements
            width="100%", # Ensure vstack takes full width
            max_width="600px", # Limit max width for better readability
            margin_top="2em", # Add some margin at the top
            padding="1em", # Padding inside the container
            border="1px solid #ddd", # Add a light border
            border_radius="lg", # Rounded corners
            box_shadow="md", # Add a subtle shadow
        ),
        center_content=True, # Center the main vstack container
    )

# Create app instance and add page.
app = rx.App()
app.add_page(index, title="Todo App with Priority")
app.compile()
