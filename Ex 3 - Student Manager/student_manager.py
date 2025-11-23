import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager Pro")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f0f4f8")
        
        self.students = []
        self.load_data()
        
        # Create main container with gradient-like background
        self.setup_ui()
        
    def load_data(self):
        """Load student data from file"""
        try:
            with open('studentMarks.txt', 'r') as file:
                lines = file.readlines()
                student_count = int(lines[0].strip())
                self.students = []
                
                for i in range(1, student_count + 1):
                    parts = lines[i].strip().split(',')
                    student = {
                        'code': parts[0],
                        'name': parts[1],
                        'coursework1': int(parts[2]),
                        'coursework2': int(parts[3]),
                        'coursework3': int(parts[4]),
                        'exam': int(parts[5])
                    }
                    self.students.append(student)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def save_data(self):
        """Save student data to file"""
        try:
            with open('studentMarks.txt', 'w') as file:
                file.write(f"{len(self.students)}\n")
                for student in self.students:
                    file.write(f"{student['code']},{student['name']},{student['coursework1']},"
                             f"{student['coursework2']},{student['coursework3']},{student['exam']}\n")
            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def calculate_stats(self, student):
        """Calculate student statistics"""
        total_coursework = student['coursework1'] + student['coursework2'] + student['coursework3']
        overall_percentage = ((total_coursework + student['exam']) / 160) * 100
        
        if overall_percentage >= 70:
            grade = 'A'
        elif overall_percentage >= 60:
            grade = 'B'
        elif overall_percentage >= 50:
            grade = 'C'
        elif overall_percentage >= 40:
            grade = 'D'
        else:
            grade = 'F'
        
        return {
            'total_coursework': total_coursework,
            'overall_percentage': round(overall_percentage, 2),
            'grade': grade
        }
    
    def get_grade_color(self, grade):
        """Return color based on grade"""
        colors = {
            'A': '#10b981',
            'B': '#3b82f6',
            'C': '#f59e0b',
            'D': '#f97316',
            'F': '#ef4444'
        }
        return colors.get(grade, '#6b7280')
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#4f46e5", height=120)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎓 Student Manager Pro",
            font=("Helvetica", 32, "bold"),
            bg="#4f46e5",
            fg="white"
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Advanced Academic Performance Tracking System",
            font=("Helvetica", 12),
            bg="#4f46e5",
            fg="#e0e7ff"
        )
        subtitle_label.pack()
        
        # Menu Bar Frame
        menu_frame = tk.Frame(self.root, bg="#6366f1", height=60)
        menu_frame.pack(fill=tk.X)
        menu_frame.pack_propagate(False)
        
        # Menu Buttons with modern styling
        button_style = {
            'font': ('Helvetica', 11, 'bold'),
            'bg': '#8b5cf6',
            'fg': 'white',
            'activebackground': '#7c3aed',
            'activeforeground': 'white',
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'padx': 20,
            'pady': 10
        }
        
        buttons_data = [
            ("📊 View All", self.view_all_students),
            ("🔍 Search Student", self.view_individual_student),
            ("🏆 Highest Score", self.show_highest_student),
            ("📉 Lowest Score", self.show_lowest_student),
            ("↕️ Sort Records", self.sort_students),
            ("➕ Add Student", self.add_student),
            ("🗑️ Delete Student", self.delete_student),
            ("✏️ Update Student", self.update_student)
        ]
        
        for text, command in buttons_data:
            btn = tk.Button(menu_frame, text=text, command=command, **button_style)
            btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Main Content Frame
        self.content_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard with statistics"""
        self.clear_content()
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(self.content_frame, bg="#f0f4f8", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Statistics Cards
        stats_frame = tk.Frame(scrollable_frame, bg="#f0f4f8")
        stats_frame.pack(fill=tk.X, pady=20)
        
        total_students = len(self.students)
        avg_percentage = sum(self.calculate_stats(s)['overall_percentage'] for s in self.students) / total_students if total_students > 0 else 0
        
        stats = [
            ("Total Students", str(total_students), "#3b82f6"),
            ("Average Score", f"{avg_percentage:.2f}%", "#10b981"),
            ("Highest Score", f"{self.calculate_stats(self.get_highest_student())['overall_percentage']:.2f}%" if self.students else "N/A", "#f59e0b"),
            ("Grade A Count", str(sum(1 for s in self.students if self.calculate_stats(s)['grade'] == 'A')), "#8b5cf6")
        ]
        
        for title, value, color in stats:
            card = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, bd=0)
            card.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            
            tk.Label(card, text=title, font=("Helvetica", 12), bg=color, fg="white").pack(pady=(20, 5))
            tk.Label(card, text=value, font=("Helvetica", 24, "bold"), bg=color, fg="white").pack(pady=(0, 20))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def view_all_students(self):
        """Display all student records"""
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="📊 All Student Records",
            font=("Helvetica", 24, "bold"),
            bg="#f0f4f8",
            fg="#1e293b"
        )
        title.pack(pady=(0, 20))
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(self.content_frame, bg="#f0f4f8", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display students in a grid
        col = 0
        row = 0
        for student in self.students:
            self.create_student_card(scrollable_frame, student, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Summary
        summary_frame = tk.Frame(scrollable_frame, bg="#1e293b", relief=tk.RAISED, bd=2)
        summary_frame.grid(row=row+1, column=0, columnspan=3, sticky="ew", padx=10, pady=20)
        
        avg_percentage = sum(self.calculate_stats(s)['overall_percentage'] for s in self.students) / len(self.students)
        
        tk.Label(
            summary_frame,
            text=f"Total Students: {len(self.students)} | Average Percentage: {avg_percentage:.2f}%",
            font=("Helvetica", 14, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_student_card(self, parent, student, row, col):
        """Create a student card widget"""
        stats = self.calculate_stats(student)
        grade_color = self.get_grade_color(stats['grade'])
        
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2, width=400)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Header with grade
        header = tk.Frame(card, bg=grade_color, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=student['name'],
            font=("Helvetica", 16, "bold"),
            bg=grade_color,
            fg="white"
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        tk.Label(
            header,
            text=f"ID: {student['code']}",
            font=("Helvetica", 10),
            bg=grade_color,
            fg="white"
        ).pack(anchor="w", padx=15)
        
        grade_label = tk.Label(
            header,
            text=stats['grade'],
            font=("Helvetica", 32, "bold"),
            bg=grade_color,
            fg="white"
        )
        grade_label.place(relx=0.85, rely=0.5, anchor="center")
        
        # Body with details
        body = tk.Frame(card, bg="white")
        body.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        details = [
            ("Coursework Total:", f"{stats['total_coursework']}/60"),
            ("Exam Score:", f"{student['exam']}/100"),
            ("Overall Percentage:", f"{stats['overall_percentage']}%"),
            ("Grade:", stats['grade'])
        ]
        
        for label, value in details:
            row_frame = tk.Frame(body, bg="white")
            row_frame.pack(fill=tk.X, pady=3)
            
            tk.Label(
                row_frame,
                text=label,
                font=("Helvetica", 10),
                bg="white",
                fg="#64748b"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row_frame,
                text=value,
                font=("Helvetica", 10, "bold"),
                bg="white",
                fg="#1e293b"
            ).pack(side=tk.RIGHT)
    
    def view_individual_student(self):
        """Search and view individual student"""
        search_term = simpledialog.askstring("Search Student", "Enter Student Name or Code:")
        
        if not search_term:
            return
        
        found_student = None
        for student in self.students:
            if search_term.lower() in student['name'].lower() or search_term in student['code']:
                found_student = student
                break
        
        if found_student:
            self.clear_content()
            
            title = tk.Label(
                self.content_frame,
                text="🔍 Student Record",
                font=("Helvetica", 24, "bold"),
                bg="#f0f4f8",
                fg="#1e293b"
            )
            title.pack(pady=(0, 20))
            
            container = tk.Frame(self.content_frame, bg="#f0f4f8")
            container.pack(expand=True)
            
            self.create_student_card(container, found_student, 0, 0)
        else:
            messagebox.showwarning("Not Found", "Student not found!")
    
    def get_highest_student(self):
        """Get student with highest score"""
        return max(self.students, key=lambda s: self.calculate_stats(s)['overall_percentage'])
    
    def get_lowest_student(self):
        """Get student with lowest score"""
        return min(self.students, key=lambda s: self.calculate_stats(s)['overall_percentage'])
    
    def show_highest_student(self):
        """Display student with highest score"""
        if not self.students:
            messagebox.showwarning("No Data", "No student records available!")
            return
        
        highest = self.get_highest_student()
        self.clear_content()
        
        title = tk.Label(
            self.content_frame,
            text="🏆 Highest Scoring Student",
            font=("Helvetica", 24, "bold"),
            bg="#f0f4f8",
            fg="#1e293b"
        )
        title.pack(pady=(0, 20))
        
        container = tk.Frame(self.content_frame, bg="#f0f4f8")
        container.pack(expand=True)
        
        self.create_student_card(container, highest, 0, 0)
    
    def show_lowest_student(self):
        """Display student with lowest score"""
        if not self.students:
            messagebox.showwarning("No Data", "No student records available!")
            return
        
        lowest = self.get_lowest_student()
        self.clear_content()
        
        title = tk.Label(
            self.content_frame,
            text="📉 Lowest Scoring Student",
            font=("Helvetica", 24, "bold"),
            bg="#f0f4f8",
            fg="#1e293b"
        )
        title.pack(pady=(0, 20))
        
        container = tk.Frame(self.content_frame, bg="#f0f4f8")
        container.pack(expand=True)
        
        self.create_student_card(container, lowest, 0, 0)
    
    def sort_students(self):
        """Sort students by overall percentage"""
        self.clear_content()
        
        title = tk.Label(
            self.content_frame,
            text="↕️ Sort Students",
            font=("Helvetica", 24, "bold"),
            bg="#f0f4f8",
            fg="#1e293b"
        )
        title.pack(pady=20)
        
        btn_frame = tk.Frame(self.content_frame, bg="#f0f4f8")
        btn_frame.pack(pady=20)
        
        def sort_asc():
            self.students.sort(key=lambda s: self.calculate_stats(s)['overall_percentage'])
            self.view_all_students()
        
        def sort_desc():
            self.students.sort(key=lambda s: self.calculate_stats(s)['overall_percentage'], reverse=True)
            self.view_all_students()
        
        tk.Button(
            btn_frame,
            text="⬆️ Sort Ascending",
            command=sort_asc,
            font=("Helvetica", 14, "bold"),
            bg="#10b981",
            fg="white",
            padx=30,
            pady=15,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame,
            text="⬇️ Sort Descending",
            command=sort_desc,
            font=("Helvetica", 14, "bold"),
            bg="#3b82f6",
            fg="white",
            padx=30,
            pady=15,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
    
    def add_student(self):
        """Add a new student"""
        self.clear_content()
        
        title = tk.Label(
            self.content_frame,
            text="➕ Add New Student",
            font=("Helvetica", 24, "bold"),
            bg="#f0f4f8",
            fg="#1e293b"
        )
        title.pack(pady=20)
        
        form_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        form_frame.pack(padx=100, pady=20, fill=tk.BOTH, expand=True)
        
        fields = [
            ("Student Code (1000-9999):", "code"),
            ("Student Name:", "name"),
            ("Coursework 1 (out of 20):", "cw1"),
            ("Coursework 2 (out of 20):", "cw2"),
            ("Coursework 3 (out of 20):", "cw3"),
            ("Exam Mark (out of 100):", "exam")
        ]
        
        entries = {}
        
        for i, (label_text, key) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label_text,
                font=("Helvetica", 12),
                bg="white",
                fg="#1e293b"
            ).grid(row=i, column=0, sticky="w", padx=30, pady=15)
            
            entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
            entry.grid(row=i, column=1, padx=30, pady=15)
            entries[key] = entry
        
        def submit():
            try:
                new_student = {
                    'code': entries['code'].get(),
                    'name': entries['name'].get(),
                    'coursework1': int(entries['cw1'].get()),
                    'coursework2': int(entries['cw2'].get()),
                    'coursework3': int(entries['cw3'].get()),
                    'exam': int(entries['exam'].get())
                }
                
                # Validation
                if not (1000 <= int(new_student['code']) <= 9999):
                    messagebox.showerror("Error", "Student code must be between 1000 and 9999")
                    return
                
                if not all(0 <= new_student[f'coursework{i}'] <= 20 for i in range(1, 4)):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20")
                    return
                
                if not (0 <= new_student['exam'] <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                    return
                
                self.students.append(new_student)
                self.save_data()
                self.view_all_students()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks")
        
        tk.Button(
            form_frame,
            text="✓ Add Student",
            command=submit,
            font=("Helvetica", 14, "bold"),
            bg="#10b981",
            fg="white",
            padx=40,
            pady=15,
            relief=tk.FLAT,
            cursor="hand2"
        ).grid(row=len(fields), column=0, columnspan=2, pady=30)
    
    def delete_student(self):
        """Delete a student record"""
        search_term = simpledialog.askstring("Delete Student", "Enter Student Name or Code to Delete:")
        
        if not search_term:
            return
        
        found_index = -1
        for i, student in enumerate(self.students):
            if search_term.lower() in student['name'].lower() or search_term in student['code']:
                found_index = i
                break
        
        if found_index != -1:
            student = self.students[found_index]
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete {student['name']} ({student['code']})?"
            )
            
            if confirm:
                self.students.pop(found_index)
                self.save_data()
                self.view_all_students()
        else:
            messagebox.showwarning("Not Found", "Student not found!")
    
    def update_student(self):
        """Update a student record"""
        search_term = simpledialog.askstring("Update Student", "Enter Student Name or Code to Update:")
        
        if not search_term:
            return
        
        found_student = None
        found_index = -1
        for i, student in enumerate(self.students):
            if search_term.lower() in student['name'].lower() or search_term in student['code']:
                found_student = student
                found_index = i
                break
        
        if not found_student:
            messagebox.showwarning("Not Found", "Student not found!")
            return
        
        self.clear_content()
        
        title = tk.Label(
            self.content_frame,
            text=f"✏️ Update Student: {found_student['name']}",
            font=("Helvetica", 24, "bold"),
            bg="#f0f4f8",
            fg="#1e293b"
        )
        title.pack(pady=20)
        
        form_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        form_frame.pack(padx=100, pady=20, fill=tk.BOTH, expand=True)
        
        fields = [
            ("Student Code:", "code", found_student['code']),
            ("Student Name:", "name", found_student['name']),
            ("Coursework 1:", "cw1", str(found_student['coursework1'])),
            ("Coursework 2:", "cw2", str(found_student['coursework2'])),
            ("Coursework 3:", "cw3", str(found_student['coursework3'])),
            ("Exam Mark:", "exam", str(found_student['exam']))
        ]
        
        entries = {}
        
        for i, (label_text, key, default) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label_text,
                font=("Helvetica", 12),
                bg="white",
                fg="#1e293b"
            ).grid(row=i, column=0, sticky="w", padx=30, pady=15)
            
            entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=30, pady=15)
            entries[key] = entry
        
        def submit():
            try:
                updated_student = {
                    'code': entries['code'].get(),
                    'name': entries['name'].get(),
                    'coursework1': int(entries['cw1'].get()),
                    'coursework2': int(entries['cw2'].get()),
                    'coursework3': int(entries['cw3'].get()),
                    'exam': int(entries['exam'].get())
                }
                
                self.students[found_index] = updated_student
                self.save_data()
                self.view_all_students()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks")
        
        tk.Button(
            form_frame,
            text="✓ Update Student",
            command=submit,
            font=("Helvetica", 14, "bold"),
            bg="#3b82f6",
            fg="white",
            padx=40,
            pady=15,
            relief=tk.FLAT,
            cursor="hand2"
        ).grid(row=len(fields), column=0, columnspan=2, pady=30)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()