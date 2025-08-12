import os
import tkinter as tk
from tkinter import ttk, messagebox
from yt_dlp import YoutubeDL


def download():
    url = url_entry.get().strip()
    quality = quality_combo.get()

    if not url:
        messagebox.showwarning("Thiếu URL", "Vui lòng nhập URL video YouTube.")
        return

    ydl_opts = {
        'format': quality,
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [hook],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    }

    if USE_COOKIES:
        ydl_opts['cookiefile'] = 'cookies.txt'

    try:
        status_label.config(text="⏳ Đang tải...")
        root.update()

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_label.config(text="✅ Tải xong!")
        messagebox.showinfo("Hoàn tất", "Video đã được tải thành công.")
    except Exception as e:
        status_label.config(text="❌ Lỗi khi tải.")
        messagebox.showerror("Lỗi", str(e))

def hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        status_label.config(text=f"Đang tải: {percent}")
        root.update()
    elif d['status'] == 'finished':
        status_label.config(text="🔄 Đang xử lý...")

# GUI
root = tk.Tk()
root.title("SnapYouTube")
root.geometry("420x230")
root.resizable(False, False)

tk.Label(root, text="🔗 Dán link YouTube:").pack(pady=5)
url_entry = tk.Entry(root, width=55)
url_entry.pack()

tk.Label(root, text="📺 Chọn chất lượng:").pack(pady=5)
quality_combo = ttk.Combobox(root, values=[
    "bestvideo+bestaudio/best",
    "best",
    "worst",
    "bestaudio",
    "worstaudio",
    "18",  # 360p
    "22",  # 720p
])
quality_combo.set("bestvideo+bestaudio/best")
quality_combo.pack()

tk.Button(root, text="⬇️ Tải video", command=download).pack(pady=10)
status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

root.mainloop()

