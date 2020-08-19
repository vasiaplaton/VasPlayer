from tkinter import *
from PIL import Image, ImageTk
import vlc
import os
import time, threading

path = "."
setting0 = ["Музыка Василия Платона"]
font_name = "Menlo"
big_font = 16
album_font = 13
med_font = 14
small_font = 12

class UI:
    background = "#2b2b2b"
    active_bg = "#fc6400"
    default_bg = "#ad4500"
    height_w = 750
    width_w = 700
    num_track = 0

    def __init__(self, os_get):
        self.myOS = os_get

        # commands
        def play_pause():
            self.myOS.play_pause()

        def next_track():
            pass

        def prev_track():
            pass

        def on_album_change(_event):
            album = self.albumsList.curselection()[0]
            self.myOS.set_album(album)
            self.update_tracks()

        def on_track_change(_event):
            track = self.tracksList.curselection()[0]
            self.track_changed(track)
            myOS.play(track)

        def slider_motion(_event):
            self.myOS.set_pos(self.slide.get()/100)

        # window constructor
        self.root = Tk()
        self.root.geometry('700x750')
        self.root.config(bg=self.background)
        # album box(colon)
        albums_colon = Frame(self.root, bg=self.background)
        albums_colon.pack(side=LEFT, fill=Y)
        # albums colon Label
        albums_label = Label(albums_colon, text="Albums", font=(font_name, big_font, "bold"), fg="#dddddd", bg=self.background)
        albums_label.pack(side=TOP)
        # listbox create
        self.albumsList = Listbox(albums_colon, selectmode=SINGLE, bg=self.background, width=23, borderwidth=0,
                                  highlightthickness=0, fg="#dddddd", selectbackground=self.active_bg,
                                  font=(font_name, album_font), exportselection=False)
        self.albumsList.pack(side=LEFT, fill=Y)
        self.albumsList.bind('<<ListboxSelect>>', on_album_change)
        # scroll create
        albums_scroll = Scrollbar(albums_colon, command=self.albumsList.yview, bg=self.default_bg, bd=0, relief=FLAT,
                                  troughcolor=self.background, activebackground=self.active_bg)
        albums_scroll.pack(side=LEFT, fill=Y, pady=5, padx=5)
        # connect scroll to list
        self.albumsList.config(yscrollcommand=albums_scroll.set)
        # controls
        controls_box = Frame(self.root, bg=self.background, bd=0, padx=5)
        controls_box.pack(side=TOP, fill=X)
        # label_debug = Label(controls_box, text="Top controls", font=(font_name, big_font), fg="#dddddd", bg=self.background)
        # label_debug.pack(side=TOP)
        # icons
        # play
        k_resize = 1.7
        k_resize_1 = 3
        image = Image.open("play.png")
        image = image.resize((int(image.width/k_resize), int(image.height/k_resize)), Image.ANTIALIAS)
        self.play_i = ImageTk.PhotoImage(image)
        # pause
        image = Image.open("pause.png")
        image = image.resize((int(image.width / k_resize), int(image.height / k_resize)), Image.ANTIALIAS)
        self.pause_i = ImageTk.PhotoImage(image)
        # previous
        image = Image.open("prev.png")
        image = image.resize((int(image.width / k_resize_1), int(image.height / k_resize_1)), Image.ANTIALIAS)
        prev_t = ImageTk.PhotoImage(image)
        # next
        image = Image.open("next.png")
        image = image.resize((int(image.width / k_resize_1), int(image.height / k_resize_1)), Image.ANTIALIAS)
        next_t = ImageTk.PhotoImage(image)
        # buttons
        # play/pause
        self.play_b = Button(controls_box, image=self.play_i, activebackground=self.background,
                             bg=self.background, highlightthickness=0, bd=0, command=play_pause)
        self.play_b.image = self.play_i
        self.play_b.pack(side=LEFT, padx=15)
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

        self.time_now = Label(names, text="0:00", font=(font_name, small_font), fg="#dddddd", bg=self.background)
        self.time_now.pack(side=LEFT)

        self.time_end = Label(names, text="3:10", font=(font_name, small_font), fg="#dddddd", bg=self.background)
        self.time_end.pack(side=RIGHT)

        self.track_name = Label(names, text="Track", font=(font_name, med_font, "bold"), fg="#dddddd", bg=self.background)
        self.author_name = Label(names, text="Author", font=(font_name, small_font), fg="#dddddd", bg=self.background)
        self.track_name.pack(side=TOP)
        self.author_name.pack(side=TOP)

        self.slide = Scale(controls_box, variable=input, orient='horizontal', showvalue=0, relief=FLAT, bd=0,
                           bg=self.active_bg, highlightbackground=self.background, troughcolor=self.default_bg,
                           activebackground=self.active_bg, width=10, sliderlength=30)
        self.slide.bind("<B1-Motion>", slider_motion)
        self.slide['to'] = 100
        self.slide['from'] = 0
        self.slide.pack(side=TOP, fill=X)

        # tracks
        tracks_colon = Frame(self.root, bg=self.background)
        Label(self.root, text="Tracks", font=(font_name, big_font, "bold"), fg="#dddddd", bg=self.background).pack(side=TOP)
        # tracks constructor
        # listbox create
        self.tracksList = Listbox(tracks_colon, selectmode=SINGLE, bg=self.background, width=0, borderwidth=0,
                                  highlightthickness=0, fg="#dddddd", selectbackground=self.active_bg,
                                  font=(font_name, med_font), exportselection=False)
        self.tracksList_duration = Listbox(self.root, selectmode=SINGLE, bg=self.background, width=0, borderwidth=0,
                                           highlightthickness=0, fg="#dddddd", selectbackground=self.active_bg,
                                           font=(font_name, med_font))
        self.tracksList.bind('<<ListboxSelect>>', on_track_change)
        # scroll create

        def on_mouse_wheel(event):
            if event.num == 5:
                event.delta = 1
            if event.num == 4:
                event.delta = -1
            self.tracksList.yview("scroll", event.delta, "units")
            self.tracksList_duration.yview("scroll", event.delta, "units")
            # this prevents default bindings from firing, which
            # would end up scrolling the widget twice
            return "break"

        def on_vsb(*args):
            self.tracksList.yview(*args)
            self.tracksList_duration.yview(*args)
        tracks_scroll = Scrollbar(self.root, command=on_vsb, bg=self.default_bg, bd=0, relief=FLAT,
                                  troughcolor=self.background, activebackground=self.active_bg)
        tracks_scroll.pack(side=RIGHT, fill=Y, padx=5, pady=5)
        self.tracksList_duration.pack(side=RIGHT, fill=Y, padx=5, pady=5)
        tracks_colon.pack(side=LEFT, fill=BOTH, padx=15, pady=5)
        self.tracksList.pack(side=LEFT, fill=BOTH)
        # connect scroll to list
        self.tracksList.config(yscrollcommand=tracks_scroll.set)
        self.tracksList_duration.config(yscrollcommand=tracks_scroll.set)
        self.tracksList.bind("<Button-4>", on_mouse_wheel)
        self.tracksList.bind("<Button-5>", on_mouse_wheel)
        self.tracksList_duration.bind("<Button-4>", on_mouse_wheel)
        self.tracksList_duration.bind("<Button-5>", on_mouse_wheel)
        # album set
        self._set_album(0)
        # timer start
        self.timer()

    def loop_start(self):
        self.root.mainloop()

    def timer(self):
        # play/pause
        if not self.myOS.is_playing():
            if self.play_b.image != self.play_i:
                self.play_b.configure(image=self.play_i)
                self.play_b.image = self.play_i
        else:
            if self.play_b.image != self.pause_i:
                self.play_b.configure(image=self.pause_i)
                self.play_b.image = self.pause_i
        self.time_now.configure(text=self.myOS.get_time())
        self.slide.set(self.myOS.player.get_position()*100)
        # start timer
        threading.Timer(0.1, self.timer).start()

    @staticmethod
    def set_element_listbox(index, listbox):
        listbox.select_clear(0, "end")
        listbox.selection_set(index)
        listbox.see(index)
        listbox.activate(index)
        listbox.selection_anchor(index)

    def set_track(self, index):
        self.set_element_listbox(index, self.tracksList)
        self.num_track = index

    def _set_element_duration(self, index):
        self.set_element_listbox(index, self.tracksList_duration)

    def _set_album(self, index):
        self.albumsList.select_clear(0, "end")
        self.albumsList.selection_set(index)
        self.albumsList.see(index)
        self.albumsList.activate(index)
        self.albumsList.selection_anchor(index)

    def update_albums(self, albums):
        self.albumsList.delete(0, 'end')
        for album in albums:
            if len(album) > 21:
                album = album[0:20]
                album += "..."
            else:
                while len(album) < 21:
                    album += ' '
            self.albumsList.insert(END, album)
        if self.albumsList.size() == 0:
            self.albumsList.insert(END, "       nothing        ")

    def update_tracks(self):
        self.tracksList.delete(0, 'end')
        self.tracksList_duration.delete(0, 'end')
        for i in range(len(self.myOS.get_tracks())):
            self.tracksList_duration.insert(END, self.myOS.get_length(i))
            # str
            self.tracksList.insert(END, self.myOS.get_name(i))
        if self.tracksList.size() == 0:
            self.tracksList.insert(END, "       nothing        ")

    def track_changed(self, index):
        self._set_element_duration(index)
        # labels set
        self.time_end.configure(text=self.myOS.get_length(index))
        print(self.myOS.get_author_and_title(index))
        self.track_name.configure(text=self.myOS.get_author_and_title(index)[1])
        self.author_name.configure(text=self.myOS.get_author_and_title(index)[0])


class OS:
    path = ""
    dirs = [""]
    tracks = [""]
    album = ""

    def __init__(self, path_d):
        self.path = path_d
        self.player = vlc.MediaPlayer()

    def get_dirs(self):
        self.dirs = []
        for directory in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, directory)) and directory[0] != '.':
                self.dirs.append(directory)
        return self.dirs

    def set_album(self, album_num=0):
        self.tracks = []
        self.album = self.dirs[album_num]
        path_d = os.path.join(self.path, self.dirs[album_num])
        for track in os.listdir(path_d):
            if self._get_ext(track) == "mp3":
                self.tracks.append(track)
        self.tracks.sort(key=self._get_num)
        for album in setting0:
            if self.album == album:
                print(self.tracks)
                self.tracks.reverse()

    def get_tracks(self):
        return self.tracks

    @staticmethod
    def _get_ext(string):
        num = len(string)-1
        ext = ""
        while string[num] != '.' and num > 0:
            ext = string[num] + ext
            num -= 1
        return ext

    @staticmethod
    def _get_num(string):
        i = 0
        num = ""
        while (string[i] != ' ') and (i < len(string)):
            num = num + string[i]
            i += 1
        if num == "":
            num = 0
        else:
            num = int(num)
        return num

    def get_name(self, index):
        string = self.tracks[index]
        start = 0
        stop = 0
        for i in range(len(string)):
            if string[i] == ' ':
                start = i
                break
        for i in reversed(range(len(string))):
            if string[i] == '.':
                stop = i
                break
        return string[start+1:stop]

    def get_author_and_title(self, index):
        name = self.get_name(index)
        start = len(name)
        for i in range(len(name)):
            if name[i] == '-':
                start = i
                break
        return name[0: start-1], name[start+2: len(name)]

    def get_length(self, track=0):
        path_t = os.path.join(self.path, self.album, self.tracks[track])
        media = vlc.Media(path_t)
        media.parse()
        duration = media.get_duration()
        return self._format_ms_time(duration)

    def get_time(self):
        return self._format_ms_time(self.player.get_time())

    @staticmethod
    def _format_ms_time(duration):
        duration = duration // 1000
        string = str(duration // 60) + ':' + str(duration % 60).zfill(2)
        return string

    def play(self, index):
        path_t = os.path.join(self.path, self.album, self.tracks[index])
        media = vlc.Media(path_t)
        self.player.set_media(media)
        self.player.play()

    def play_pause(self):
        self.player.pause()

    def set_pos(self, pos):
        self.player.set_position(pos)

    def is_playing(self):
        return self.player.is_playing()


myOS = OS("/media/vasia/HDD1TB/music1")
myUI = UI(myOS)
myUI.update_albums(myOS.get_dirs())
myUI.loop_start()
