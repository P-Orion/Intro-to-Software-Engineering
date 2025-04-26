"""Unit tests for the UI components in the refactored Todo application."""
import sys
import os
import unittest
from typing import Dict, List, Any
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the todo module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the UI components from the refactored todo app
from todo.refactored_todo import UIComponentLibrary, Priority

class TestUIComponentLibrary(unittest.TestCase):
    """Test cases for the UIComponentLibrary class."""
    
    def test_get_priority_color(self):
        """Test that get_priority_color returns the correct color for each priority."""
        self.assertEqual(UIComponentLibrary.get_priority_color("High"), "red")
        self.assertEqual(UIComponentLibrary.get_priority_color("Medium"), "blue")
        self.assertEqual(UIComponentLibrary.get_priority_color("Low"), "gray")
        # Test with invalid priority (should default to some color)
        self.assertEqual(UIComponentLibrary.get_priority_color("Invalid"), "gray")
    
    def test_create_priority_badge(self):
        """Test that create_priority_badge creates a badge with the correct properties."""
        # Test with High priority
        high_badge = UIComponentLibrary.create_priority_badge("High")
        self.assertEqual(high_badge.children, "High")
        self.assertEqual(high_badge.color_scheme, "red")
        self.assertEqual(high_badge.variant, "solid")
        self.assertEqual(high_badge.border_radius, "full")
        self.assertEqual(high_badge.padding_x, "0.75em")
        
        # Test with Medium priority
        medium_badge = UIComponentLibrary.create_priority_badge("Medium")
        self.assertEqual(medium_badge.children, "Medium")
        self.assertEqual(medium_badge.color_scheme, "blue")
        
        # Test with Low priority
        low_badge = UIComponentLibrary.create_priority_badge("Low")
        self.assertEqual(low_badge.children, "Low")
        self.assertEqual(low_badge.color_scheme, "gray")
    
    def test_create_todo_item_component(self):
        """Test that create_todo_item_component creates a component with the correct structure."""
        # Create a mock callback
        mock_callback = MagicMock()
        
        # Create a test item
        item = {"text": "Test Item", "priority": "High"}
        
        # Create the component
        component = UIComponentLibrary.create_todo_item_component(item, mock_callback)
        
        # Check the component structure
        self.assertEqual(component.tag, "li")  # list_item creates an li element
        
        # Check that the component contains the item text
        hstack = component.children
        self.assertEqual(hstack.tag, "div")  # hstack creates a div
        
        # Find the text component
        text_component = None
        for child in hstack.children:
            if hasattr(child, 'children') and child.children == "Test Item":
                text_component = child
                break
        
        self.assertIsNotNone(text_component, "Text component not found")
        self.assertEqual(text_component.children, "Test Item")
        self.assertEqual(text_component.as_, "span")
    
    def test_create_todo_list(self):
        """Test that create_todo_list creates a list with the correct structure."""
        # Create a mock callback
        mock_callback = MagicMock()
        
        # Create test items
        items = [
            {"text": "Item 1", "priority": "High"},
            {"text": "Item 2", "priority": "Medium"}
        ]
        
        # Create the component
        component = UIComponentLibrary.create_todo_list(items, mock_callback)
        
        # Check the component structure
        self.assertEqual(component.tag, "ol")  # ordered_list creates an ol element
        self.assertEqual(component.list_style_type, "none")
        self.assertEqual(component.padding_left, "0")
        self.assertEqual(component.width, "100%")
    
    def test_create_new_item_form(self):
        """Test that create_new_item_form creates a form with the correct structure."""
        # Create a mock callback
        mock_callback = MagicMock()
        
        # Create the component
        component = UIComponentLibrary.create_new_item_form(mock_callback, Priority.get_all_values())
        
        # Check the component structure
        self.assertEqual(component.tag, "form")
        self.assertEqual(component.on_submit, mock_callback)
        self.assertEqual(component.reset_on_submit, True)
        self.assertEqual(component.width, "100%")
        
        # Check that the form contains the expected elements
        hstack = component.children
        self.assertEqual(hstack.tag, "div")  # hstack creates a div
        
        # Check for input field
        input_field = None
        select_field = None
        button = None
        
        for child in hstack.children:
            if hasattr(child, 'tag'):
                if child.tag == "input":
                    input_field = child
                elif child.tag == "select":
                    select_field = child
                elif child.tag == "button":
                    button = child
        
        self.assertIsNotNone(input_field, "Input field not found")
        self.assertEqual(input_field.placeholder, "Add a todo...")
        self.assertEqual(input_field.name, "new_item")
        
        self.assertIsNotNone(select_field, "Select field not found")
        self.assertEqual(select_field.placeholder, "Priority")
        self.assertEqual(select_field.name, "priority")
        self.assertEqual(select_field.default_value, "Medium")
        
        self.assertIsNotNone(button, "Button not found")
        self.assertEqual(button.children, "Add")
        self.assertEqual(button.type, "submit")
        self.assertEqual(button.color_scheme, "blue")


if __name__ == "__main__":
    unittest.main()
