import datetime
from your_flask_app import db
from your_flask_app.models import AdmissionNumber


class AdmissionNumberGenerator:
    def generate_admission_number(self, department_code):
        # Get the current year
        current_year = datetime.datetime.now().year

        # Check if the department already has a student count in the database
        record = AdmissionNumber.query.filter_by(department_code=department_code).order_by(
            AdmissionNumber.id.desc()).first()

        if record:
            # Increment the student count
            student_count = record.student_count + 1
        else:
            # Initialize student count for the department
            student_count = 1

        # Generate the admission number
        admission_number = f"{current_year}-{department_code}-{student_count:03d}"

        # Save to database
        new_admission = AdmissionNumber(
            department_code=department_code,
            student_count=student_count,
            admission_number=admission_number
        )
        db.session.add(new_admission)
        db.session.commit()

        return admission_number


generator = AdmissionNumberGenerator()

# Generate admission numbers for different departments
admission_num_1 = generator.generate_admission_number("CSE")  # CSE for Computer Science
admission_num_2 = generator.generate_admission_number("EEE")  # EEE for Electrical Engineering

print(admission_num_1)  # e.g., 2024-CSE-001
print(admission_num_2)  # e.g., 2024-EEE-001