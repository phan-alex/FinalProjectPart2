
import csv
from operator import attrgetter

class Student:
    def __init__(self, student_id, last_name, first_name, major, disciplinary_action=None):
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.major = major
        self.disciplinary_action = disciplinary_action

    def __str__(self):
        return f"{self.student_id},{self.last_name},{self.first_name},{self.major},{self.disciplinary_action}"

class StudentRecordsManager:
    def __init__(self):
        self.students = {}
        self.gpas = {}
        self.graduation_dates = {}

    def load_data(self, students_file, gpa_file, graduation_file):
        self.load_students(students_file)
        self.load_gpas(gpa_file)
        self.load_graduation_dates(graduation_file)

    def load_students(self, students_file):
        with open(students_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                student_id, last_name, first_name, major, disciplinary_action = row
                self.students[student_id] = Student(student_id, last_name, first_name, major, disciplinary_action)

    def load_gpas(self, gpa_file):
        with open(gpa_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                student_id, gpa = row
                self.gpas[student_id] = float(gpa)

    def load_graduation_dates(self, graduation_file):
        with open(graduation_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                student_id, graduation_date = row
                self.graduation_dates[student_id] = graduation_date

    def generate_reports(self):
        self.generate_full_roster()
        self.generate_major_reports()
        self.generate_scholarship_candidates()
        self.generate_disciplined_students()

    def generate_full_roster(self):
        full_roster = list(self.students.values())
        full_roster.sort(key=attrgetter('last_name'))
        self.write_csv(r'D:\Google Downloads\FullRoster-1.csv', full_roster, print_to_console=True)

    def generate_major_reports(self):
        majors = set(student.major for student in self.students.values())
        for major in majors:
            major_students = [student for student in self.students.values() if student.major == major]
            major_students.sort(key=attrgetter('student_id'))
            filename = fr"{major.replace(' ', '')}Students.csv"
            self.write_csv(filename, major_students, print_to_console=True)

    def generate_scholarship_candidates(self):
        eligible_students = [student for student in self.students.values() if
                             student.student_id in self.gpas and
                             self.gpas[student.student_id] > 3.8 and
                             student.student_id not in self.graduation_dates and
                             not student.disciplinary_action]
        eligible_students.sort(key=lambda x: self.gpas[x.student_id], reverse=True)
        self.write_csv(r'D:\Google Downloads\ScholarshipCandidates-1.csv', eligible_students, print_to_console=True)

    def generate_disciplined_students(self):
        disciplined_students = [student for student in self.students.values() if student.disciplinary_action]
        disciplined_students.sort(key=self.get_graduation_date)
        self.write_csv(r'D:\Google Downloads\DisciplinedStudents-1.csv', disciplined_students, print_to_console=True)

    @staticmethod
    def write_csv(filename, data, print_to_console=False):
        header = ["Student ID", "Last Name", "First Name", "Major", "Disciplinary Action"]

        if print_to_console:
            print(f"Printing data for {filename}:")
            print(",".join(header))  # Print header

            for student in data:
                print(",".join(str(getattr(student, attr, 'None')) for attr in header))
        else:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                for student in data:
                    writer.writerow([getattr(student, attr, 'None') for attr in header])

    def get_graduation_date(self, student):
        return self.graduation_dates.get(student.student_id, '')

    def interactive_query(self):
        while True:
            input_str = input("Enter a major and GPA (or 'q' to quit): ").strip().lower()

            if input_str == 'q':
                break

            major, _, gpa_str = input_str.partition(' ')
            try:
                gpa = float(gpa_str)
            except ValueError:
                print("Invalid GPA. Please enter a valid major and GPA.")
                continue

            if major not in [student.major for student in self.students.values()]:
                print("No such student.")
                continue

            eligible_students = [student for student in self.students.values() if
                                 student.major == major and
                                 not student.disciplinary_action and
                                 student.student_id not in self.graduation_dates and
                                 abs(self.gpas.get(student.student_id, 0) - gpa) <= 0.1]

            if eligible_students:
                print("\nYour student(s):")
                for student in eligible_students:
                    print(f"Student ID: {student.student_id}, First Name: {student.first_name}, Last Name: {student.last_name}, GPA: {self.gpas.get(student.student_id, 0)}")
            else:
                print("\nNo matching students found within 0.1 of the requested GPA.")

                additional_suggestions = [student for student in self.students.values() if
                                          student.major == major and
                                          not student.disciplinary_action and
                                          student.student_id not in self.graduation_dates and
                                          abs(self.gpas.get(student.student_id, 0) - gpa) <= 0.25]

                if additional_suggestions:
                    print("\nYou may also consider:")
                    for student in additional_suggestions:
                        print(f"Student ID: {student.student_id}, First Name: {student.first_name}, Last Name: {student.last_name}, GPA: {self.gpas.get(student.student_id, 0)}")
                else:
                    closest_student = min(self.students.values(), key=lambda student: abs(self.gpas.get(student.student_id, 0) - gpa))
                    print("\nNo students found within 0.1 or 0.25 of the requested GPA. Closest match:")
                    print(f"Student ID: {closest_student.student_id}, First Name: {closest_student.first_name}, Last Name: {closest_student.last_name}, GPA: {self.gpas.get(closest_student.student_id, 0)}")

# Example usage
if __name__ == "__main__":
    manager = StudentRecordsManager()
    manager.load_data(r'D:\Google Downloads\StudentsMajorsList-3.csv', r'D:\Google Downloads\GPAList-1.csv', r'D:\Google Downloads\GraduationDatesList-1.csv')
    manager.generate_reports()
    manager.interactive_query()
