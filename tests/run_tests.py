"""Test runner script for the Todo application tests."""
import sys
import os
import unittest
import coverage

# Add the parent directory to the path so we can import the todo module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests_with_coverage():
    """Run all tests and generate a coverage report."""
    # Start coverage measurement
    cov = coverage.Coverage(
        source=["todo.refactored_todo"],
        omit=["*/__pycache__/*", "*/tests/*"]
    )
    cov.start()
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(test_dir)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage measurement and generate report
    cov.stop()
    cov.save()
    
    print("\nCoverage Report:")
    cov.report()
    
    # Generate HTML report
    cov.html_report(directory=os.path.join(test_dir, "coverage_html"))
    print(f"HTML coverage report generated in {os.path.join(test_dir, 'coverage_html')}")
    
    return result

if __name__ == "__main__":
    result = run_tests_with_coverage()
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())
