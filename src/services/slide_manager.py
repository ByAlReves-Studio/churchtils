from typing import List, Dict, Any
import os
from pathlib import Path

class SlideManager:
    def __init__(self):
        self.current_slide = 0
        self.slides: List[Dict[str, Any]] = []
        self.total_slides = 0

    def load_slides(self, slides_data: List[Dict[str, Any]]) -> None:
        """Carga la lista de slides"""
        if not slides_data:
            self.slides = []
            self.total_slides = 0
            self.current_slide = 0
            return
            
        self.current_slide = 0
        self.slides = slides_data
        self.total_slides = len(slides_data)

    def get_current_slide(self) -> Dict[str, Any]:
        """Obtiene el slide actual"""
        if 0 <= self.current_slide < self.total_slides:
            return self.slides[self.current_slide]
        return {}

    def next_slide(self) -> Dict[str, Any]:
        """Avanza al siguiente slide"""
        if self.current_slide < self.total_slides - 1:
            self.current_slide += 1
        return self.get_current_slide()

    def previous_slide(self) -> Dict[str, Any]:
        """Retrocede al slide anterior"""
        if self.current_slide > 0:
            self.current_slide -= 1
        return self.get_current_slide()

    def goto_slide(self, index: int) -> Dict[str, Any]:
        """Va a un slide específico por índice"""
        if 0 <= index < self.total_slides:
            self.current_slide = index
        return self.get_current_slide()

    def get_total_slides(self) -> int:
        """Retorna el número total de slides"""
        return self.total_slides

    def get_current_index(self) -> int:
        """Retorna el índice actual"""
        return self.current_slide