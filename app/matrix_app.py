import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from app.gui import MatrixAppUI
from domain.matrix_operations import MatrixOperations

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Operations")
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.matrix_operations = MatrixOperations()
        self.app_ui = MatrixAppUI(self.root, self.matrix_operations)
        
    def run(self):
        self.root.mainloop()
