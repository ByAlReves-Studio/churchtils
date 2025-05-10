import tkinter as tk
from tkinter import filedialog

# Importar el módulo de proyección
from src.services.windows import ProjectionModule
# Ejecutar el módulo
if __name__ == "__main__":
    app = ProjectionModule()
    app.run()
