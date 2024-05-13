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

        # Load syntax highlighting rules from JSON strings
        self.syntax_rules = {
            'python': json.loads("""
                [
                    {
                        "pattern": "def|class|if|else|elif|while|for|try|except|finally|with|as|import|from|return",
                        "style": "bold #0000FF"
                    },
                    {
                        "pattern": "#.*$",
                        "style": "italic #008000"
                    }
                ]
            """),
            'html': json.loads("""
                [
                    {
                        "pattern": "<([A-Za-z][A-Za-z0-9]*)\\b[^>]*>",
                        "style": "bold #0000FF"
                    },
                    {
                        "pattern": "(\\b[A-Za-z0-9-]+=\\".*?\\")",
                        "style": "italic #008000"
                    }
                ]
            """)
        }

        # Create menus
        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)

        # Add commands to File menu
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Add commands to Edit menu
        self.edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)

        # Add File and Edit menus to menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Binding Ctrl keys to functions
        self.root.bind('<Control-n>', self.new_file)
        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-a>', self.select_all)
        self.root.bind('<Control-c>', self.copy_text)
        self.root.bind('<Control-x>', self.cut_text)
        self.root.bind('<Control-v>', self.paste_text)
        self.root.bind('<Control-z>', self.undo)

        # Configure root menu
        self.root.config(menu=self.menu_bar)

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

    def new_file(self, event=None):
        self.text_area.delete('1.0', 'end')

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
