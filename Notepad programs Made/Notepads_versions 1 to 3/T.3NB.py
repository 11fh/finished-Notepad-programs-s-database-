import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from pygments.lexers import get_lexer_by_name
from pygments import highlight
import json

class SyntaxHighlightingNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Highlighting Notepad")
        self.text_area = ScrolledText(root, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill='both')

        # Load syntax highlighting rules from JSON files
        self.syntax_rules = {}
        self.load_syntax_rules('python.json')
        self.load_syntax_rules('html.json')

        # Binding Ctrl keys to functions
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-a>', self.select_all)
        self.root.bind('<Control-c>', self.copy_text)
        self.root.bind('<Control-x>', self.cut_text)
        self.root.bind('<Control-v>', self.paste_text)
        self.root.bind('<Control-z>', self.undo)

    def load_syntax_rules(self, filename):
        try:
            with open(filename, 'r') as file:
                language = filename.split('.')[0]
                self.syntax_rules[language] = json.load(file)
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", f"Syntax rules file '{filename}' not found.")

    def save_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                text_content = self.text_area.get('1.0', 'end-1c')
                file.write(text_content)
            messagebox.showinfo("Success", "File saved successfully.")

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete('1.0', 'end')
                self.text_area.insert('1.0', file.read())
            self.highlight_syntax()

    def highlight_syntax(self):
        content = self.text_area.get('1.0', 'end-1c')
        lexer = self.get_lexer()
        highlighted_code = highlight(content, lexer, self.get_formatter())
        self.text_area.tag_configure('code', font=('Courier New', 10))
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', highlighted_code)

    def get_lexer(self):
        content = self.text_area.get('1.0', 'end-1c')
        for language, rules in self.syntax_rules.items():
            for rule in rules:
                if rule['pattern'] in content:
                    return get_lexer_by_name(language)
        return get_lexer_by_name('text')

    def get_formatter(self):
        return 'raw'

    def select_all(self, event=None):
        self.text_area.tag_add('sel', '1.0', 'end')

    def copy_text(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_area.selection_get())

    def cut_text(self, event=None):
        self.copy_text()
        self.text_area.delete('sel.first', 'sel.last')

    def paste_text(self, event=None):
        self.text_area.insert('insert', self.root.clipboard_get())

    def undo(self, event=None):
        self.text_area.edit_undo()

if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlightingNotepad(root)
    root.mainloop()
