import customtkinter as ctk
from tkinter import messagebox
from domain.matrix import Matrix
from fractions import Fraction

class MatrixAppUI:
    def __init__(self, root, matrix_operations):
        self.root = root
        self.matrix_operations = matrix_operations
        self.matrix = None
        self.entries = []

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(root, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Calculadora de Matrizes", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=(10, 20))

        self.dim_frame = ctk.CTkFrame(self.main_frame)
        self.dim_frame.pack(pady=10)
        self.create_dimension_widgets()

        self.create_matrix_button = ctk.CTkButton(self.main_frame, text="Criar Matriz", command=self.create_matrix, width=220, height=40)
        self.create_matrix_button.pack(pady=10)

        self.matrix_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.matrix_frame.pack(pady=10)

        self.create_operation_buttons()

        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(pady=20, fill="both", expand=True)
        self.create_result_labels()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.minsize(600, 400)

    def create_dimension_widgets(self):
        ctk.CTkLabel(self.dim_frame, text="Linhas:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
        self.row_entry = ctk.CTkEntry(self.dim_frame, width=80)
        self.row_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.dim_frame, text="Colunas:", font=("Arial", 14)).grid(row=0, column=2, padx=10, pady=5)
        self.col_entry = ctk.CTkEntry(self.dim_frame, width=80)
        self.col_entry.grid(row=0, column=3, padx=10, pady=5)

    def create_operation_buttons(self):
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.determinant_button = ctk.CTkButton(button_frame, text="Calcular Determinante", command=self.calculate_determinant, width=200, height=40)
        self.determinant_button.grid(row=0, column=0, padx=10, pady=5)

        self.triangularize_button = ctk.CTkButton(button_frame, text="Triangularizar Matriz", command=self.triangularize_matrix, width=200, height=40)
        self.triangularize_button.grid(row=0, column=1, padx=10, pady=5)

    def create_result_labels(self):
        self.determinant_label = ctk.CTkLabel(self.result_frame, text="", font=("Arial", 14, "bold"), anchor="w", wraplength=400)
        self.determinant_label.pack(pady=5, padx=10, fill="x")

        self.triangularization_scroll_frame = ctk.CTkScrollableFrame(self.result_frame, width=400, height=250)
        self.triangularization_scroll_frame.pack(pady=5, fill="both", expand=True)

        self.triangularization_label = ctk.CTkLabel(self.triangularization_scroll_frame, text="", font=("Arial", 12), anchor="w", justify="left", wraplength=400)
        self.triangularization_label.grid(row=0, column=0, padx=5, pady=5)

    def create_matrix(self):
        self.clear_results()
        try:
            rows, cols = self.get_matrix_dimensions()
            if rows <= 0 or cols <= 0:
                messagebox.showerror("Erro de Entrada", "O número de linhas e colunas deve ser maior que 0")
                return

            self.matrix = Matrix(rows, cols)
            self.clear_matrix_frame()
            self.create_matrix_entries(rows, cols)

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira números válidos para linhas e colunas.")

    def get_matrix_dimensions(self):
        return int(self.row_entry.get()), int(self.col_entry.get())

    def clear_matrix_frame(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries = []

    def create_matrix_entries(self, rows, cols):
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ctk.CTkEntry(self.matrix_frame, width=80, height=30, corner_radius=10)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def clear_results(self):
        self.determinant_label.configure(text="")
        self.triangularization_label.configure(text="")

    def calculate_determinant(self):
        if not self.matrix:
            messagebox.showerror("Erro", "Matriz não foi criada!")
            return

        try:
            self.clear_results()
            self.fill_matrix_from_entries()

            det = self.matrix_operations.calculate_determinant(self.matrix)
            det_sign = "(Positivo)" if det >= 0 else "(Negativo)"
            self.determinant_label.configure(text=f"Determinante: {det} {det_sign}")

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def triangularize_matrix(self):
        if not self.matrix:
            messagebox.showerror("Erro", "Matriz não foi criada!")
            return

        try:
            self.clear_results()
            self.fill_matrix_from_entries()

            triangularized, steps, determinant = self.matrix_operations.triangularize(self.matrix)
            det_sign = "(Positivo)" if determinant >= 0 else "(Negativo)"

            result_text = f"Matriz Triangularizada:\n{self.matrix_operations.to_string(triangularized)}\n\nPassos:\n"
            result_text += "\n".join(steps) + f"\n\nDeterminante: {determinant} {det_sign}"

            self.triangularization_label.configure(text=result_text)

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def fill_matrix_from_entries(self):
        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                value = entry.get().strip()
                if value:
                    self.matrix.set_value(i, j, Fraction(value))
                else:
                    self.matrix.set_value(i, j, Fraction(0))