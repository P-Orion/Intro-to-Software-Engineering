"""Unit tests for the domain models in the refactored Todo application."""
import sys
import os
import unittest
from typing import Dict, Any

# Add the parent directory to the path so we can import the todo module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the domain models from the refactored todo app
from todo.refactored_todo import Priority, TodoItem

class TestPriorityEnum(unittest.TestCase):
    """Test cases for the Priority enum."""
    
    def test_priority_values(self):
        """Test that the Priority enum has the expected values."""
        self.assertEqual(Priority.LOW.value, "Low")
        self.assertEqual(Priority.MEDIUM.value, "Medium")
        self.assertEqual(Priority.HIGH.value, "High")
    
    def test_get_all_values(self):
        """Test that get_all_values returns all priority values as strings."""
        expected = ["Low", "Medium", "High"]
        self.assertEqual(Priority.get_all_values(), expected)
    
    def test_from_string_valid(self):
        """Test that from_string correctly converts valid strings to Priority enum values."""
        self.assertEqual(Priority.from_string("Low"), Priority.LOW)
        self.assertEqual(Priority.from_string("Medium"), Priority.MEDIUM)
        self.assertEqual(Priority.from_string("High"), Priority.HIGH)
    
    def test_from_string_invalid(self):
        """Test that from_string returns MEDIUM for invalid strings."""
        self.assertEqual(Priority.from_string("Invalid"), Priority.MEDIUM)
        self.assertEqual(Priority.from_string(""), Priority.MEDIUM)
        self.assertEqual(Priority.from_string(None), Priority.MEDIUM)


class TestTodoItem(unittest.TestCase):
    """Test cases for the TodoItem class."""
    
    def test_create_valid(self):
        """Test that create returns a TodoItem for valid inputs."""
        item = TodoItem.create("Test Item", "High")
        self.assertIsNotNone(item)
        self.assertEqual(item.text, "Test Item")
        self.assertEqual(item.priority, Priority.HIGH)
    
    def test_create_empty_text(self):
        """Test that create returns None for empty text."""
        self.assertIsNone(TodoItem.create("", "Medium"))
        self.assertIsNone(TodoItem.create("   ", "Medium"))
        self.assertIsNone(TodoItem.create(None, "Medium"))
    
    def test_create_strips_whitespace(self):
        """Test that create strips whitespace from text."""
        item = TodoItem.create("  Test Item  ", "Medium")
        self.assertEqual(item.text, "Test Item")
    
    def test_to_dict(self):
        """Test that to_dict correctly converts a TodoItem to a dictionary."""
        item = TodoItem("Test Item", Priority.MEDIUM)
        expected = {"text": "Test Item", "priority": "Medium"}
        self.assertEqual(item.to_dict(), expected)
    
    def test_from_dict_valid(self):
        """Test that from_dict correctly creates a TodoItem from a valid dictionary."""
        data = {"text": "Test Item", "priority": "High"}
        item = TodoItem.from_dict(data)
        self.assertEqual(item.text, "Test Item")
        self.assertEqual(item.priority, Priority.HIGH)
    
    def test_from_dict_missing_fields(self):
        """Test that from_dict handles dictionaries with missing fields."""
        # Missing priority
        data1 = {"text": "Test Item"}
        item1 = TodoItem.from_dict(data1)
        self.assertEqual(item1.text, "Test Item")
        self.assertEqual(item1.priority, Priority.MEDIUM)
        
        # Missing text
        data2 = {"priority": "High"}
        item2 = TodoItem.from_dict(data2)
        self.assertEqual(item2.text, "")
        self.assertEqual(item2.priority, Priority.HIGH)
        
        # Empty dictionary
        data3 = {}
        item3 = TodoItem.from_dict(data3)
        self.assertEqual(item3.text, "")
        self.assertEqual(item3.priority, Priority.MEDIUM)


if __name__ == "__main__":
    unittest.main()
