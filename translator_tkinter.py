import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Простой переводчик [fq-хай")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.translation_map = {}
        self.load_base_file()
        self.create_widgets()
        
    def load_base_file(self):
        try:
            base_file = "base.txt"
            if not os.path.exists(base_file):
                messagebox.showerror("Ошибка", f"Файл {base_file} не найден!")
                return
                
            with open(base_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '-' in line:
                        parts = line.split('-', 1)
                        if len(parts) == 2:
                            from_char, to_char = parts
                            self.translation_map[from_char] = to_char
                            
            if not self.translation_map:
                messagebox.showwarning("Предупреждение", "Файл base.txt пуст или содержит некорректные данные")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл base.txt: {e}")
            
    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Текст для перевода:").pack(anchor=tk.W, pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(top_frame, height=8, width=1, font=("Arial", 11))
        self.input_text.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Копировать", command=self.copy_text).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Вставить", command=self.paste_text).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Очистить", command=self.clear_text).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Поменять местами", command=self.swap_text).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(top_frame, text="Результат перевода:").pack(anchor=tk.W, pady=(10, 5))
        
        self.output_text = scrolledtext.ScrolledText(top_frame, height=8, width=1, font=("Arial", 11))
        self.output_text.pack(fill=tk.X, pady=(0, 10))
        
        self.status_var = tk.StringVar()
        self.status_var.set(f"Загружено {len(self.translation_map)} символов для перевода")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.root.bind('<Control-Return>', lambda e: self.translate_text())
        self.root.bind('<Control-l>', lambda e: self.clear_text())
        self.root.bind('<Control-s>', lambda e: self.swap_text())
        
        self.input_text.bind('<KeyRelease>', self.on_text_change)
        self.input_text.bind('<Button-1>', self.on_text_change)
        
    def translate_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        
        if not input_text:
            self.output_text.delete("1.0", tk.END)
            return
            
        translated = self.translate_string(input_text)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, translated)
        
    def on_text_change(self, event=None):
        if hasattr(self, '_after_id'):
            self.root.after_cancel(self._after_id)
        
        self._after_id = self.root.after(100, self.translate_text)
        
    def translate_string(self, text):
        result = []
        for char in text:
            if char in self.translation_map:
                result.append(self.translation_map[char])
            elif char.lower() in self.translation_map:
                translated_char = self.translation_map[char.lower()]
                result.append(translated_char.upper() if char.isupper() else translated_char)
            else:
                result.append(char)
        return ''.join(result)
        
    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        
    def copy_text(self):
        output_text = self.output_text.get("1.0", tk.END).strip()
        if output_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            self.root.update()
            
    def paste_text(self):
        try:
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                self.input_text.insert(tk.INSERT, clipboard_text)
                self.on_text_change()
        except tk.TclError:
            pass
            
    def swap_text(self):
        input_content = self.input_text.get("1.0", tk.END).strip()
        output_content = self.output_text.get("1.0", tk.END).strip()
        
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, output_content)
        
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, input_content)

def main():
    root = tk.Tk()
    TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()