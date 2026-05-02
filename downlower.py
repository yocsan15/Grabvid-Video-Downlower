import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import os

# ↓ Cambia esta ruta por la tuya
FFMPEG_PATH = r'C:\ffmpeg-master-latest-win64-gpl-shared\bin'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("600x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.output_dir = os.path.expanduser("~\\Downloads")
        self._build_ui()

    def _build_ui(self):
        BG = "#1e1e2e"
        CARD = "#2a2a3e"
        ACCENT = "#7c3aed"
        TEXT = "#e2e8f0"
        MUTED = "#94a3b8"
        ENTRY_BG = "#13131f"

        # Título
        tk.Label(self.root, text="Video Downloader", font=("Segoe UI", 18, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(24, 4))
        tk.Label(self.root, text="Descarga videos en máxima calidad",
                 font=("Segoe UI", 10), bg=BG, fg=MUTED).pack(pady=(0, 20))

        # Card principal
        card = tk.Frame(self.root, bg=CARD, padx=24, pady=20)
        card.pack(fill="x", padx=28)

        # URL
        tk.Label(card, text="URL del video", font=("Segoe UI", 9, "bold"),
                 bg=CARD, fg=MUTED).pack(anchor="w")
        self.url_entry = tk.Entry(card, font=("Segoe UI", 11), bg=ENTRY_BG,
                                  fg=TEXT, insertbackground=TEXT, relief="flat",
                                  highlightthickness=1, highlightbackground="#3f3f5a",
                                  highlightcolor=ACCENT)
        self.url_entry.pack(fill="x", pady=(4, 14), ipady=8)

        # Formato
        tk.Label(card, text="Formato", font=("Segoe UI", 9, "bold"),
                 bg=CARD, fg=MUTED).pack(anchor="w")
        self.format_var = tk.StringVar(value="MP4 (máxima calidad)")
        formats = ["MP4 (máxima calidad)", "MP4 720p", "MP4 480p", "Solo audio MP3"]
        self.format_box = ttk.Combobox(card, textvariable=self.format_var,
                                       values=formats, state="readonly",
                                       font=("Segoe UI", 10))
        self.format_box.pack(fill="x", pady=(4, 14))

        # Carpeta destino
        tk.Label(card, text="Carpeta de destino", font=("Segoe UI", 9, "bold"),
                 bg=CARD, fg=MUTED).pack(anchor="w")
        dir_frame = tk.Frame(card, bg=CARD)
        dir_frame.pack(fill="x", pady=(4, 0))
        self.dir_label = tk.Label(dir_frame, text=self.output_dir, font=("Segoe UI", 9),
                                  bg=ENTRY_BG, fg=MUTED, anchor="w",
                                  highlightthickness=1, highlightbackground="#3f3f5a")
        self.dir_label.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        tk.Button(dir_frame, text="Cambiar", font=("Segoe UI", 9), bg=CARD,
                  fg=TEXT, relief="flat", cursor="hand2",
                  command=self.choose_dir).pack(side="right", ipadx=10, ipady=4)

        # Botón descargar
        self.btn = tk.Button(self.root, text="Descargar", font=("Segoe UI", 11, "bold"),
                             bg=ACCENT, fg="white", relief="flat", cursor="hand2",
                             activebackground="#6d28d9", activeforeground="white",
                             command=self.start_download)
        self.btn.pack(fill="x", padx=28, pady=(16, 8), ipady=10)

        # Progreso
        self.progress = ttk.Progressbar(self.root, mode="indeterminate")
        self.progress.pack(fill="x", padx=28)

        # Status
        self.status_var = tk.StringVar(value="Listo para descargar")
        tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 9),
                 bg=BG, fg=MUTED).pack(pady=(8, 0))

    def choose_dir(self):
        d = filedialog.askdirectory(initialdir=self.output_dir)
        if d:
            self.output_dir = d
            self.dir_label.config(text=d)

    def get_format_string(self):
        f = self.format_var.get()
        if f == "MP4 (máxima calidad)":
            return "bestvideo+bestaudio/best"
        elif f == "MP4 720p":
            return "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif f == "MP4 480p":
            return "bestvideo[height<=480]+bestaudio/best[height<=480]"
        elif f == "Solo audio MP3":
            return "bestaudio/best"

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("URL vacía", "Por favor ingresa la URL del video.")
            return
        self.btn.config(state="disabled")
        self.progress.start()
        self.status_var.set("Descargando...")
        threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def download(self, url):
        fmt = self.get_format_string()
        is_audio = "MP3" in self.format_var.get()

        opts = {
            'format': fmt,
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'ffmpeg_location': FFMPEG_PATH,
            'noplaylist': True,
            'progress_hooks': [self.progress_hook],
        }

        if is_audio:
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            opts['merge_output_format'] = 'mp4'

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            self.root.after(0, self.on_success)
        except Exception as e:
            self.root.after(0, lambda: self.on_error(str(e)))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '').strip()
            self.root.after(0, lambda: self.status_var.set(f"Descargando... {p}"))

    def on_success(self):
        self.progress.stop()
        self.btn.config(state="normal")
        self.status_var.set("✓ Descarga completa")
        messagebox.showinfo("Listo", f"Video guardado en:\n{self.output_dir}")

    def on_error(self, msg):
        self.progress.stop()
        self.btn.config(state="normal")
        self.status_var.set("Error en la descarga")
        messagebox.showerror("Error", msg)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()