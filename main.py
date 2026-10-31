
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

# ==========================================
# 1. FILE PATHS AND DATA STORAGE
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_FILE = os.path.join(
    BASE_DIR, "student_performance_dataset.csv"
)

FILE_NAME = os.path.join(
    BASE_DIR, "students.csv"
)

students = []

# Stores only the students added through the application
new_students = []

subjects = [
    "Python",
    "DBMS",
    "DAA",
    "Java",
    "Mathematics"
]


# ==========================================
# 2. CONVERT CSV ROW INTO STUDENT RECORD
# ==========================================

def create_student(row):

    marks = [
        float(row["Python"]),
        float(row["DBMS"]),
        float(row["DAA"]),
        float(row["Java"]),
        float(row["Mathematics"])
    ]

    return {
        "Name": str(row["Name"]),
        "Roll Number": str(row["Roll Number"]),
        "Marks": marks,
        "Total": float(row["Total"]),
        "Percentage": float(row["Percentage"])
    }


# ==========================================
# 3. LOAD THE MAIN 500-RECORD DATASET
# ==========================================

def load_dataset():

    if not os.path.exists(DATASET_FILE):

        messagebox.showwarning(
            "Dataset Missing",
            "student_performance_dataset.csv was not found.\n"
            "Please place it in the same folder as main.py."
        )
        return

    try:

        df = pd.read_csv(DATASET_FILE)

        required_columns = [
            "Name", "Roll Number",
            "Python", "DBMS", "DAA",
            "Java", "Mathematics",
            "Total", "Percentage"
        ]

        for column in required_columns:
            if column not in df.columns:
                raise ValueError(
                    f"Missing column: {column}"
                )

        for _, row in df.iterrows():

            student = create_student(row)

            students.append(student)

    except Exception as error:

        messagebox.showerror(
            "Dataset Error",
            str(error)
        )


# ==========================================
# 4. LOAD NEWLY ADDED STUDENTS
# ==========================================

def load_added_students():

    if not os.path.exists(FILE_NAME):
        return

    try:

        with open(FILE_NAME, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                student = create_student(row)

                # Avoid duplicate roll numbers
                duplicate = any(
                    s["Roll Number"] == student["Roll Number"]
                    for s in students
                )

                if not duplicate:

                    students.append(student)
                    new_students.append(student)

    except Exception as error:

        messagebox.showerror(
            "File Error",
            str(error)
        )


# ==========================================
# 5. SAVE NEW STUDENTS TO CSV
# ==========================================

def save_students():

    try:

        with open(FILE_NAME, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Name", "Roll Number",
                "Python", "DBMS", "DAA",
                "Java", "Mathematics",
                "Total", "Percentage"
            ])

            for student in new_students:

                writer.writerow([
                    student["Name"],
                    student["Roll Number"],
                    *student["Marks"],
                    student["Total"],
                    student["Percentage"]
                ])

    except Exception as error:

        messagebox.showerror(
            "Save Error",
            str(error)
        )


# ==========================================
# 6. ADD STUDENT
# ==========================================

def add_student():

    name = entries["Student Name"].get().strip()
    roll = entries["Roll Number"].get().strip()

    if not name or not roll:

        messagebox.showwarning(
            "Input Error",
            "Please enter student name and roll number."
        )
        return

    # Check duplicate roll number
    for student in students:

        if student["Roll Number"] == roll:

            messagebox.showerror(
                "Duplicate Error",
                "This roll number already exists."
            )
            return

    try:

        marks = []

        for subject in subjects:

            value = float(
                entries[subject + " Marks"].get()
            )

            if value < 0 or value > 100:

                messagebox.showerror(
                    "Invalid Marks",
                    "Marks must be between 0 and 100."
                )
                return

            marks.append(value)

        total = sum(marks)
        percentage = total / len(subjects)

        student = {
            "Name": name,
            "Roll Number": roll,
            "Marks": marks,
            "Total": total,
            "Percentage": percentage
        }

        students.append(student)
        new_students.append(student)

        save_students()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        # Clear all input fields
        for entry in entries.values():
            entry.delete(0, tk.END)

    except ValueError:

        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric marks."
        )


# ==========================================
# 7. VIEW ALL STUDENTS
# ==========================================

def view_students():

    if not students:

        messagebox.showwarning(
            "No Records",
            "No student records found."
        )
        return

    window = tk.Toplevel(root)
    window.title("Student Records")
    window.geometry("1100x500")

    tk.Label(
        window,
        text=f"Student Records - {len(students)} Students",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    columns = (
        "Name", "Roll", "Python", "DBMS",
        "DAA", "Java", "Maths",
        "Total", "Percentage"
    )

    table_frame = tk.Frame(window)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        table.heading(column, text=column)
        table.column(
            column,
            width=110,
            anchor="center"
        )

    # Vertical scrollbar
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(yscrollcommand=scrollbar.set)

    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Insert all student records
    for student in students:

        table.insert(
            "",
            tk.END,
            values=(
                student["Name"],
                student["Roll Number"],
                *student["Marks"],
                student["Total"],
                round(student["Percentage"], 2)
            )
        )


# ==========================================
# 8. CALCULATE STUDENT PERFORMANCE
# ==========================================

def calculate_performance():

    if not students:

        messagebox.showwarning(
            "No Records",
            "Please load student records first."
        )
        return

    # Convert student records into Pandas DataFrame
    df = pd.DataFrame([

        {
            "Name": student["Name"],
            "Roll Number": student["Roll Number"],
            "Python": student["Marks"][0],
            "DBMS": student["Marks"][1],
            "DAA": student["Marks"][2],
            "Java": student["Marks"][3],
            "Mathematics": student["Marks"][4],
            "Percentage": student["Percentage"]
        }

        for student in students

    ])

    # NumPy calculations
    percentages = np.array(df["Percentage"])

    average = np.mean(percentages)
    highest = np.max(percentages)
    lowest = np.min(percentages)
    median = np.median(percentages)
    standard_deviation = np.std(percentages)

    # Find topper
    topper = df.loc[df["Percentage"].idxmax()]

    # Subject-wise averages using Pandas
    subject_averages = df[subjects].mean()

    report = (
        "STUDENT PERFORMANCE REPORT\n"
        "================================\n\n"

        f"Total Students: {len(students)}\n"
        f"Class Average: {average:.2f}%\n"
        f"Highest Percentage: {highest:.2f}%\n"
        f"Lowest Percentage: {lowest:.2f}%\n"
        f"Median Percentage: {median:.2f}%\n"
        f"Standard Deviation: {standard_deviation:.2f}\n\n"

        "TOPPER DETAILS\n"
        "================================\n"

        f"Name: {topper['Name']}\n"
        f"Roll Number: {topper['Roll Number']}\n"
        f"Percentage: {topper['Percentage']:.2f}%\n\n"

        "SUBJECT-WISE AVERAGE\n"
        "================================\n"
    )

    for subject, marks in subject_averages.items():

        report += f"{subject}: {marks:.2f}\n"

    messagebox.showinfo(
        "Performance Analysis",
        report
    )


# ==========================================
# 9. GENERATE MATPLOTLIB CHARTS
# ==========================================

def generate_charts():

    if not students:

        messagebox.showwarning(
            "No Records",
            "Please load student records first."
        )
        return

    df = pd.DataFrame([

        {
            "Name": student["Name"],
            "Percentage": student["Percentage"],
            "Python": student["Marks"][0],
            "DBMS": student["Marks"][1],
            "DAA": student["Marks"][2],
            "Java": student["Marks"][3],
            "Mathematics": student["Marks"][4]
        }

        for student in students

    ])

    # First 30 students for readable charts
    chart_df = df.head(30)

    names = chart_df["Name"]
    percentages = chart_df["Percentage"]

    # Calculate average marks of all students
    subject_averages = df[subjects].mean()

    # Create three charts
    fig, axes = plt.subplots(
        1, 3,
        figsize=(18, 6)
    )

    # BAR CHART
    axes[0].bar(names, percentages)

    axes[0].set_title(
        "Student Performance - First 30 Students"
    )

    axes[0].set_xlabel("Students")
    axes[0].set_ylabel("Percentage")
    axes[0].set_ylim(0, 100)

    axes[0].tick_params(
        axis="x",
        rotation=90,
        labelsize=7
    )

    # PIE CHART
    axes[1].pie(
        subject_averages,
        labels=subjects,
        autopct="%1.1f%%"
    )

    axes[1].set_title(
        "Subject-wise Average Marks"
    )

    # LINE CHART
    axes[2].plot(
        names,
        percentages,
        marker="o"
    )

    axes[2].set_title(
        "Performance Trend - First 30 Students"
    )

    axes[2].set_xlabel("Students")
    axes[2].set_ylabel("Percentage")
    axes[2].set_ylim(0, 100)

    axes[2].tick_params(
        axis="x",
        rotation=90,
        labelsize=7
    )

    plt.tight_layout()
    plt.show()


# ==========================================
# 10. MAIN TKINTER WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Student Performance Analysis System"
)

root.geometry("1100x720")
root.configure(bg="#f2f4f8")


# Main heading
tk.Label(
    root,
    text="Student Performance Analysis System",
    font=("Arial", 22, "bold"),
    bg="#263859",
    fg="white",
    pady=20
).pack(fill="x")


# Form heading
tk.Label(
    root,
    text="Add Student Details",
    font=("Arial", 18, "bold"),
    bg="#f2f4f8"
).pack(pady=10)


# Input form
form = tk.Frame(
    root,
    bg="#f2f4f8"
)

form.pack()

fields = [
    "Student Name",
    "Roll Number",
    "Python Marks",
    "DBMS Marks",
    "DAA Marks",
    "Java Marks",
    "Mathematics Marks"
]

entries = {}

for i, field in enumerate(fields):

    tk.Label(
        form,
        text=field,
        font=("Arial", 11),
        bg="#f2f4f8"
    ).grid(
        row=i,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=25
    )

    entry.grid(
        row=i,
        column=1,
        padx=10,
        pady=5
    )

    entries[field] = entry


# ==========================================
# 11. BUTTONS
# ==========================================

button_frame = tk.Frame(
    root,
    bg="#f2f4f8"
)

button_frame.pack(pady=20)


# Add Student button
tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    width=22,
    bg="#263859",
    fg="white",
    font=("Arial", 11, "bold")
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)


# View Students button
tk.Button(
    button_frame,
    text="View Students",
    command=view_students,
    width=22,
    bg="#263859",
    fg="white",
    font=("Arial", 11, "bold")
).grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Calculate Performance button
tk.Button(
    button_frame,
    text="Calculate Performance",
    command=calculate_performance,
    width=22,
    bg="#263859",
    fg="white",
    font=("Arial", 11, "bold")
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)


# Generate Charts button
tk.Button(
    button_frame,
    text="Generate Charts",
    command=generate_charts,
    width=22,
    bg="#263859",
    fg="white",
    font=("Arial", 11, "bold")
).grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Exit button
tk.Button(
    button_frame,
    text="Exit",
    command=root.destroy,
    width=22,
    bg="#b83232",
    fg="white",
    font=("Arial", 11, "bold")
).grid(
    row=2,
    column=0,
    columnspan=2,
    pady=10
)


# ==========================================
# 12. LOAD DATA WHEN APPLICATION STARTS
# ==========================================

load_dataset()
load_added_students()

# Display number of loaded records
tk.Label(
    root,
    text=f"Total Student Records Loaded: {len(students)}",
    font=("Arial", 11, "bold"),
    bg="#f2f4f8",
    fg="#263859"
).pack(pady=5)


# Run application
root.mainloop()
