from tkinter import *
from tkinter import filedialog
import pygame
import webbrowser
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root=Tk()
root.title("Music Player")
root.iconbitmap("C:/Users/sam/Documents/pyprog/Tkinter/musicplayer/headphoneicon.ico.bmp")
root.geometry("500x500")
root.configure(bg='#264653')
# initializin pygame mixer
pygame.mixer.init()



#grab song time
def song_time():
    #sliders double timing bug fix
    if stopped:
        return True
    #grab current sog elapsed time
    current_time= pygame.mixer.music.get_pos()/1000
    #temporary label to get data
    #slider_label.config(text=f'Slider:{int(slider.get())} and Song Pos: {int(current_time)}')
    #converts to time formate
    converted_current_time= time.strftime('%M:%S', time.gmtime(current_time))


    #gives the current song playing
    current_song = song_list.curselection()
    #grab song title from playlist
    song = song_list.get(ACTIVE)
    #adding directory and file type(.mp3) to the song title to play it
    song = f'E:/mUz!c/{song}.mp3'

    #get song length
    song_gen = MP3(song)
    #loads song with mutagen...... gives the length in seconds
    global song_length
    song_length= song_gen.info.length
    #converting the only seconds into minutes and seconds
    converted_song_length= time.strftime('%M:%S', time.gmtime(song_length))

    #increase current_time by 1 sec
    current_time+=1
    if int(slider.get())== int(song_length):
        status_bar.config(text=f'Music: {converted_song_length} of {converted_song_length} ')

    elif paused:
        pass



    elif int(slider.get()) == int(current_time):
        #slider hasn't moved
        #updating slider position
        slider_position =  int(song_length)

        slider.config(to=slider_position, value=int(current_time))
    else:
        #slider has been moved
        #updating slider position
        slider_position =  int(song_length)

        slider.config(to=slider_position, value=int(slider.get()))

        #converts to time formate
        converted_current_time= time.strftime('%M:%S', time.gmtime(int(slider.get())))
        #output time to status bar
        status_bar.config(text=f'Music: {converted_current_time} of {converted_song_length} ')
        #move this thing along by one second
        next_time= int(slider.get())+1
        slider.config(value=next_time)


    # #output time to status bar
    # status_bar.config(text=f'Music: {converted_current_time} of {converted_song_length} ')


    # fake_label = Label(root, text=int(current_time))
    # fake_label.pack(pady=10)


    #update time
    status_bar.after(1000,song_time)

#function to add song
def add_song():
    song = filedialog.askopenfilename(initialdir='E:/mUz!c', title="Choose a song", filetypes=(("mp3 files", "*.mp3"),))

#to display only song name
    song = song.replace("E:/mUz!c/","")
    song = song.replace(".mp3","")
#to insert song
    song_list.insert(END, song)

#add multiple Songs
def add_multi_song():
    #to add multiple songs using .askopenfilenames not .askopenfilename
    songs = filedialog.askopenfilenames(initialdir='E:/mUz!c', title="Choose a song", filetypes=(("mp3 files", "*.mp3"),))
    #loop through
    for song in songs:
        #to display only song name
            song = song.replace("E:/mUz!c/","")
            song = song.replace(".mp3","")
        #to insert song
            song_list.insert(END, song)

#slider function
def slide(x):
    #slider_label.config(text=f'{int(slider.get())} of {int(song_length)}')
    song = song_list.get(ACTIVE)
    song = f'E:/mUz!c/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(slider.get()))


#to delete a single song
def delete_song():
    stop()
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()
#to delete all songs
def delete_all_songs():
    stop()
    song_list.delete(0,END)
    pygame.mixer.music.stop()


#function to play a selected song
def play():
    #setting stopped variable to false to play the song
    global stopped
    stopped = False
    song = song_list.get(ACTIVE)
    song = f'E:/mUz!c/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #call the time function
    song_time()

    #updating slider position
    slider_position =  int(song_length)
    slider.config(to=slider_position, value=0)



global stopped
stopped = False

#function to stop music
def stop():

    #reset slider and status bar
    status_bar.config(text='')
    slider.config(value=0)

    pygame.mixer.music.stop()
    song_list.selection_clear(ACTIVE)
    #clear the text bar or show some message
    status_bar.config(text='')

    #set stop variable to True
    global stopped
    stopped=True

#global pause variable
global paused
paused = False

#functon to pause the song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#play previous song
def prev():
    #reset slider and status bar
    status_bar.config(text='')
    slider.config(value=0)
    #gives the current song tuple no.
    next_one = song_list.curselection()
    #add one to the current song no.
    next_one= next_one[0]-1
    #grab song title from playlist
    song = song_list.get(next_one)
    #adding directory and file type(.mp3) to the song title to play it
    song = f'E:/mUz!c/{song}.mp3'
    #load and playing the song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #move active bar in te Playlist
    song_list.selection_clear(0, END)
    #to activate bar again
    song_list.activate(next_one)
    #to set the bar to new song
    song_list.selection_set(next_one, last=None)

    #updating slider position
    slider_position =  int(song_length)
    slider.config(to=slider_position, value=0)

#Function to play nextsong
def next():
    #reset slider and status bar
    status_bar.config(text='')
    slider.config(value=0)
    #gives the current song tuple no.
    next_one = song_list.curselection()
    #add one to the current song no.
    next_one= next_one[0]+1
    #grab song title from playlist
    song = song_list.get(next_one)
    #adding directory and file type(.mp3) to the song title to play it
    song = f'E:/mUz!c/{song}.mp3'
    #load and playing the song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #move active bar in te Playlist
    song_list.selection_clear(0, END)
    #to activate bar again
    song_list.activate(next_one)
    #to set the bar to new song
    song_list.selection_set(next_one, last=None)

    #updating slider position
    slider_position =  int(song_length)
    slider.config(to=slider_position, value=0)


def onClick(x):
    webbrowser.open(x,new=1)

#volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())



#url for youtube music
url = "https://music.youtube.com/"

#main Frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#volume label frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=3, column=0)


#Playlist box
song_list = Listbox(main_frame, bg="#e76f51", fg="#264653", width=60, selectbackground="#f4a261", selectforeground="black")
song_list.grid(row=0, column=0)



#Buttons images

prev_bt = PhotoImage(file='musicplayer/prev.png')
next_bt = PhotoImage(file='musicplayer/next.png')
play_bt =PhotoImage(file='musicplayer/play.png')
pause_bt =PhotoImage(file='musicplayer/pause.png')
stop_bt =PhotoImage(file='musicplayer/stop.png')
youtube_bt= PhotoImage(file='musicplayer/youtube.png')

#Control Buttons Frame
controls_frame = Frame(main_frame)
controls_frame.grid(row=1, column=0, pady=20)



#Control Buttons
prev_button = Button(controls_frame, image=prev_bt,  borderwidth=0, command= prev)
next_button = Button(controls_frame, image=next_bt, borderwidth=0, command= next)
play_button = Button(controls_frame, image=play_bt, borderwidth=0, command= play)
pause_button = Button(controls_frame, image=pause_bt, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_bt, borderwidth=0, command= stop)
click = Button(controls_frame, image=youtube_bt, borderwidth=0, command=lambda: onClick(url))



prev_button.grid(row=0,column=0,padx=10)
next_button.grid(row=0,column=4,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=1,padx=10)
stop_button.grid(row=0,column=3,padx=10)
click.grid(row=1, column=2,padx=10,pady=15)

#menu

my_menu = Menu(root)
root.config(menu=my_menu)


#to add song

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to Playlist", command= add_song)

#to remove songs
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist", command=delete_all_songs)


#add multiple Songs
add_song_menu.add_command(label="Add multiple songs to Playlist", command= add_multi_song)

#
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=N)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#creating the slider
slider =ttk.Scale(main_frame, from_= 0, to=100, orient=HORIZONTAL, value=0, length=360, command=slide)
slider.grid(row=2,column=0,pady=5)

#creating volume slider
volume_slider=ttk.Scale(volume_frame, from_= 0, to=1, orient=HORIZONTAL, value=1, length=125, command=volume)
volume_slider.pack()


#label to see where the slider is
# slider_label = Label(root, text="0")
# slider_label.pack(pady=10)

root.mainloop()
