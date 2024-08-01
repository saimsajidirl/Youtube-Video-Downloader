from os.path import expanduser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube, exceptions as pytube_exceptions
from threading import Thread

class YouTubeDownloader:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.setup_gui()

    def setup_gui(self):
        self.root.title("YouTube Downloader")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")

        self.label1 = ttk.Label(frame, text="Enter The Link Of The Video You Want To Download:")
        self.label1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.entry1 = ttk.Entry(frame)
        self.entry1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.detect_quality_button = ttk.Button(frame, text="Detect Quality", command=self.detect_quality)
        self.detect_quality_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.label2 = ttk.Label(frame, text="Select Download Quality:")
        self.label2.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.download_options = ttk.Combobox(frame)
        self.download_options.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.button1 = ttk.Button(frame, text="Browse", command=self.browse_location)
        self.button1.grid(row=5, column=0, padx=10, pady=10)

        self.button2 = ttk.Button(frame, text="Download", command=self.download_video)
        self.button2.grid(row=5, column=1, padx=10, pady=10)

        self.progress_label = ttk.Label(frame, text="Download Progress:")
        self.progress_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.percentage_label = ttk.Label(frame, text="")
        self.percentage_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.label3 = ttk.Label(frame, text="Enter File Name:")
        self.label3.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.entry_file_name = ttk.Entry(frame)
        self.entry_file_name.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        self.entry1.bind("<FocusOut>", self.detect_quality)

        self.download_path = expanduser("~") + "/Desktop"
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - self.root.winfo_reqwidth()) // 2
        y_coordinate = (screen_height - self.root.winfo_reqheight()) // 2
        self.root.geometry("+{}+{}".format(x_coordinate, y_coordinate))

    def browse_location(self):
        self.download_path = filedialog.askdirectory()

    def is_valid_link(self, link):
        if not link.strip():
            return False
        try:
            YouTube(link)
            return True
        except pytube_exceptions.RegexMatchError:
            return False

    def detect_quality(self, event=None):
        link = self.entry1.get()

        if not self.is_valid_link(link):
            if link.strip():
                messagebox.showerror("Error", "Invalid YouTube link.")
            return

        # Run detect_quality in a separate thread
        Thread(target=self.detect_quality_worker, args=(link,)).start()

    def detect_quality_worker(self, link):
        try:
            videodown = YouTube(link)
            available_qualities = [stream.resolution for stream in videodown.streams.filter(progressive=True)]
            self.root.after(0, self.update_quality_options, available_qualities)
        except pytube_exceptions.RegexMatchError:
            self.root.after(0, self.show_error_message, "Invalid YouTube link.")

    def update_quality_options(self, available_qualities):
        self.download_options['values'] = available_qualities

        if available_qualities:
            self.download_options.set(available_qualities[0])  # Set the default quality
        else:
            messagebox.showinfo("Info", "No progressive download options available.")

    def download_video(self):
        link = self.entry1.get()

        # Run download_video in a separate thread
        Thread(target=self.download_video_worker, args=(link,)).start()

    def download_video_worker(self, link):
        try:
            videodown = YouTube(link,
                                on_progress_callback=lambda stream, chunk, remaining: self.download_progress(stream, chunk,
                                                                                                               remaining,
                                                                                                               self.percentage_label))

            video = videodown.streams.filter(progressive=True, resolution=self.download_options.get()).first()

            if not video:
                self.root.after(0, self.show_error_message, "No download options available for the selected quality.")
                return

            file_name = self.entry_file_name.get().strip()

            if not file_name:
                file_name = "video"

            file_name += ".mp4"

            print(f"Downloading: {video.title}")
            video.download(output_path=self.download_path, filename=file_name)
            print("Video Downloaded Successfully")
            self.root.after(0, self.show_download_complete_message)

        except Exception as e:
            self.root.after(0, self.show_error_message, str(e))

    def download_progress(self, stream, chunk, remaining, percentage_label):
        total_size = stream.filesize
        bytes_downloaded = total_size - remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_bar['value'] = percentage
        percentage_label["text"] = f"{percentage:.1f}%"

    def show_download_complete_message(self):
        messagebox.showinfo("Download Complete", "Video Downloaded Successfully")
        self.progress_bar['value'] = 0
        self.percentage_label["text"] = ""

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    youtubedownloader = YouTubeDownloader()
    youtubedownloader.run()
