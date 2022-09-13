from os import getcwd
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

def main():
    # create the TK root object
    root = tk.Tk()
    root.geometry("570x525")

    #initialize mixer 
    mixer.init()

    #create the main frame.
    frm_main = tk.Frame(root, bd=0, bg="gray10")
    frm_main.master.title("Music Player")
    frm_main.pack(fill=tk.BOTH, expand=1)

    populate_main_window(frm_main)

    root.mainloop()

def populate_main_window(frm_main):
    """Populate the main window of this program. In other words, put
    the labels, text entry boxes, and buttons into the main window.

    Parameter
        frm_main: the main frame (window)
    Return: nothing
    """
    # images
    global img_headphones
    global img_play_btn
    global img_pause_btn
    global img_next_btn
    global img_prev_btn
    img_headphones = tk.PhotoImage(file="images/headphones.png", format="png")
    img_play_btn = tk.PhotoImage(file="images/play-button.png", format="png")
    img_pause_btn = tk.PhotoImage(file="images/pause-button.png", format="png")
    img_next_btn = tk.PhotoImage(file="images/next-button.png", format="png")
    img_prev_btn = tk.PhotoImage(file="images/prev-button.png", format="png")

    # labels
    lbl_playin_from = tk.Label(frm_main, text="", fg="ivory2", bg="gray10")
    lbl_headphones = tk.Label(frm_main, image=img_headphones, bg="gray10", width=280, height=280)
    lbl_song = tk.Label(frm_main, text="We are the champions", fg="ivory2", bg="gray10", font="bold")
    lbl_now_playing = tk.Label(frm_main, text="Now playing", fg="ivory4", bg="gray10")

    # list box
    listbox_songs = tk.Listbox(frm_main, selectmode="single", bg="gray8", fg="ivory2", bd=0, highlightthickness=0, selectbackground="MediumPurple4", selectforeground="ivory2", width=36, height=28)

    # buttons
    btn_add_songs = tk.Button(frm_main, cursor="hand2", text="Add Songs", bd=0, fg="ivory3", bg="DarkOrchid4", width=33, highlightthickness=0, activeforeground="ivory4", activebackground="purple4")
    btn_play = tk.Button(frm_main, cursor="hand2", image=img_play_btn, bd=0, bg="gray10", highlightthickness=0, activebackground="gray10")
    btn_pause = tk.Button(frm_main, cursor="hand2", image=img_pause_btn, bd=0, bg="gray10", highlightthickness=0, activebackground="gray10")
    btn_next = tk.Button(frm_main, cursor="hand2", image=img_next_btn, bd=0, bg="gray10", highlightthickness=0, activebackground="gray10")
    btn_prev = tk.Button(frm_main, cursor="hand2", image=img_prev_btn, bd=0, bg="gray10", highlightthickness=0, activebackground="gray10")

    # grid layout
    lbl_playin_from.grid(row=0, column=1, columnspan=11)
    lbl_headphones.grid(row=1, column=0, columnspan=12, pady=20)
    lbl_song.grid(row=2, column=0, columnspan=12, pady=5)
    lbl_now_playing.grid(row=3, column=0, columnspan=12, pady=0)

    btn_prev.grid(row=4, column=0, columnspan=3, pady=3)
    btn_play.grid(row=4, column=3, columnspan=6, pady=20)
    btn_pause.grid(row=4, column=3, columnspan=6, pady=20)
    btn_pause.grid_remove()
    btn_next.grid(row=4, column=9, columnspan=3, pady=3)
    btn_add_songs.grid(row=0, column=13)

    listbox_songs.grid(row=1, rowspan=4, column=13)
    
    CWD = getcwd() # current working directory
    MUSIC_FOLDER = "music/"

    # music player functions
    def add_songs():
        """add songs to the music player playlist"""
        #open file/s
        temp_song = filedialog.askopenfilenames(initialdir=MUSIC_FOLDER, title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
        # insert each item into the list
        for song in temp_song:
            song = song.replace(f"{CWD}/music/", "")
            listbox_songs.insert("end", song)

        lbl_playin_from.config(text=f"playing from {MUSIC_FOLDER}")

    def play_song(evt):
        """play selected song"""
        song = listbox_songs.get("active")
        song_path = f"{CWD}/music/{song}"
        mixer.music.load(song_path)
        mixer.music.play()
        btn_play.grid_remove()
        btn_pause.grid_configure()

        update_curr_song_name(song)

    def pause_song():
        """to pause the song thats currently playing"""
        mixer.music.pause()
        btn_play.grid_configure()
        btn_pause.grid_remove()
    
    def resume_song():
        """resume the paused song"""
        mixer.music.unpause()
        btn_play.grid_remove()
        btn_pause.grid_configure()
    
    def next_song():
        """play next song on the list"""
        next_song_index = listbox_songs.curselection()[0] + 1
        next_song = listbox_songs.get(next_song_index)
        next_song_path = f"{CWD}/music/{next_song}"
        mixer.music.load(next_song_path)
        mixer.music.play()
        listbox_songs.selection_clear(0, "end")
        listbox_songs.activate(next_song_index)
        listbox_songs.select_set(next_song_index)
        update_curr_song_name(next_song)

    def prev_song():
        """play previous song on the list"""
        prev_song_index = listbox_songs.curselection()[0] - 1
        prev_song = listbox_songs.get(prev_song_index)
        prev_song_path = f"{CWD}/music/{prev_song}"
        mixer.music.load(prev_song_path)
        mixer.music.play()
        listbox_songs.selection_clear(0, "end")
        listbox_songs.activate(prev_song_index)
        listbox_songs.select_set(prev_song_index)
        update_curr_song_name(prev_song)

    def update_curr_song_name(name):
        """change song label name on GUI to the name provided
        Parameters:
            name: string - name of current song"""
        song_name = trim_song_name(name, 25)
        lbl_song.config(text=song_name)


    # bind functions to buttons/widgets
    btn_add_songs.config(command=add_songs)
    listbox_songs.bind("<<ListboxSelect>>", play_song)
    btn_pause.config(command=pause_song)
    btn_play.config(command=resume_song)
    btn_prev.config(command=prev_song)
    btn_next.config(command=next_song)

def trim_song_name(name, max_len):
    """trim the length of the song name to a specified length
    Parameters:
        name: string - name of the song
        max_len: number - the maximum length of the final string
    Return: string - trimmed song name"""

    # remove the .mp3 extention
    song_name = name.replace(".mp3", "")
    
    if len(song_name) > max_len:
        song_name = f"{song_name[:max_len]}..."

    return song_name



# If this file is executed like this:
# > python heart_rate.py
# then call the main function. However, if this file is simply
# imported (e.g. into a test file), then skip the call to main.
if __name__ == "__main__":
    main()
