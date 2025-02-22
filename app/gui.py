import customtkinter as ctk
from tkinter import messagebox
from domain.matrix import Matrix

class MatrixAppUI:
    def __init__(self, root, matrix_operations):
        self.root = root
        self.matrix_operations = matrix_operations

        self.matrix = None
        self.entries = []

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(padx=20, pady=20)

        self.dim_frame = ctk.CTkFrame(self.main_frame)
        self.dim_frame.pack(pady=(0, 20))

        self.row_label = ctk.CTkLabel(self.dim_frame, text="Rows:", width=10)
        self.row_label.grid(row=0, column=0, padx=10)
        self.row_entry = ctk.CTkEntry(self.dim_frame, width=60)
        self.row_entry.grid(row=0, column=1)

        self.col_label = ctk.CTkLabel(self.dim_frame, text="Columns:", width=10)
        self.col_label.grid(row=0, column=2, padx=10)
        self.col_entry = ctk.CTkEntry(self.dim_frame, width=60)
        self.col_entry.grid(row=0, column=3)

        self.create_matrix_button = ctk.CTkButton(self.main_frame, text="Create Matrix", command=self.create_matrix)
        self.create_matrix_button.pack(pady=(10, 20))

        self.matrix_frame = ctk.CTkFrame(self.main_frame)
        self.matrix_frame.pack()

        self.determinant_button = ctk.CTkButton(self.main_frame, text="Calculate Determinant", command=self.calculate_determinant)
        self.determinant_button.pack(pady=10)

        self.triangularize_button = ctk.CTkButton(self.main_frame, text="Triangularize Matrix", command=self.triangularize_matrix)
        self.triangularize_button.pack(pady=10)

        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(pady=(20, 0))

        self.determinant_label = ctk.CTkLabel(self.result_frame, text="", font=("Arial", 12), width=300, anchor="w")
        self.determinant_label.pack(pady=5)

        self.triangularization_label = ctk.CTkLabel(self.result_frame, text="", font=("Arial", 12), width=300, anchor="w")
        self.triangularization_label.pack(pady=5)

    def setup_ui(self):
        self.determinant_label.configure(text="", font=("Arial", 12), text_color="white")
        self.triangularization_label.configure(text="", font=("Arial", 12), text_color="white")

    def create_matrix(self):
        self.determinant_label.configure(text="", font=("Arial", 12), text_color="white")
        self.triangularization_label.configure(text="", font=("Arial", 12), text_color="white")

        rows = int(self.row_entry.get())
        cols = int(self.col_entry.get())

        if rows <= 0 or cols <= 0:
            messagebox.showerror("Input Error", "Rows and columns must be greater than 0")
            return

        self.matrix = Matrix(rows, cols)

        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ctk.CTkEntry(self.matrix_frame, width=60)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def calculate_determinant(self):
        if not self.matrix:
            messagebox.showerror("Input Error", "Matrix not created!")
            return

        try:
            self.determinant_label.configure(text="", font=("Arial", 12), text_color="white")

            for i, row_entries in enumerate(self.entries):
                for j, entry in enumerate(row_entries):
                    value = float(entry.get()) if entry.get() else 0.0
                    self.matrix.set_value(i, j, value)

            det = self.matrix_operations.calculate_determinant(self.matrix)
            self.determinant_label.configure(text=f"Determinant: {det:.2f}", font=("Arial", 12, "bold"), text_color="white")
            self.triangularization_label.configure(text="")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def triangularize_matrix(self):
        if not self.matrix:
            messagebox.showerror("Input Error", "Matrix not created!")
            return

        try:
            self.determinant_label.configure(text="", font=("Arial", 12), text_color="white")

            for i, row_entries in enumerate(self.entries):
                for j, entry in enumerate(row_entries):
                    value = float(entry.get()) if entry.get() else 0.0
                    self.matrix.set_value(i, j, value)

            triangularized, steps = self.matrix_operations.triangularize(self.matrix)

            result_text = f"Triangularized Matrix:\n{self.matrix_operations.to_string(triangularized)}\n\nSteps:\n"
            result_text += "\n".join(steps)

            self.triangularization_label.configure(text=result_text, font=("Arial", 12, "bold"), text_color="white")
            self.determinant_label.configure(text="")

        except ValueError as e:
            messagebox.showerror("Error", str(e))