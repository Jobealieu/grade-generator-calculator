import importlib.util
import sys
import os

def test_transcript():
    """Test the calculator with provided transcript data"""
    
    # Load the GradeCalculator class from the main file
    filename = "a.jobe@alustudent.com_IL-1.py"  # Replace with your actual filename
    
    try:
        spec = importlib.util.spec_from_file_location("grade_calculator", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        GradeCalculator = module.GradeCalculator
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        print("Make sure the main file exists in the same directory.")
        return
    
    calculator = GradeCalculator()
    
    # Test data from transcript
    test_data = [
        ("Group Coding Lab", "FA", 19, 30),
        ("Discussion Forum", "FA", 56, 10),
        ("General Quiz", "FA", 67, 20),
        ("Pre-Summative", "SA", 45, 15),
        ("Individual Lab", "SA", 81, 25)
    ]
    
    print("Testing with provided transcript data:")
    print("="*50)
    
    for name, category, grade, weight in test_data:
        calculator.add_assignment(name, category, grade, weight)
    
    calculator.display_results()
    
    # Verify calculations
    formative_total, summative_total = calculator.get_category_grades()
    gpa = calculator.calculate_gpa()
    
    print("\nVERIFICATION:")
    print(f"Expected Formative Total: 24.7")
    print(f"Calculated Formative Total: {formative_total:.1f}")
    print(f"Expected Summative Total: 27.0")
    print(f"Calculated Summative Total: {summative_total:.1f}")
    print(f"Expected GPA: 2.585")
    print(f"Calculated GPA: {gpa:.3f}")

if __name__ == "__main__":
    test_transcript()