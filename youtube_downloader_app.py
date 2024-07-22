import tkinter as tk
import customtkinter as ctk
from pytubefix import YouTube
import os

# Configurar apariencia
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class YoutubeDownloaderApp(ctk.CTk):
    APP_NAME = "Youtube Downloader App"
    WIDTH = 650
    HEIGHT = 350

    def __init__(self):
        super().__init__()
        self.title(YoutubeDownloaderApp.APP_NAME)
        self.geometry(f"{YoutubeDownloaderApp.WIDTH}x{YoutubeDownloaderApp.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)
        self.create_widgets()

    def create_widgets(self):
        self.url = ctk.StringVar()
        self.resolution = ctk.StringVar(value="720p")
        
        ctk.CTkLabel(master=self, text="Descarga Videos de YouTube", font=(None,25)).pack(padx=10, pady=30)
        ctk.CTkEntry(master=self, width=500, textvariable=self.url).pack(padx=10, pady=2)
        ctk.CTkSegmentedButton(master=self, values=["720p", "480p", "360p"], command=self.segmented_button_callback, variable=self.resolution).pack(padx=10, pady=10)
        
        self.label_message = ctk.CTkLabel(master=self, text="")
        self.label_message.pack(padx=10, pady=2)
        
        self.progress_bar = ctk.CTkProgressBar(master=self, width=300)
        self.progress_bar.pack(padx=10, pady=2)
        self.progress_bar.set(0)

        ctk.CTkButton(master=self, text="Descargar", command=self.download_video).pack(padx=10, pady=15)

    def segmented_button_callback(self, value):
        print("segmented button clicked:", value)

    def download_video(self):
        try:
            self.progress_bar.set(0)
            self.label_message.configure(text="")

            url = self.url.get().strip()
            print(f"URL ingresada: {url}")
            yt = YouTube(url, on_progress_callback=self.on_progress)
            video = yt.streams.get_highest_resolution()
            # Crear la carpeta 'videos' si no existe
            download_folder = 'videos'
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            # Descargar el video en la carpeta 'videos'
            video.download(output_path=download_folder)
        except Exception as e:
            self.label_message.configure(text=f"Error {e}")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = int(bytes_downloaded / total_size * 100)
        if percentage_of_completion != 100:
            self.label_message.configure(text=f"{percentage_of_completion}%")
        else:
            self.label_message.configure(text="Descarga completada!")

        self.progress_bar.set(percentage_of_completion/100)
        self.label_message.update()

if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.mainloop()