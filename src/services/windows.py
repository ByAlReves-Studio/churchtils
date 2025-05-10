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
        self.root.title("Sistema de Proyección")
        self.root.geometry("1280x720")
        self.root.configure(bg="#2C3E50")
        self.root.minsize(1024, 600)

        # Panel lateral para lista de canciones
        self.song_list_frame = tk.Frame(self.root, bg="#34495E", padx=10, pady=10)
        self.song_list_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Título del panel lateral
        tk.Label(self.song_list_frame, text="Lista de Canciones", font=("Helvetica", 14, "bold"), bg="#34495E", fg="white").pack(pady=(0,10))

        # Lista de canciones con scrollbar
        list_container = tk.Frame(self.song_list_frame, bg="#34495E")
        list_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.song_listbox = tk.Listbox(list_container, 
                                     bg="#ECF0F1", 
                                     fg="#2C3E50",
                                     font=("Helvetica", 12),
                                     selectmode=tk.SINGLE,
                                     activestyle='none',
                                     selectbackground="#3498DB",
                                     selectforeground="white",
                                     width=30)
        self.song_listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.song_listbox.yview)
        self.song_listbox.config(yscrollcommand=scrollbar.set)

        # Cargar canciones desde musics.json
        try:
            with open('./data/lyrics.json', 'r', encoding='utf-8') as file:
                self.song_data = json.load(file)
                for song in self.song_data:
                    title = song['title'][:30] + '...' if len(song['title']) > 30 else song['title']
                    self.song_listbox.insert(tk.END, title)
                self.song_listbox.bind('<<ListboxSelect>>', self.on_song_select)
        except Exception as e:
            print(f"Error al cargar lyrics.json: {e}")
            self.song_data = []
            
        # Botón para importar canciones
        import_button = tk.Button(self.song_list_frame, 
                                text="Importar desde Holyrics",
                                command=ifj.import_from_json,
                                bg="#3498DB",
                                fg="white",
                                font=("Helvetica", 10),
                                relief=tk.FLAT,
                                padx=10,
                                pady=5)
        import_button.pack(pady=10, fill=tk.X)

        # Panel de contenido principal
        self.content_frame = tk.Frame(self.root, bg="#2C3E50")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Vista previa de diapositivas
        self.preview_label = tk.Label(self.content_frame, 
                                    text="Vista Previa", 
                                    font=("Helvetica", 18, "bold"), 
                                    bg="#2C3E50", 
                                    fg="white")
        self.preview_label.pack(pady=20)

        # Botones de control
        control_frame = tk.Frame(self.content_frame, bg="#2C3E50", pady=10)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        button_style = {
            "font": ("Helvetica", 11),
            "bg": "#3498DB",
            "fg": "white",
            "relief": tk.FLAT,
            "padx": 15,
            "pady": 5
        }

        tk.Button(control_frame, text="Siguiente →", command=self.next_slide, **button_style).pack(side=tk.RIGHT, padx=5)
        tk.Button(control_frame, text="Vaciar ✕", command=self.clear_screen, **button_style).pack(side=tk.RIGHT, padx=5)
        tk.Button(control_frame, text="← Anterior", command=self.previous_slide, **button_style).pack(side=tk.RIGHT, padx=5)

        # Segunda ventana para proyección
        self.second_window = None

    def get_secondary_screen_geometry(self):
        screens = screeninfo.get_monitors()
        if len(screens) > 1:
            # Identificar la pantalla secundaria (no primaria)
            secondary_screens = [screen for screen in screens if not screen.is_primary]
            if secondary_screens:
                screen = secondary_screens[0]
                return screen.x, screen.y, screen.width, screen.height
        return None

    def open_second_window(self):
        screen_geometry = self.get_secondary_screen_geometry()
        if screen_geometry:
            x, y, width, height = screen_geometry
            if self.second_window is None or not tk.Toplevel.winfo_exists(self.second_window):
                self.second_window = tk.Toplevel(self.root)
                self.second_window.title("Proyección")
                self.second_window.geometry(f"{width}x{height}+{x}+{y}")
                # self.second_window.attributes('-fullscreen', True)
                self.second_window.configure(bg='black')
                self.second_window.attributes('-topmost', True)
                
                # Contenedor para centrar el texto verticalmente
                container = tk.Frame(self.second_window, bg="black")
                container.place(relx=0.5, rely=0.5, anchor="center")
                
                self.projection_label = tk.Label(container, 
                                               text="", 
                                               font=("Helvetica", 48), 
                                               bg="black", 
                                               fg="white", 
                                               wraplength=width-200, 
                                               justify=tk.CENTER)
                self.projection_label.pack(expand=True)
                
                self.update_projection()
        else:
            self.second_window = tk.Toplevel(self.root)
            self.second_window.title("Error")
            self.second_window.geometry("400x200")
            self.second_window.configure(bg="#2C3E50")
            label = tk.Label(self.second_window, 
                           text="No se encontró una segunda pantalla", 
                           font=("Helvetica", 14), 
                           bg="#2C3E50", 
                           fg="white")
            label.place(relx=0.5, rely=0.5, anchor="center")

    def on_song_select(self, event):
        try:
            selected_index = self.song_listbox.curselection()[0]
            if not hasattr(self, 'song_data') or not self.song_data:
                with open('./data/lyrics.json', 'r', encoding='utf-8') as file:
                    self.song_data = json.load(file)
            if 0 <= selected_index < len(self.song_data):
                self.show_preview(self.song_data[selected_index])
            else:
                print(f"Índice seleccionado inválido: {selected_index}, total elementos: {len(self.song_data)}")
        except Exception as e:
            print(f"Error al seleccionar canción: {e}")

    def show_preview(self, song_data):
        for widget in self.content_frame.winfo_children():
            if widget != self.preview_label:
                widget.destroy()

        preview_container = tk.Frame(self.content_frame, bg="#2C3E50")
        preview_container.pack(fill=tk.BOTH, expand=True, padx=20)

        title_label = tk.Label(preview_container, 
                             text=song_data['title'], 
                             font=("Helvetica", 16, "bold"), 
                             bg="#2C3E50", 
                             fg="white")
        title_label.pack(pady=(0, 10))

        if 'artist' in song_data and song_data['artist']:
            artist_label = tk.Label(preview_container, 
                                  text=f"Por: {song_data['artist']}", 
                                  font=("Helvetica", 12), 
                                  bg="#2C3E50", 
                                  fg="#BDC3C7")
            artist_label.pack(pady=(0, 20))

        if 'slides' in song_data and isinstance(song_data['slides'], list):
            canvas = tk.Canvas(preview_container, bg="#2C3E50", highlightthickness=0)
            scrollbar = tk.Scrollbar(preview_container, orient="vertical", command=canvas.yview)
            slides_frame = tk.Frame(canvas, bg="#2C3E50")

            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((0, 0), window=slides_frame, anchor="nw", width=canvas.winfo_reqwidth())

            for i, slide_text in enumerate(song_data['slides']):
                slide_frame = tk.Frame(slides_frame, bg="#34495E", padx=15, pady=15)
                slide_frame.pack(fill=tk.X, pady=5)
                
                slide_label = tk.Label(slide_frame, 
                                     text=slide_text, 
                                     font=("Helvetica", 12), 
                                     bg="#34495E", 
                                     fg="white", 
                                     justify=tk.LEFT, 
                                     wraplength=500)
                slide_label.pack(anchor="w")

            slides_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        else:
            no_slides_label = tk.Label(preview_container, 
                                     text="No hay diapositivas disponibles", 
                                     font=("Helvetica", 14), 
                                     bg="#2C3E50", 
                                     fg="#E74C3C")
            no_slides_label.pack(pady=20)

        if 'slides' in song_data:
            slides_formatted = [{'text': slide} for slide in song_data['slides']]
            sm.load_slides(slides_formatted)

    def update_projection(self):
        if self.second_window is None or not tk.Toplevel.winfo_exists(self.second_window):
            return
            
        current_slide = sm.get_current_slide()
        if current_slide and 'text' in current_slide:
            self.projection_label.config(text=current_slide['text'])
        else:
            self.projection_label.config(text="")
    
    def next_slide(self):
        sm.next_slide()
        self.update_projection()
    
    def previous_slide(self):
        sm.previous_slide()
        self.update_projection()

    def clear_screen(self):
        self.projection_label.config(text="")
        
    def clear(self):
        self.clear_screen()
            
    def run(self):
        self.open_second_window()
        self.root.mainloop()