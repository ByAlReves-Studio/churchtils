import json
import os
from typing import List, Dict, Any
from tkinter import filedialog

class ImportFromJson:
  """Clase para importar datos desde archivos JSON."""
    
  @staticmethod
  def import_from_json() -> List[Dict[str, Any]]:
      """
      Importa datos desde un archivo JSON.
        
      Returns:
          List[Dict[str, Any]]: Lista de diccionarios con los datos importados
            
      Raises:
          ValueError: Si el archivo JSON no contiene datos válidos
      """
      # Asegurar que existe el directorio data
      if not os.path.exists('data'):
          os.makedirs('data')
            
      file_path = filedialog.askopenfilename(
          filetypes=[("Archivos JSON", "*.json")]
      )
        
      if not file_path:
          raise ValueError("No se seleccionó ningún archivo.")
            
      with open(file_path, 'r', encoding='utf-8') as file:
          data = json.load(file)
            
          # Validar que sea una lista
          if not isinstance(data, list):
              raise ValueError("El archivo JSON debe contener una lista de canciones.")
                
          result = []
          for song in data:
              # Validar la estructura necesaria
              if not isinstance(song, dict):
                  continue
                    
              lyrics = song.get('lyrics', {})
              if not isinstance(lyrics, dict):
                  continue
                    
              paragraphs = lyrics.get('paragraphs', [])
              if not isinstance(paragraphs, list):
                  continue
                    
              # Crear objeto de canción con título y artista
              song_data = {
                  'title': song.get('title', ''),
                  'artist': song.get('artist', ''),
                  'slides': []
              }
                
              # Validar que cada párrafo tenga el texto necesario
              for paragraph in paragraphs:
                  if isinstance(paragraph, dict) and 'text' in paragraph:
                      song_data['slides'].append(paragraph['text'])
                        
              if song_data['slides']:
                  result.append(song_data)
                  
              # Guardar los datos en el archivo JSON existente o crear uno nuevo
              output_path = os.path.join('data', 'lyrics.json')
              try:
                with open(output_path, 'r', encoding='utf-8') as existing_file:
                    existing_data = json.load(existing_file)
                    result.extend(existing_data)
              except (FileNotFoundError, json.JSONDecodeError):
                pass
                
              with open(output_path, 'w', encoding='utf-8') as output_file:
                json.dump(result, output_file, ensure_ascii=False, indent=2)
                  
            
          if not result:
              raise ValueError("El archivo JSON no contiene datos válidos o el formato es incorrecto.")
                
          return result