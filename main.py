from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import filechooser
from PIL import Image
import os

class ImgToPdfApp(App):
    def build(self):
        # إعدادات الشاشة الأساسية
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # نص توضيحي
        self.info_label = Label(text="Select an Image to convert to PDF", font_size='20sp', halign='center')
        self.layout.add_widget(self.info_label)
        
        # زر اختيار الصورة
        self.select_btn = Button(text="1. Select Image", font_size='22sp', size_hint=(1, 0.2), background_color=(0.2, 0.6, 1, 1))
        self.select_btn.bind(on_press=self.choose_file)
        self.layout.add_widget(self.select_btn)
        
        # زر التحويل (يكون معطلاً حتى نختار صورة)
        self.convert_btn = Button(text="2. Convert to PDF", font_size='22sp', size_hint=(1, 0.2), disabled=True)
        self.convert_btn.bind(on_press=self.convert_file)
        self.layout.add_widget(self.convert_btn)
        
        self.file_path = None
        return self.layout

    def choose_file(self, *args):
        try:
            # فتح معرض الصور
            filechooser.open_file(on_selection=self.handle_selection, filters=[("Image", "*.png", "*.jpg", "*.jpeg")])
        except Exception as e:
            self.info_label.text = "Error opening file manager!"

    def handle_selection(self, selection):
        if selection:
            self.file_path = selection[0]
            file_name = os.path.basename(self.file_path)
            self.info_label.text = f"Selected: {file_name}"
            # تفعيل زر التحويل بعد اختيار الصورة
            self.convert_btn.disabled = False
        else:
            self.info_label.text = "No file selected."

    def convert_file(self, *args):
        if self.file_path:
            try:
                self.info_label.text = "Converting to PDF..."
                image = Image.open(self.file_path)
                
                # تحويل ألوان الصورة لتتناسب مع صيغة PDF
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                
                # إنشاء مسار واسم ملف الـ PDF الجديد
                pdf_path = self.file_path.rsplit('.', 1)[0] + ".pdf"
                image.save(pdf_path, "PDF", resolution=100.0)
                
                self.info_label.text = f"Success!\nSaved at: {os.path.basename(pdf_path)}"
            except Exception as e:
                self.info_label.text = "Error during conversion!"

if __name__ == '__main__':
    ImgToPdfApp().run()
  
