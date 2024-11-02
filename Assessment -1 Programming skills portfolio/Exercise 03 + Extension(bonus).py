import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk


class Student:
    def __init__(self, student_id, name, course_marks, exam_mark):
        # Initializing the main object with student ID,  Student name, course marks, exam mark  calculate grade
        self.student_id = student_id
        self.name = name
        self.course_marks = course_marks
        self.exam_mark = exam_mark
        self.total_coursework_mark = sum(course_marks)
        self.overall_percentage = (self.total_coursework_mark + exam_mark) / 160 * 100
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        # getting grade with the help of percentage
        if self.overall_percentage >= 70:
            return 'A'
        elif self.overall_percentage >= 60:
            return 'B'
        elif self.overall_percentage >= 50:
            return 'C'
        elif self.overall_percentage >= 40:
            return 'D'
        else:
            return 'F'


class StudentRecordsApp:
    def __init__(self, root):
        # main  window
        self.root = root
        self.root.title("Student Manager")

        # making window  icon
        icon_image = Image.open("icon.ico") # uploading image as icon
        self.root.iconphoto(False, ImageTk.PhotoImage(icon_image))

        # background window image
        bg_image = Image.open("background.png")  # uploading image for background
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # loading text from a file to get student information
        self.students = []
        self.load_data("studentMarks.txt")

        # displaying main image
        title_image = Image.open("title.png")  # opening image for a title
        self.title_photo = ImageTk.PhotoImage(title_image)
        self.title_image_label = tk.Label(root, image=self.title_photo, bg="#f0f0f0")
        self.title_image_label.pack(pady=(10, 0))

        # displaying title
        title_label = tk.Label(root, text="Student Manager", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title_label.pack()

        # code for buttons that display options for user to choose
        button_font = ("Helvetica", 12)
        tk.Button(root, text="View All Student Records", font=button_font, width=30,
                  command=self.all_records).pack(pady=5)
        tk.Button(root, text="View Individual Student Record", font=button_font, width=30,
                  command=self.view_individual_record).pack(pady=5)
        tk.Button(root, text="Show Student with Highest Total Score", font=button_font, width=30,
                  command=self.show_highest_score).pack(pady=5)
        tk.Button(root, text="Show Student with Lowest Total Score", font=button_font, width=30,
                  command=self.show_lowest_score).pack(pady=5)
        tk.Button(root, text="Sort Student Records", font=button_font, width=30,
                  command=self.sort_records).pack(pady=5)
        tk.Button(root, text="Add Student Record", font=button_font, width=30,
                  command=self.add_record).pack(pady=5)
        tk.Button(root, text="Delete Student Record", font=button_font, width=30,
                  command=self.delete_record).pack(pady=5)
        tk.Button(root, text="Update Student Record", font=button_font, width=30,
                  command=self.update_record).pack(pady=5)

        # Creating a frame for the Text widget and Scrollbar
        text_frame = tk.Frame(root)
        text_frame.pack(pady=10, padx=10, fill="both", expand=True)

        #  widget for displaying results
        self.result_text = tk.Text(text_frame, wrap="word", font=("Helvetica", 10), height=20, width=60,
                                   state="disabled")
        self.result_text.pack(side="left", fill="both", expand=True)

        # Scrollbar added so user can scroll and view all information
        scrollbar = tk.Scrollbar(text_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def load_data(self, filename):
        # Loading data from file
        try:
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    student_id = int(data[0])
                    name = data[1]
                    course_marks = list(map(int, data[2:5]))
                    exam_mark = int(data[5])
                    self.students.append(Student(student_id, name, course_marks, exam_mark))
        except FileNotFoundError:
            self.display_message(f"File '{filename}' not found.\n")

    def all_records(self):
        # records of all students to be displayed
        total_percentage = 0
        display_text = ""

        for student in self.students:
            display_text += self.format_info(student) + "\n\n"
            total_percentage += student.overall_percentage

        # In the showing total strength and percentage of class
        class_average = total_percentage / len(self.students) if self.students else 0
        display_text += f"Total Students: {len(self.students)}\n"
        display_text += f"Class Average Percentage: {class_average:.2f}%"

        self.display_message(display_text)

    def view_individual_record(self):
        # in order to display a records individually by just entering the name
        name = simpledialog.askstring("Student Name", "Enter the student's name:")

        if name:
            for student in self.students:
                if student.name.lower() == name.lower():
                    display_text = self.format_info(student)
                    self.display_message(display_text)
                    return
            self.display_message(f"Student '{name}' not found.\n")

    def show_highest_score(self):
        #  record of the student with the highest score to be displayed
        if not self.students:
            self.display_message("No student data available.\n")
            return

        highest_student = max(self.students, key=lambda s: s.total_coursework_mark + s.exam_mark)
        display_text = self.format_info(highest_student)
        self.display_message(display_text)

    def show_lowest_score(self):
        # record of the student with the lowest score
        if not self.students:
            self.display_message("No student data available.\n")
            return

        lowest_student = min(self.students, key=lambda s: s.total_coursework_mark + s.exam_mark)
        display_text = self.format_info(lowest_student)
        self.display_message(display_text)

    def format_info(self, student):
        # the student's information for display being formatted
        return (
            f"Name: {student.name}\n"
            f"Student ID: {student.student_id}\n"
            f"Total Coursework Mark: {student.total_coursework_mark}/60\n"
            f"Exam Mark: {student.exam_mark}/100\n"
            f"Overall Percentage: {student.overall_percentage:.2f}%\n"
            f"Grade: {student.grade}"
        )

    def display_message(self, message):
        # user cannot edit directly in the list
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)  # Clear previous content
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")  # Disable editing

    def sort_records(self):
        # in order to sort the list
        order = simpledialog.askstring("Sort Order", "Enter 'asc' for ascending or 'desc' for descending:")
        if order not in ['asc', 'desc']:
            self.display_message("Invalid order. Please enter 'asc' or 'desc'.")
            return

        # Sorting based on total score
        reverse = order == 'desc'
        self.students.sort(key=lambda s: s.total_coursework_mark + s.exam_mark, reverse=reverse)
        self.all_records()

    def add_record(self):
        # allowing user to add new student in the list
        try:
            student_id = int(simpledialog.askstring("Student ID", "Enter Student ID:"))
            name = simpledialog.askstring("Name", "Enter Student Name:")
            course_marks_input = simpledialog.askstring("Course Marks",
                                                        "Enter Course Marks (comma-separated, e.g., 15,20,18):")
            course_marks = list(map(int, course_marks_input.split(',')))
            exam_mark = int(simpledialog.askstring("Exam Mark", "Enter Exam Mark (0-100):"))

            new_student = Student(student_id, name, course_marks, exam_mark)
            self.students.append(new_student)

        # saving the new student info in the main file
            with open("studentMarks.txt", 'a') as file:
                file.write(f"{student_id},{name},{','.join(map(str, course_marks))},{exam_mark}\n")

            self.display_message("Student record added successfully.")
        except Exception as e:
            self.display_message(f"Error adding student record: {e}")

    def delete_record(self):
        # allows user to delete a record by just asking for student name or ID
        student_identifier = simpledialog.askstring("Delete Student", "Enter student Name or ID to delete:")
        if not student_identifier:
            return

        original_count = len(self.students)
        self.students = [s for s in self.students if
                         str(s.student_id) != student_identifier and s.name.lower() != student_identifier.lower()]

        if len(self.students) < original_count:

            self.save_data("studentMarks.txt")
            self.display_message(f"Student '{student_identifier}' deleted successfully.")
        else:
            self.display_message(f"No student found with name or ID '{student_identifier}'.")

    def update_record(self):
        # allows user to edit the info of students
        student_identifier = simpledialog.askstring("Update Student", "Enter Student Name or ID to update:")
        if not student_identifier:
            return

        for student in self.students:
            if str(student.student_id) == student_identifier or student.name.lower() == student_identifier.lower():
                update_field = simpledialog.askstring("Update Field",
                                                      "What do you want to update? (name, course_marks, exam_mark)")
                if update_field.lower() == 'name':
                    new_name = simpledialog.askstring("New Name", "Enter new name:")
                    student.name = new_name
                elif update_field.lower() == 'course_marks':
                    course_marks_input = simpledialog.askstring("New Course Marks",
                                                                "Enter new Course Marks (comma-separated):")
                    student.course_marks = list(map(int, course_marks_input.split(',')))
                elif update_field.lower() == 'exam_mark':
                    exam_mark = int(simpledialog.askstring("New Exam Mark", "Enter new Exam Mark (0-100):"))
                    student.exam_mark = exam_mark
                else:
                    self.display_message("Invalid field for update.")
                    return

                # after updating again managing the percentage
                student.total_coursework_mark = sum(student.course_marks)
                student.overall_percentage = (student.total_coursework_mark + student.exam_mark) / 160 * 100
                student.grade = student.calculate_grade()

                # saving the updated text in the file
                self.save_data("studentMarks.txt")
                self.display_message("Student record updated successfully.")
                return

        self.display_message(f"No student found with name or ID '{student_identifier}'.")

    def save_data(self, filename):
        # Save the student data back to the file
        with open(filename, 'w') as file:
            for student in self.students:
                file.write(
                    f"{student.student_id},{student.name},{','.join(map(str, student.course_marks))},{student.exam_mark}\n")


# creating the Tkinter app
root = tk.Tk()
app = StudentRecordsApp(root)
root.mainloop()
