import tkinter as tk
from tkinter import filedialog
import sys

# Verificar versión de Python
if sys.version_info < (3, 9):
    raise Exception("Este programa requiere Python 3.9 o superior")
# Importar el módulo de proyección
from src.services.windows import ProjectionModule
# Ejecutar el módulo
if __name__ == "__main__":
    app = ProjectionModule()
    app.run()
