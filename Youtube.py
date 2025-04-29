#Youtube Video Downloader with GUI

#Youtube Video Downloader

# This line brings in a tool called 'pytubefix' so we can grab YouTube videos
import tkinter as tk
from pytubefix import YouTube  # This lets us work with YouTube videos

# This is a special function that will help us download the video
def Download_Video():
   try:
       # We take the link the user typed and tell the program it's a YouTube video
       url = YouTube(str(yourlink.get()))  # The program looks at the link to know what video to download

       # We pick the best quality video (the highest resolution) that we can
       video = url.streams.get_highest_resolution()  # Choose the best quality video

       # Now, we download the video to the computer
       video.download()  # The video gets saved to the computer

       # We show a message to say the video was successfully downloaded
       tk.Label(root, text='Your Video is downloaded!', font='arial 15', fg="White", bg="#EC7063").place(x=10, y=140)

   except Exception as e:
       # If something goes wrong, we show an error message
       tk.Label(root, text=f'Error: {str(e)}', font='arial 15', fg="White", bg="#EC7063").place(x=10, y=140)

# This is the main part where we make the window that shows up
root = tk.Tk()  # This is like creating a new blank paper to draw on
root.geometry("600x200")  # We set how big the window is (600 wide, 200 tall)
root.config(bg="#EC7063")  # We give the window a pretty background color
root.resizable(0, 0)  # We tell the window not to change size
root.title('YouTube Video Downloader')  # We give the window a title so we know what it does

# This is where we store the link the user types
yourlink = tk.StringVar()  # It's like a box where we keep the YouTube link

# This line writes a big title on the window that says what the program does
tk.Label(root, text='                   Youtube Video Downloader                    ', font='arial 20 bold',
        fg="White", bg="Black").pack()  # This creates the title label

# This line tells the user to put their YouTube link in the box below
tk.Label(root, text='                   Put your youtube link below                    ', font='arial 20 bold',
        fg="White", bg="purple").pack()  # This creates the instructions label

# This is the space where the user types the YouTube link
link_enter = tk.Entry(root, width=53, textvariable=yourlink, font='arial 15 bold', bg="lightgreen").place(x=5, y=100)  # The place to type the link

# This is the button that starts the download when you click it
tk.Button(root, text='DOWNLOAD VIDEO', font='arial 15 bold', fg="white", bg='black', padx=2,
         command=Download_Video).place(x=385, y=140)  # When you click, the download starts

# This line starts the program and shows the window to the user
root.mainloop()  # This makes everything show up and run forever until you close it