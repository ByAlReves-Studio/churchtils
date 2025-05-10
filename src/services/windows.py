from tkinter import Tk, filedialog, ttk
import tkinter as tk
from tkinter import filedialog
from .slide_manager import SlideManager
# Crear una instancia del SlideManager
sm = SlideManager()
from .import_from_json import ImportFromJson as ifj
import screeninfo
import json

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
            with open('./data/lyrics.json', 'r', encoding='utf-8') as file:
                self.song_data = json.load(file)
                for song in self.song_data:
                    title = song['title'][:30] + '...' if len(song['title']) > 30 else song['title']
                    self.song_listbox.insert(tk.END, title)
                # Utilizar siempre on_song_select como el gestor de eventos, que es más seguro
                self.song_listbox.bind('<<ListboxSelect>>', self.on_song_select)
        except Exception as e:
            print(f"Error al cargar lyrics.json: {e}")
            self.song_data = []
            
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
        tk.Button(control_frame, text="Siguiente (→)", command=self.next_slide).pack(side=tk.RIGHT, padx=10)
        tk.Button(control_frame, text="Vaciar pantalla (✕)", command=self.start_projection).pack(side=tk.RIGHT, padx=10)
        tk.Button(control_frame, text="Anterior (←)", command=self.previous_slide).pack(side=tk.RIGHT, padx=10)

        # Segunda ventana para proyección
        self.second_window = None

    def import_holyrics(self):
        # Simulación: Importar canciones desde un archivo JSON
        file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for song in data.get("songs", []):
                        self.song_listbox.insert(tk.END, song["title"])
            except Exception as e:
                print(f"Error al importar: {e}")

    def get_secondary_screen_geometry(self):
        # Obtener la geometría del monitor secundario usando screeninfo
        screens = screeninfo.get_monitors()
        print("Hay " + str(len(screens)) + " monitores")
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
        if screen_geometry:
            x, y, width, height = screen_geometry
            if self.second_window is None or not tk.Toplevel.winfo_exists(self.second_window):
                self.second_window = tk.Toplevel(self.root)
                self.second_window.title("Público")
                self.second_window.geometry(f"{width}x{height}+{x}+{y}")
                self.second_window.attributes('-fullscreen', True)
                self.second_window.configure(bg='black')
                self.second_window.attributes('-topmost', True)
                # Crear un label para mostrar el contenido
                self.projection_label = tk.Label(self.second_window, text="", font=("Arial", 36), bg="black", fg="white", wraplength=width-100, justify=tk.CENTER)
                self.projection_label.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
                # Intentar mostrar la diapositiva actual si hay alguna
                self.update_projection()
                
        else:
            self.second_window = None
            self.second_window = tk.Toplevel(self.root)
            self.second_window.title("Error")
            label = tk.Label(self.second_window, text="No se encontró una segunda pantalla", font=("Arial", 16), bg="black", fg="white")
            label.pack(expand=True)
            
    def on_song_select(self, event):
        # Obtener el índice seleccionado
        try:
            selected_index = self.song_listbox.curselection()[0]
            # Cargar los datos si no están ya en memoria
            if not hasattr(self, 'song_data') or not self.song_data:
                with open('./data/lyrics.json', 'r', encoding='utf-8') as file:
                    self.song_data = json.load(file)
            # Asegurarse de que el índice es válido
            if 0 <= selected_index < len(self.song_data):
                self.show_preview(self.song_data[selected_index])
            else:
                print(f"Índice seleccionado inválido: {selected_index}, total elementos: {len(self.song_data)}")
        except Exception as e:
            print(f"Error al seleccionar canción: {e}")

    def show_preview(self, song_data):
        # Limpiar el contenido previo
        for widget in self.content_frame.winfo_children():
            if widget != self.preview_label:  # Mantener el título
                widget.destroy()

        # Mostrar título
        title_label = tk.Label(self.content_frame, text=song_data['title'], font=("Arial", 16, "bold"), bg="black", fg="white")
        title_label.pack(pady=(0, 10))

        # Mostrar artista si está disponible
        if 'artist' in song_data and song_data['artist']:
            artist_label = tk.Label(self.content_frame, text=f"Por: {song_data['artist']}", font=("Arial", 12), bg="black", fg="white")
            artist_label.pack(pady=(0, 20))

        # Mostrar las diapositivas/versos
        if 'slides' in song_data and isinstance(song_data['slides'], list):
            # Frame para contener las diapositivas
            slides_frame = tk.Frame(self.content_frame, bg="black")
            slides_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Mostrar cada diapositiva como un texto
            for i, slide_text in enumerate(song_data['slides']):
                slide_label = tk.Label(slides_frame, text=slide_text, font=("Arial", 14), bg="black", fg="white", justify=tk.LEFT, wraplength=500)
                slide_label.pack(pady=10, anchor="w")
                
                # Separador entre slides (excepto el último)
                if i < len(song_data['slides']) - 1:
                    separator = tk.Frame(slides_frame, height=2, bg="gray")
                    separator.pack(fill=tk.X, pady=5)
        else:
            no_slides_label = tk.Label(self.content_frame, text="No hay diapositivas disponibles", font=("Arial", 14), bg="black", fg="red")
            no_slides_label.pack(pady=20)

        # Cargar las diapositivas en el administrador de slides
        if 'slides' in song_data:
            slides_formatted = [{'text': slide} for slide in song_data['slides']]
            sm.load_slides(slides_formatted)

    def update_projection(self):
        """Actualiza el contenido de la ventana de proyección con la diapositiva actual"""
        if self.second_window is None or not tk.Toplevel.winfo_exists(self.second_window):
            return
            
        current_slide = sm.get_current_slide()
        if current_slide and 'text' in current_slide:
            self.projection_label.config(text=current_slide['text'])
        else:
            self.projection_label.config(text="")
    
    def next_slide(self):
        """Avanza a la siguiente diapositiva y actualiza la proyección"""
        sm.next_slide()
        self.update_projection()
    
    def previous_slide(self):
        """Retrocede a la diapositiva anterior y actualiza la proyección"""
        sm.previous_slide()
        self.update_projection()
            
    def run(self):
        self.open_second_window()
        self.root.mainloop()