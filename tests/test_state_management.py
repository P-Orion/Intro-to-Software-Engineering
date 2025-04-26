"""Unit tests for the state management in the refactored Todo application."""
import sys
import os
import unittest
from typing import Dict, List, Any
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the todo module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the state management from the refactored todo app
from todo.refactored_todo import TodoStateManager, TodoItem, Priority

class TestTodoStateManager(unittest.TestCase):
    """Test cases for the TodoStateManager class."""
    
    def setUp(self):
        """Set up a fresh TodoStateManager instance for each test."""
        self.state_manager = TodoStateManager()
        # Clear the default items to start with a clean state
        self.state_manager.items = []
    
    def test_initial_state(self):
        """Test that the initial state has the expected default items."""
        # Create a new instance to test the default state
        state = TodoStateManager()
        self.assertEqual(len(state.items), 3)
        self.assertEqual(state.items[0]["text"], "Write Code")
        self.assertEqual(state.items[0]["priority"], "Medium")
        self.assertEqual(state.items[1]["text"], "Sleep")
        self.assertEqual(state.items[1]["priority"], "High")
        self.assertEqual(state.items[2]["text"], "Have Fun")
        self.assertEqual(state.items[2]["priority"], "Low")
    
    def test_todo_items_property(self):
        """Test that the todo_items property correctly converts dictionaries to TodoItem objects."""
        # Add some test items
        self.state_manager.items = [
            {"text": "Test 1", "priority": "High"},
            {"text": "Test 2", "priority": "Medium"}
        ]
        
        todo_items = self.state_manager.todo_items
        self.assertEqual(len(todo_items), 2)
        self.assertIsInstance(todo_items[0], TodoItem)
        self.assertEqual(todo_items[0].text, "Test 1")
        self.assertEqual(todo_items[0].priority, Priority.HIGH)
        self.assertEqual(todo_items[1].text, "Test 2")
        self.assertEqual(todo_items[1].priority, Priority.MEDIUM)
    
    def test_add_todo_item_valid(self):
        """Test adding a valid todo item."""
        form_data = {"new_item": "New Task", "priority": "High"}
        self.state_manager.add_todo_item(form_data)
        
        self.assertEqual(len(self.state_manager.items), 1)
        self.assertEqual(self.state_manager.items[0]["text"], "New Task")
        self.assertEqual(self.state_manager.items[0]["priority"], "High")
    
    def test_add_todo_item_empty(self):
        """Test that adding an empty todo item does nothing."""
        form_data = {"new_item": "", "priority": "Medium"}
        self.state_manager.add_todo_item(form_data)
        self.assertEqual(len(self.state_manager.items), 0)
        
        form_data = {"new_item": "   ", "priority": "Medium"}
        self.state_manager.add_todo_item(form_data)
        self.assertEqual(len(self.state_manager.items), 0)
    
    def test_add_todo_item_missing_fields(self):
        """Test adding a todo item with missing fields."""
        # Missing new_item
        form_data = {"priority": "High"}
        self.state_manager.add_todo_item(form_data)
        self.assertEqual(len(self.state_manager.items), 0)
        
        # Missing priority (should use default)
        form_data = {"new_item": "New Task"}
        self.state_manager.add_todo_item(form_data)
        self.assertEqual(len(self.state_manager.items), 1)
        self.assertEqual(self.state_manager.items[0]["text"], "New Task")
        self.assertEqual(self.state_manager.items[0]["priority"], "Medium")
    
    def test_complete_todo_item(self):
        """Test completing (removing) a todo item."""
        # Add some test items
        item1 = {"text": "Test 1", "priority": "High"}
        item2 = {"text": "Test 2", "priority": "Medium"}
        self.state_manager.items = [item1, item2]
        
        # Complete the first item
        self.state_manager.complete_todo_item(item1)
        self.assertEqual(len(self.state_manager.items), 1)
        self.assertEqual(self.state_manager.items[0], item2)
    
    def test_complete_nonexistent_item(self):
        """Test completing a non-existent item."""
        # Add a test item
        item = {"text": "Test", "priority": "Medium"}
        self.state_manager.items = [item]
        
        # Try to complete a different item
        non_existent_item = {"text": "Non-existent", "priority": "High"}
        self.state_manager.complete_todo_item(non_existent_item)
        
        # The original item should still be there
        self.assertEqual(len(self.state_manager.items), 1)
        self.assertEqual(self.state_manager.items[0], item)
    
    def test_sort_items_by_priority(self):
        """Test that items are sorted correctly by priority."""
        # Add items in mixed priority order
        self.state_manager.items = [
            {"text": "Low Priority", "priority": "Low"},
            {"text": "High Priority", "priority": "High"},
            {"text": "Medium Priority", "priority": "Medium"}
        ]
        
        # Sort the items
        self.state_manager._sort_items_by_priority()
        
        # Check that they're sorted High > Medium > Low
        self.assertEqual(self.state_manager.items[0]["priority"], "High")
        self.assertEqual(self.state_manager.items[1]["priority"], "Medium")
        self.assertEqual(self.state_manager.items[2]["priority"], "Low")
    
    def test_sort_items_with_invalid_priority(self):
        """Test sorting with items that have invalid priority values."""
        # Add items with some invalid priorities
        self.state_manager.items = [
            {"text": "Invalid Priority", "priority": "Invalid"},
            {"text": "High Priority", "priority": "High"},
            {"text": "No Priority", "text": "Test"}  # Missing priority key
        ]
        
        # Sort the items
        self.state_manager._sort_items_by_priority()
        
        # Check that invalid priorities default to Medium in sorting
        self.assertEqual(self.state_manager.items[0]["priority"], "High")
        # The other two should be treated as Medium priority
        self.assertIn(self.state_manager.items[1]["text"], ["Invalid Priority", "No Priority"])
        self.assertIn(self.state_manager.items[2]["text"], ["Invalid Priority", "No Priority"])
    
    def test_add_todo_item_calls_sort(self):
        """Test that adding a todo item calls the sort method."""
        # Mock the _sort_items_by_priority method
        self.state_manager._sort_items_by_priority = MagicMock()
        
        # Add a valid item
        form_data = {"new_item": "New Task", "priority": "High"}
        self.state_manager.add_todo_item(form_data)
        
        # Check that _sort_items_by_priority was called
        self.state_manager._sort_items_by_priority.assert_called_once()


if __name__ == "__main__":
    unittest.main()
