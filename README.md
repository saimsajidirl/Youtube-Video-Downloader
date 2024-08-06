# Youtube-Video-Downloader

Overview
The YoutubeDownloader class provides a graphical user interface (GUI) for downloading YouTube videos. It uses the tkinter library for the GUI, pytube for fetching video data and downloading, and PIL (Pillow) for handling video thumbnails. The class includes features for fetching video information, selecting video quality, and downloading the video to a specified location.

Dependencies
tkinter: For creating the GUI.
ttkthemes: For applying a custom theme to the GUI.
pytube: For fetching and downloading YouTube videos.
threading: For running background tasks.
os: For interacting with the file system.
re: For regular expression operations.
PIL (Pillow): For image processing and displaying thumbnails.
requests: For downloading the video thumbnail.
io: For handling image data in memory.
time: For formatting video duration.
Initialization
__init__(self, master)
Initializes the YoutubeDownloader class.

Parameters:
master: The main Tkinter window.
Attributes:
self.master: The main window of the application.
self.style: The themed style for the application.
self.bg_color, self.fg_color, self.accent_color: Custom colors for the GUI.
self.main_frame, self.info_frame, self.download_frame: Frames to organize widgets.
self.url_entry, self.fetch_btn, self.fetch_progress_bar, self.title_label, self.duration_label, self.views_label, self.quality_combo, self.format_combo, self.download_btn, self.progress_bar, self.status_label: Widgets for user interaction.
Methods
create_widgets(self)
Creates and arranges the widgets in the main window.

Widgets Created:
URL entry field and fetch button.
Progress bars for fetching video information and downloading.
Labels for displaying video information (title, duration, views).
Dropdowns for selecting video quality and format.
Download button and status label.
create_menu(self)
Creates the application menu with options for opening the download folder and viewing the About dialog.

Menu Items:
File: Open Download Folder, Exit.
Help: About.
fetch_video(self)
Handles the process of fetching video information from YouTube.

Actions:
Retrieves URL from the entry field.
Shows a progress bar while fetching.
Starts a background thread to fetch video data.
_fetch_video_thread(self, url)
Background thread method for fetching video information.

Parameters:
url: The YouTube video URL.
Actions:
Uses pytube to get video details.
Updates the GUI with video information or shows an error if fetching fails.
_update_video_info(self, yt)
Updates the GUI with video details.

Parameters:
yt: The pytube.YouTube object.
Actions:
Updates labels with video title, duration, and views.
Fetches and displays the video thumbnail.
Populates the quality dropdown with available video streams.
_fetch_thumbnail(self, url)
Fetches the video thumbnail image.

Parameters:
url: The URL of the thumbnail image.
Actions:
Downloads and processes the thumbnail image.
Updates the thumbnail label in the GUI.
_update_thumbnail(self, photo)
Updates the GUI with the fetched thumbnail.

Parameters:
photo: The ImageTk.PhotoImage object.
Actions:
Sets the image on the thumbnail label.
_show_fetch_error(self, error_message)
Shows an error message if fetching video information fails.

Parameters:
error_message: The error message to display.
_finish_fetch(self)
Finalizes the fetching process by stopping the progress bar and re-enabling the fetch button.

start_download(self)
Starts the video download process.

Actions:
Validates video selection and quality.
Opens a file dialog for the user to choose the save location.
Starts a background thread to download the video.
_download_thread(self, stream, save_path)
Background thread method for downloading the video.

Parameters:
stream: The pytube.Stream object for the selected video quality.
save_path: The path to save the downloaded video.
Actions:
Downloads the video and updates the progress bar.
_download_complete(self)
Handles the completion of the video download.

Actions:
Updates the status label and shows a success message.
_download_failed(self, error_message)
Handles download failures.

Parameters:
error_message: The error message to display.
update_progress(self, chunk, file_handle, bytes_remaining)
Updates the download progress.

Parameters:
chunk: The current chunk of data.
file_handle: The file being written to.
bytes_remaining: The number of bytes remaining to download.
open_download_folder(self)
Opens the default download folder.

show_about(self)
Displays an About dialog with information about the application.

Usage
To use this application, run the script directly. It will open a window where you can:

Enter a YouTube URL and click "Fetch" to retrieve video information.
Select the desired quality and format from the dropdowns.
Click "Download" to save the video to your chosen location.
