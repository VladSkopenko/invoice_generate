# Перенесено

import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class FontManager:
    def __init__(self):
        self.fonts_registered = False
        self.fonts_dir = "fonts"
        self.font_files = {
            "Times": "TIMES.TTF",
            "Times-Bold": "TIMESBD.TTF",
            "Times-Italic": "TIMESI.TTF",
            "Times-BoldItalic": "TIMESBI.TTF",
        }

    def register_times_fonts(self):
        if self.fonts_registered:
            return

        for font_name, font_file in self.font_files.items():
            font_path = os.path.join(self.fonts_dir, font_file)
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(font_name, font_path))


        self.fonts_registered = True

    def is_font_available(self, font_name: str) -> bool:
        try:
            pdfmetrics.getFont(font_name)
            return True
        except:
            return False 