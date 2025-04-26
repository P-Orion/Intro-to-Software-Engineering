# Manual Test Cases for Todo Application

This document outlines the manual test cases for the Todo application. These test cases focus on UI interactions and user workflows that are difficult to automate.

## Test Case Template

```
Test Case ID: TC-[number]
Test Case Name: [descriptive name]
Objective: [what is being tested]
Preconditions: [required state before test]
Test Steps:
1. [step 1]
2. [step 2]
...
Expected Result: [what should happen]
Actual Result: [what actually happened]
Status: [Pass/Fail]
Notes: [any observations]
```

## Test Cases

### Test Case ID: TC-001
**Test Case Name:** Add Todo Item with High Priority  
**Objective:** Verify that a new todo item can be added with High priority  
**Preconditions:** Todo application is running  
**Test Steps:**
1. Enter "Complete assignment" in the text input field
2. Select "High" from the priority dropdown
3. Click the "Add" button
**Expected Result:** 
- A new todo item with text "Complete assignment" and High priority (red badge) appears at the top of the list
- The input field is cleared after submission
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-002
**Test Case Name:** Add Todo Item with Empty Text  
**Objective:** Verify that empty todo items cannot be added  
**Preconditions:** Todo application is running  
**Test Steps:**
1. Leave the text input field empty
2. Select any priority from the dropdown
3. Click the "Add" button
**Expected Result:** No new todo item is added to the list  
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-003
**Test Case Name:** Complete Todo Item  
**Objective:** Verify that clicking the check button removes the todo item  
**Preconditions:** 
- Todo application is running
- At least one todo item exists in the list
**Test Steps:**
1. Click the check button next to any todo item
**Expected Result:** The selected todo item is removed from the list  
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-004
**Test Case Name:** Priority Sorting Order  
**Objective:** Verify that todo items are sorted by priority (High > Medium > Low)  
**Preconditions:** Todo application is running with no items  
**Test Steps:**
1. Add a todo item with Low priority
2. Add a todo item with High priority
3. Add a todo item with Medium priority
**Expected Result:** 
- The items should be displayed in the order: High priority item, Medium priority item, Low priority item
- The High priority item should have a red badge
- The Medium priority item should have a blue badge
- The Low priority item should have a gray badge
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-005
**Test Case Name:** Default Priority Selection  
**Objective:** Verify that Medium is the default priority when adding a new item  
**Preconditions:** Todo application is running  
**Test Steps:**
1. Enter "Test default priority" in the text input field
2. Without selecting any priority, click the "Add" button
**Expected Result:** 
- A new todo item with text "Test default priority" and Medium priority (blue badge) is added to the list
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-006
**Test Case Name:** Long Text Handling  
**Objective:** Verify that the application handles very long todo item text properly  
**Preconditions:** Todo application is running  
**Test Steps:**
1. Enter a very long text (over 100 characters) in the text input field
2. Select any priority
3. Click the "Add" button
**Expected Result:** 
- The todo item is added with the full text
- The text is displayed properly without breaking the layout
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-007
**Test Case Name:** Special Characters Handling  
**Objective:** Verify that the application handles special characters in todo item text  
**Preconditions:** Todo application is running  
**Test Steps:**
1. Enter text with special characters (e.g., "Test @#$%^&*()_+<>?") in the text input field
2. Select any priority
3. Click the "Add" button
**Expected Result:** 
- The todo item is added with the exact text including all special characters
- The text is displayed properly
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-008
**Test Case Name:** UI Responsiveness  
**Objective:** Verify that the UI is responsive and adapts to different screen sizes  
**Preconditions:** Todo application is running  
**Test Steps:**
1. Resize the browser window to different sizes (desktop, tablet, mobile)
2. Observe the layout and components
**Expected Result:** 
- The UI should adapt to different screen sizes
- All components should remain usable and visible
- The todo list and form should adjust their width appropriately
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-009
**Test Case Name:** Initial State Loading  
**Objective:** Verify that the application loads with the correct initial state  
**Preconditions:** Fresh load of the Todo application  
**Test Steps:**
1. Open the Todo application in a browser
2. Observe the initial todo items
**Expected Result:** 
- The application should load with three default todo items:
  - "Write Code" with Medium priority
  - "Sleep" with High priority
  - "Have Fun" with Low priority
- The items should be sorted by priority (High > Medium > Low)
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

### Test Case ID: TC-010
**Test Case Name:** Form Reset After Submission  
**Objective:** Verify that the form resets after a successful submission  
**Preconditions:** Todo application is running  
**Test Steps:**
1. Enter "Test item" in the text input field
2. Select "High" from the priority dropdown
3. Click the "Add" button
4. Observe the form state after submission
**Expected Result:** 
- The text input field should be cleared
- The priority dropdown should reset to its default value (Medium)
**Actual Result:** [To be filled during testing]  
**Status:** [To be filled during testing]  
**Notes:** [To be filled during testing]  

## Test Results Summary

| Test Case ID | Test Case Name | Status |
|--------------|---------------|--------|
| TC-001 | Add Todo Item with High Priority | [To be filled] |
| TC-002 | Add Todo Item with Empty Text | [To be filled] |
| TC-003 | Complete Todo Item | [To be filled] |
| TC-004 | Priority Sorting Order | [To be filled] |
| TC-005 | Default Priority Selection | [To be filled] |
| TC-006 | Long Text Handling | [To be filled] |
| TC-007 | Special Characters Handling | [To be filled] |
| TC-008 | UI Responsiveness | [To be filled] |
| TC-009 | Initial State Loading | [To be filled] |
| TC-010 | Form Reset After Submission | [To be filled] |
