from app.matrix_app import MatrixApp
import customtkinter as ctk

if __name__ == "__main__":
    root = ctk.CTk()
    app = MatrixApp(root)
    app.run()