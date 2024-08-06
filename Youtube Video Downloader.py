import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkthemes
import pytube
import threading
import os
import re
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time

class YoutubeDownloader:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Downloader Pro")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        
        self.style = ttkthemes.ThemedStyle(self.master)
        self.style.set_theme("equilux")

        self.bg_color = "#2E2E2E"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#FF0000"

        self.master.configure(bg=self.bg_color)

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
      
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

       
        self.url_label = ttk.Label(self.main_frame, text="YouTube URL:", foreground=self.fg_color)
        self.url_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.url_entry = ttk.Entry(self.main_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=(0, 10), pady=(0, 10))
        self.fetch_btn = ttk.Button(self.main_frame, text="Fetch", command=self.fetch_video)
        self.fetch_btn.grid(row=0, column=2, pady=(0, 10))

      
        self.fetch_progress_var = tk.DoubleVar()
        self.fetch_progress_bar = ttk.Progressbar(self.main_frame, variable=self.fetch_progress_var, maximum=100, mode='indeterminate')
        self.fetch_progress_bar.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        self.fetch_progress_bar.grid_remove()  
       
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Video Information", padding="10")
        self.info_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 10))

        self.thumbnail_label = ttk.Label(self.info_frame)
        self.thumbnail_label.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        self.title_label = ttk.Label(self.info_frame, text="Title: ", foreground=self.fg_color)
        self.title_label.grid(row=0, column=1, sticky="w")

       
        self.duration_label = ttk.Label(self.info_frame, text="Duration: ", foreground=self.fg_color)
        self.duration_label.grid(row=1, column=1, sticky="w")

      
        self.views_label = ttk.Label(self.info_frame, text="Views: ", foreground=self.fg_color)
        self.views_label.grid(row=2, column=1, sticky="w")

    
        self.download_frame = ttk.LabelFrame(self.main_frame, text="Download Options", padding="10")
        self.download_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 10))

     
        self.quality_label = ttk.Label(self.download_frame, text="Quality:", foreground=self.fg_color)
        self.quality_label.grid(row=0, column=0, sticky="w")
        self.quality_combo = ttk.Combobox(self.download_frame, state="readonly", width=30)
        self.quality_combo.grid(row=0, column=1, padx=(0, 10))

       
        self.format_label = ttk.Label(self.download_frame, text="Format:", foreground=self.fg_color)
        self.format_label.grid(row=0, column=2, sticky="w")
        self.format_combo = ttk.Combobox(self.download_frame, state="readonly", width=10)
        self.format_combo.grid(row=0, column=3)

      
        self.download_btn = ttk.Button(self.main_frame, text="Download", command=self.start_download)
        self.download_btn.grid(row=4, column=0, columnspan=3, pady=(0, 10))

      
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 10))

       
        self.status_label = ttk.Label(self.main_frame, text="", foreground=self.fg_color)
        self.status_label.grid(row=6, column=0, columnspan=3)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Download Folder", command=self.open_download_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def fetch_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        self.status_label.config(text="Fetching video information...")
        self.fetch_progress_bar.grid()  
        self.fetch_progress_bar.start(10)  
        self.fetch_btn.config(state="disabled")  
        
        threading.Thread(target=self._fetch_video_thread, args=(url,), daemon=True).start()

    def _fetch_video_thread(self, url):
        try:
            yt = pytube.YouTube(url)
            self.current_video = yt

            self.master.after(0, self._update_video_info, yt)
        except Exception as e:
            self.master.after(0, self._show_fetch_error, str(e))
        finally:
            self.master.after(0, self._finish_fetch)

    def _update_video_info(self, yt):
        self.title_label.config(text=f"Title: {yt.title}")
        self.duration_label.config(text=f"Duration: {time.strftime('%H:%M:%S', time.gmtime(yt.length))}")
        self.views_label.config(text=f"Views: {yt.views:,}")

 
        threading.Thread(target=self._fetch_thumbnail, args=(yt.thumbnail_url,), daemon=True).start()

        streams = yt.streams.filter(progressive=True)
        qualities = list(set([f"{s.resolution} ({s.mime_type.split('/')[1]})" for s in streams]))
        self.quality_combo['values'] = qualities
        if qualities:
            self.quality_combo.set(qualities[0])

        self.status_label.config(text="Video information fetched successfully")

    def _fetch_thumbnail(self, url):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.thumbnail((150, 150))
            photo = ImageTk.PhotoImage(img)
            self.master.after(0, self._update_thumbnail, photo)
        except Exception as e:
            print(f"Error fetching thumbnail: {e}")

    def _update_thumbnail(self, photo):
        self.thumbnail_label.config(image=photo)
        self.thumbnail_label.image = photo

    def _show_fetch_error(self, error_message):
        messagebox.showerror("Error", error_message)
        self.status_label.config(text="Failed to fetch video information")

    def _finish_fetch(self):
        self.fetch_progress_bar.stop()  
        self.fetch_progress_bar.grid_remove()  
        self.fetch_btn.config(state="normal")  

    def start_download(self):
        if not hasattr(self, 'current_video'):
            messagebox.showerror("Error", "Please fetch a video first")
            return

        quality = self.quality_combo.get()
        if not quality:
            messagebox.showerror("Error", "Please select a quality")
            return

        try:
            resolution, format_ = re.match(r"(\d+p) \((\w+)\)", quality).groups()
        except AttributeError:
            messagebox.showerror("Error", "Invalid quality format selected")
            return

        stream = self.current_video.streams.filter(progressive=True, resolution=resolution, file_extension=format_).first()

        if not stream:
            messagebox.showerror("Error", "No stream found for the selected quality")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=f".{format_}", filetypes=[("All Files", "*.*")])
        if not save_path:
            return

        self.status_label.config(text="Downloading...")
        self.progress_var.set(0)
        threading.Thread(target=self._download_thread, args=(stream, save_path), daemon=True).start()

    def _download_thread(self, stream, save_path):
        try:

            stream.download(filename=save_path, on_progress_callback=self.update_progress)
            self.master.after(0, self._download_complete)
        except Exception as e:
            self.master.after(0, self._download_failed, str(e))

    def _download_complete(self):
        self.status_label.config(text="Download completed successfully")
        messagebox.showinfo("Success", "Video downloaded successfully")

    def _download_failed(self, error_message):
        messagebox.showerror("Error", error_message)
        self.status_label.config(text="Download failed")

    def update_progress(self, chunk, file_handle, bytes_remaining):
        total_size = self.current_video.streams.first().filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.master.after(0, self.progress_var.set, percentage)

    def open_download_folder(self):
        download_path = os.path.expanduser("~/Downloads")
        os.startfile(download_path)

    def show_about(self):
        about_text = "YouTube Downloader Pro\nVersion 1.0\n\nCreated by Your Name\n\nThis application allows you to download YouTube videos with ease."
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloader(root)
    root.mainloop()
