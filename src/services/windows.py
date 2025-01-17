from tkinter import Tk, filedialog, ttk
import tkinter as tk
from tkinter import filedialog
from .slide_manager import SlideManager as sm
from .import_from_json import ImportFromJson as ifj
import screeninfo

class ProjectionModule:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Proyección")
        self.root.geometry("1200x600")
        self.root.configure(bg="black")

        # Panel lateral para lista de canciones
        self.song_list_frame = tk.Frame(self.root, bg="gray")
        self.song_list_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.song_listbox = tk.Listbox(self.song_list_frame, bg="white", font=("Arial", 12))
        self.song_listbox.pack(fill=tk.BOTH, expand=True)

        # Cargar canciones desde musics.json
        try:
            import json
            with open('./data/lyrics.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                for song in data:
                    title = song['title'][:30] + '...' if len(song['title']) > 30 else song['title']
                    self.song_listbox.insert(tk.END, title)
                self.song_listbox.bind('<<ListboxSelect>>', lambda e: self.show_preview(data[self.song_listbox.curselection()[0]]))
        except Exception as e:
            print(f"Error al cargar musics.json: {e}")
        # Botón para importar canciones
        tk.Button(self.song_list_frame, text="Importar desde Holyrics", command=ifj.import_from_json).pack(pady=5)

        # Panel de contenido principal
        self.content_frame = tk.Frame(self.root, bg="black")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Vista previa de diapositivas
        self.preview_label = tk.Label(self.content_frame, text="Vista Previa", font=("Arial", 18), bg="black", fg="white")
        self.preview_label.pack(pady=20)

        # Botones de control
        control_frame = tk.Frame(self.root, bg="black")
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(control_frame, text="Siguiente (→)", command=sm.next_slide).pack(side=tk.RIGHT, padx=10)
        tk.Button(control_frame, text="Anterior (←)", command=sm.previous_slide).pack(side=tk.RIGHT, padx=10)

        # Segunda ventana para proyección
        self.second_window = None

    def import_holyrics(self):
        # Simulación: Importar canciones desde un archivo JSON
        file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if file_path:
            import json
            with open(file_path, 'r') as file:
                data = json.load(file)
                for song in data.get("songs", []):
                    self.song_listbox.insert(tk.END, song["title"])

    def get_secondary_screen_geometry(self):
        # Obtener la geometría del monitor secundario usando screeninfo
        screens = screeninfo.get_monitors()
        print("Hay" + str(len(screens)) + " monitores")
        if len(screens) > 1:
            second_screen = screens[1]  # Asumir que el segundo monitor es el deseado
            if screens[0].is_primary:
                second_screen = screens[1]
            else:
                second_screen = screens[0]
            return second_screen.x, second_screen.y, second_screen.width, second_screen.height
        return None

    def open_second_window(self):
        screen_geometry = self.get_secondary_screen_geometry()
        #file = sm.get_current_slide()
        #if file:
        #    file.show_slide(self.second_window)
        #else:
        #    print("No hay archivo")
        #    return str("black")
        if screen_geometry:
            #print("Mostrando segunda pantalla en" + str(self.get_secondary_screen_geometry.name()))
            x, y, width, height = screen_geometry
            if self.second_window is None or not tk.Toplevel.winfo_exists(self.second_window):
                self.second_window = tk.Toplevel(self.root)
                self.second_window.title("Público")
                self.second_window.geometry(f"{width}x{height}+{x}+{y}")
                self.second_window.attributes('-fullscreen', False)
                self.second_window.configure(bg=file.get_background_color())
                self.second_window.overrideredirect(True)
                self.second_window.attributes('-topmost', True)
                self.second_window.attributes('-fullscreen', True)
                #self.second_window.configure(bg=file.get_background_color())
                self.second_window.configure(bg='black')
                self.second_window.overrideredirect(True)
                self.second_window.attributes('-topmost', True)
                file.show_slide(self)
                
        else:
            self.second_window = None
            self.second_window = tk.Toplevel(self.root)
            self.second_window.title("Error")
            label = tk.Label(self.second_window, text="No se encontró una segunda pantalla", font=("Arial", 16), bg="black", fg="white")
            label.pack(expand=True)
    def run(self):
        self.open_second_window()
        self.root.mainloop()