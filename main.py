from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import vlc
import os
import time

path = "."


class UI:
    background = "#2b2b2b"
    active_bg = "#fc6400"
    default_bg = "#ad4500"
    height_w = 750
    width_w = 700
    num_track = 0

    def __init__(self):
        # window constructor
        self.root = Tk()
        self.root.geometry('700x750')
        self.root.config(bg=self.background)

        # albums constructor
        languages = ["PythonPythonPythonPythonPythonPythonPythonPython", "JavaScript", "C#", "Java", "C/C++", "Swift",
                     "PHP", "Visual Basic.NET", "F#", "Ruby", "Rust", "R", "Go",
                     "T-SQL", "PL-SQL", "Typescript"]
        # album box(colon)
        albums_colon = Frame(self.root, bg=self.background)
        albums_colon.pack(side=LEFT, fill=Y)
        # albums colon Label
        albums_label = Label(albums_colon, text="Albums", font=("Menlo", 16, "bold"), fg="#dddddd", bg=self.background)
        albums_label.pack(side=TOP)
        # listbox create
        self.albumsList = Listbox(albums_colon, selectmode=SINGLE, bg=self.background, width=0, borderwidth=0,
                                  highlightthickness=0, fg="#dddddd", selectbackground=self.active_bg,
                                  font=("Menlo", 13), exportselection=False)
        self.albumsList.pack(side=LEFT, fill=Y)
        # scroll create
        albums_scroll = Scrollbar(albums_colon, command=self.albumsList.yview, bg=self.default_bg, bd=0, relief=FLAT,
                                  troughcolor=self.background, activebackground=self.active_bg)
        albums_scroll.pack(side=LEFT, fill=Y, pady=5, padx=5)
        # connect scroll to list
        self.albumsList.config(yscrollcommand=albums_scroll.set)
        # debug insert test elements
        for i in range(4):
            for language in languages:
                if len(language) > 21:
                    language = language[0:20]
                    language += "..."
                self.albumsList.insert(END, language)

        # controls
        controls_box = Frame(self.root, bg=self.background, bd=0, padx=5)
        controls_box.pack(side=TOP, fill=X)
        # label_debug = Label(controls_box, text="Top controls", font=("Menlo", 16), fg="#dddddd", bg=self.background)
        # label_debug.pack(side=TOP)
        # icons
        # play
        k_resize = 1.7
        k_resize_1 = 3
        image = Image.open("play.png")
        image = image.resize((int(image.width/k_resize), int(image.height/k_resize)), Image.ANTIALIAS)
        play = ImageTk.PhotoImage(image)
        # pause
        image = Image.open("pause.png")
        image = image.resize((int(image.width / k_resize), int(image.height / k_resize)), Image.ANTIALIAS)
        pause = ImageTk.PhotoImage(image)
        # previous
        image = Image.open("prev.png")
        image = image.resize((int(image.width / k_resize_1), int(image.height / k_resize_1)), Image.ANTIALIAS)
        prev_t = ImageTk.PhotoImage(image)
        # next
        image = Image.open("next.png")
        image = image.resize((int(image.width / k_resize_1), int(image.height / k_resize_1)), Image.ANTIALIAS)
        next_t = ImageTk.PhotoImage(image)
        # commands

        def play_pause():
            play_b.config(image=pause)
            self.set_track(4)
            self._set_album(4)
            self.root.focus_set()

        def next_track():
            pass

        def prev_track():
            pass
        # buttons
        # play/pause
        play_b = Button(controls_box, image=play, activebackground=self.background,
                        bg=self.background, highlightthickness=0, bd=0, command=play_pause)
        play_b.image = play
        play_b.pack(side=LEFT, padx=15)
        # prev
        prev_b = Button(controls_box, image=prev_t, activebackground=self.background,
                        bg=self.background, highlightthickness=0, bd=0, command=prev_track)
        prev_b.image = prev_t
        prev_b.pack(side=LEFT, padx=0)
        # next
        next_b = Button(controls_box, image=next_t, activebackground=self.background,
                        bg=self.background, highlightthickness=0, bd=0, command=next_track)
        next_b.image = next_t
        next_b.pack(side=LEFT, padx=2)
        # labels
        names = Frame(controls_box, bg=self.background)
        names.pack(fill=X)

        time_now = Label(names, text="0:00", font=("Menlo", 12), fg="#dddddd", bg=self.background)
        time_now.pack(side=LEFT)

        time_end = Label(names, text="3:10", font=("Menlo", 12), fg="#dddddd", bg=self.background)
        time_end.pack(side=RIGHT)

        track_name = Label(names, text="Track", font=("Menlo", 14, "bold"), fg="#dddddd", bg=self.background)
        author_name = Label(names, text="Author", font=("Menlo", 12), fg="#dddddd", bg=self.background)
        track_name.pack(side=TOP)
        author_name.pack(side=TOP)

        slide = Scale(controls_box, variable=input, orient='horizontal', showvalue=0, relief=FLAT, bd=0,
                      bg=self.active_bg, highlightbackground=self.background, troughcolor=self.default_bg,
                      activebackground=self.active_bg, width=10, sliderlength=30)
        slide['to'] = 100
        slide['from'] = 0
        slide.pack(side=TOP, fill=X)

        # tracks
        tracks_colon = Frame(self.root, bg=self.background)
        Label(self.root, text="Tracks", font=("Menlo", 16, "bold"), fg="#dddddd", bg=self.background).pack(side=TOP)
        # tracks constructor
        # listbox create
        self.tracksList = Listbox(tracks_colon, selectmode=SINGLE, bg=self.background, width=0, borderwidth=0,
                                  highlightthickness=0, fg="#dddddd", selectbackground=self.active_bg,
                                  font=("Menlo", 14), exportselection=False)
        # scroll create
        tracks_scroll = Scrollbar(self.root, command=self.tracksList.yview, bg=self.default_bg, bd=0, relief=FLAT,
                                  troughcolor=self.background, activebackground=self.active_bg)
        tracks_scroll.pack(side=RIGHT, fill=Y, padx=5, pady=5)
        tracks_colon.pack(side=LEFT, fill=BOTH, padx=15, pady=5)
        self.tracksList.pack(side=LEFT, fill=BOTH)
        # connect scroll to list
        self.tracksList.config(yscrollcommand=tracks_scroll.set)
        # debug insert test elements
        for i in range(15):
            for language in languages:
                self.tracksList.insert(END, language)

    def loop_start(self):
        self.root.mainloop()

    def set_track(self, index):
        self.tracksList.select_clear(0, "end")
        self.tracksList.selection_set(index)
        self.tracksList.see(index)
        self.tracksList.activate(index)
        self.tracksList.selection_anchor(index)
        self.num_track = index

    def _set_album(self, index):
        self.albumsList.select_clear(0, "end")
        self.albumsList.selection_set(index)
        self.albumsList.see(index)
        self.albumsList.activate(index)
        self.albumsList.selection_anchor(index)
        self.albumsList = index



class MusicPlayer:
    def __init__(self):
        pass


myUI = UI()
myUI.loop_start()
