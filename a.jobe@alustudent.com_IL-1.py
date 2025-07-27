class Assignment:
    """Class to represent an individual assignment"""
    def __init__(self, name, category, grade, weight):
        self.name = name
        self.category = category.upper()  # FA or SA
        self.grade = grade  # Grade out of 100
        self.weight = weight  # Weight as percentage
        self.weighted_grade = (grade * weight) / 100
    
    def __str__(self):
        return f"{self.name}: {self.grade}% (Weight: {self.weight}%) = {self.weighted_grade:.2f}"

class GradeCalculator:
    """Main class for grade calculation and management"""
    def __init__(self):
        self.assignments = []
        self.formative_total_weight = 0
        self.summative_total_weight = 0
        self.max_formative_weight = 60
        self.max_summative_weight = 40
    
    def validate_grade(self, grade):
        """Validate grade is between 0 and 100"""
        try:
            grade = float(grade)
            if 0 <= grade <= 100:
                return grade
            else:
                raise ValueError("Grade must be between 0 and 100")
        except ValueError:
            raise ValueError("Grade must be a valid number")
    
    def validate_weight(self, weight, category):
        """Validate weight limits for each category"""
        try:
            weight = float(weight)
            if weight <= 0:
                raise ValueError("Weight must be greater than 0")
            
            current_weight = self.formative_total_weight if category.upper() == "FA" else self.summative_total_weight
            max_weight = self.max_formative_weight if category.upper() == "FA" else self.max_summative_weight
            
            if current_weight + weight > max_weight:
                raise ValueError(f"Total weight for {category} category would exceed {max_weight}%")
            
            return weight
        except ValueError as e:
            if "could not convert" in str(e):
                raise ValueError("Weight must be a valid number")
            raise e
    
    def validate_category(self, category):
        """Validate category is either FA or SA"""
        category = category.upper().strip()
        if category not in ["FA", "SA", "FORMATIVE", "SUMMATIVE"]:
            raise ValueError("Category must be FA (Formative) or SA (Summative)")
        
        # Convert full names to abbreviations
        if category == "FORMATIVE":
            category = "FA"
        elif category == "SUMMATIVE":
            category = "SA"
        
        return category
    
    def add_assignment(self, name, category, grade, weight):
        """Add a new assignment with validation"""
        # Validate inputs
        category = self.validate_category(category)
        grade = self.validate_grade(grade)
        weight = self.validate_weight(weight, category)
        
        # Create assignment
        assignment = Assignment(name, category, grade, weight)
        self.assignments.append(assignment)
        
        # Update weight totals
        if category == "FA":
            self.formative_total_weight += weight
        else:
            self.summative_total_weight += weight
        
        print(f"Assignment '{name}' added successfully!")
    
    def get_category_grades(self):
        """Calculate total grades for each category"""
        formative_total = sum(assignment.weighted_grade for assignment in self.assignments if assignment.category == "FA")
        summative_total = sum(assignment.weighted_grade for assignment in self.assignments if assignment.category == "SA")
        
        return formative_total, summative_total
    
    def calculate_gpa(self):
        """Calculate GPA out of 5 based on weighted grades"""
        formative_total, summative_total = self.get_category_grades()
        total_grade = formative_total + summative_total
        
        # Convert to GPA scale (assuming 100% = 5.0 GPA)
        gpa = (total_grade / 100) * 5
        return gpa
    
    def calculate_category_averages(self):
        """Calculate average grades for each category"""
        formative_assignments = [a for a in self.assignments if a.category == "FA"]
        summative_assignments = [a for a in self.assignments if a.category == "SA"]
        
        formative_avg = sum(a.grade for a in formative_assignments) / len(formative_assignments) if formative_assignments else 0
        summative_avg = sum(a.grade for a in summative_assignments) / len(summative_assignments) if summative_assignments else 0
        
        return formative_avg, summative_avg
    
    def determine_pass_fail(self):
        """Determine if student passes or fails based on category averages"""
        formative_total, summative_total = self.get_category_grades()
        formative_avg, summative_avg = self.calculate_category_averages()
        
        # Check if student scores at or above average in both categories
        formative_assignments = [a for a in self.assignments if a.category == "FA"]
        summative_assignments = [a for a in self.assignments if a.category == "SA"]
        
        # Calculate weighted averages for comparison
        formative_weighted_avg = formative_total / self.formative_total_weight * 100 if self.formative_total_weight > 0 else 0
        summative_weighted_avg = summative_total / self.summative_total_weight * 100 if self.summative_total_weight > 0 else 0
        
        if formative_weighted_avg >= formative_avg and summative_weighted_avg >= summative_avg:
            return "PASS"
        else:
            return "FAIL AND REPEAT"
    
    def display_results(self):
        """Display comprehensive results"""
        print("\n" + "="*60)
        print("GRADE CALCULATOR RESULTS")
        print("="*60)
        
        print("\nASSIGNMENTS BREAKDOWN:")
        print("-" * 40)
        for assignment in self.assignments:
            print(f"{assignment}")
        
        formative_total, summative_total = self.get_category_grades()
        
        print(f"\nCATEGORY TOTALS:")
        print("-" * 20)
        print(f"Formative (FA) Total: {formative_total:.2f}/60")
        print(f"Summative (SA) Total: {summative_total:.2f}/40")
        
        gpa = self.calculate_gpa()
        print(f"\nGPA: {gpa:.3f}/5.0")
        
        pass_fail = self.determine_pass_fail()
        print(f"\nFINAL RESULT: {pass_fail}")
        
        print("="*60)

def collect_assignment_input():
    """Collect assignment details from user input"""
    print("\nEnter assignment details:")
    name = input("Assignment name: ").strip()
    
    while True:
        try:
            category = input("Category (FA/Formative or SA/Summative): ").strip()
            category = calculator.validate_category(category)
            break
        except ValueError as e:
            print(f"Error: {e}")
    
    while True:
        try:
            grade = input("Grade obtained (0-100): ").strip()
            grade = calculator.validate_grade(grade)
            break
        except ValueError as e:
            print(f"Error: {e}")
    
    while True:
        try:
            weight = input("Weight percentage: ").strip()
            weight = calculator.validate_weight(weight, category)
            break
        except ValueError as e:
            print(f"Error: {e}")
    
    return name, category, grade, weight

def main():
    """Main application function"""
    global calculator
    calculator = GradeCalculator()
    
    print("AFRICAN LEADERSHIP UNIVERSITY")
    print("GRADE GENERATOR CALCULATOR")
    print("="*50)
    
    while True:
        print("\nOptions:")
        print("1. Add assignment")
        print("2. View results")
        print("3. Load test transcript")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            try:
                name, category, grade, weight = collect_assignment_input()
                calculator.add_assignment(name, category, grade, weight)
            except ValueError as e:
                print(f"Error adding assignment: {e}")
        
        elif choice == "2":
            if not calculator.assignments:
                print("No assignments added yet!")
            else:
                calculator.display_results()
        
        elif choice == "3":
            load_test_transcript()
        
        elif choice == "4":
            print("Thank you for using Grade Generator Calculator!")
            break
        
        else:
            print("Invalid option. Please select 1-4.")

def load_test_transcript():
    """Load the provided transcript data for testing"""
    global calculator
    calculator = GradeCalculator()  # Reset calculator
    
    # Test data from provided transcript
    test_assignments = [
        ("Group Coding Lab", "FA", 19, 30),
        ("Discussion Forum", "FA", 56, 10),
        ("General Quiz", "FA", 67, 20),
        ("Pre-Summative", "SA", 45, 15),
        ("Individual Lab", "SA", 81, 25)
    ]
    
    print("\nLoading test transcript...")
    for name, category, grade, weight in test_assignments:
        calculator.add_assignment(name, category, grade, weight)
    
    print("Test transcript loaded successfully!")
    calculator.display_results()

if __name__ == "__main__":
    main()