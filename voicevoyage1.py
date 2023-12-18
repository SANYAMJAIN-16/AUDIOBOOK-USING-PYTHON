# importing all module
import pyttsx3
import sqlite3 as sq
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as tmsg
from PIL import Image,ImageTk
import os
import pygame



#creating the fuctio ns
conn=sq.connect("userdatabase.db")
c = conn.cursor()

# Create user table if it doesn't exist
c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            fullname TEXT ,
            phoneno NUMBER,
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
conn.commit()
# adding user
def audiobook():
    root = Tk()
    root.title("VOICEVOYAGE")
    root.wm_iconbitmap("listening.ico")
    root.minsize(1300,700)
    root.maxsize(1300,700)
    root.config(bg="#ADD8E6")

    def add_user(fullname,phoneno,username, password):
        c.execute("INSERT INTO users (fullname,phoneno,username, password) VALUES (?,?,?, ?)", (fullname,phoneno,username, password))
        conn.commit()
    # checking user
    def check_user(username,password):
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return c.fetchone()
    # function for user sign up
    def signup():
        fullname=entry1.get()
        phoneno=entry2.get()
        username = entry3.get()
        password = entry4.get()

        if check_user(username, password):
            tmsg.showerror("Error", "Username already exists.")
        else:
            if len(password)>=8:
                if (username[0].isdigit()):
                    tmsg.showerror("Error", "Your username should not start with numeric value")
                else:
                    add_user(fullname, phoneno, username, password)
                    tmsg.showinfo("Success", "Registration successful!,\nVOICEVOYAGE family welcomes you")
            else:
                tmsg.showerror("Error","Your password is below 8,Which should be above 8")
        var1.set("YOU HAVE SUCCESSFULLY REGISTERED PROPERLY NOW PLEASE LOGIN")
    # function for login
    def login():
        username = entry5.get()
        password = entry6.get()

        # Check if username and password match
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            show_audiobooks_screen(username)
            var1.set("LOGIN SUCCESSFUL")
        else:
            tmsg.showerror("Error", "Invalid username or password.")

    def audiobook_select(book):
        audiobook_playback()
    def audiobook_playback():
        book=var.get()
        def on_listbox_select(event):
            global selected_file
            selected_index = listbox1.curselection()
            if selected_index:
                index = int(selected_index[0])
                selected_file = file_paths[index]
            var1.set(f"THE BOOK SELECTED IS {selected_file}")

        def play_music(file_path):
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(1.0)
            var1.set("PLAYING AUDIO...")



        def pause_audio():
            pygame.mixer.music.pause()
            var1.set("AUDIO IS PAUSED")
        def resume_music():
            pygame.mixer.music.unpause()
            var1.set("AUDIO IS PLAYED")
        def stop_music():
            pygame.mixer.music.stop()
            var1.set("AUDIO STOPPED")

        def playback_control(file_path):
            global photo
            frame8=Frame(root)
            frame8.place(x=920,y=40)
            if book==1:
                photo=ImageTk.PhotoImage(file="boys life.png")
                Button(frame8,image=photo).pack()
            elif book==2:
                photo=ImageTk.PhotoImage(file="haunted house.png")
                Button(frame8,image=photo).pack()
            elif book==3:
                photo=ImageTk.PhotoImage(file="the world best litrature.png")
                Button(frame8,image=photo).pack()
            elif book==4:
                photo=ImageTk.PhotoImage(file="The Falcon on the Baltic.png")
                Button(frame8,image=photo).pack()
            else:
                photo=ImageTk.PhotoImage(file="audio.png")
                Button(frame8,image=photo).pack()
            label12=Label(frame8,text=f"PLAYING THE BOOK {book} OF PATH {file_path}",bg="red",fg="green")
            label12.pack(fill=X)
            button12=Button(frame8,text="▶",command= lambda i=file_path:play_music(i))
            button12.pack(side=LEFT,anchor="nw")
            button13=Button(frame8,text="❚❚",command=pause_audio)
            button13.pack(side=LEFT,anchor="nw")
            button14=Button(frame8,text="resume",command=resume_music)
            button14.pack(side=LEFT,anchor="nw")
            button15=Button(frame8,text="■",command=stop_music)
            button15.pack(side=LEFT,anchor="nw")




        def play_selected_music():
            if selected_file:
                print(f"SELECTED : {selected_file}")
                playback_control(selected_file)


        def populate_listbox(folder_path):
            global file_paths
            file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
            for file_path in file_paths:
                listbox1.insert(END, os.path.basename(file_path))



        # Function to read the selected text file aloud


        frame4 = Frame(root, width=180, height=50)
        frame4.pack(anchor="sw", pady=90)
        label20=Label(frame4,text="PLEASE SELECT THE CHAPTERS LISTED BELOW")
        label20.pack()
        if book==1:
            folder_path = "boys life"
            listbox1 = Listbox(frame4, selectmode=SINGLE, height=15, width=60)
            scrollbar1 = Scrollbar(frame4, command=listbox1.yview)
            listbox1.config(yscrollcommand=scrollbar1.set)
            populate_listbox(folder_path)
            listbox1.bind("<<ListboxSelect>>", on_listbox_select)
            listbox1.pack(side=LEFT,padx=5,pady=10)
            scrollbar1.pack(side=RIGHT, fill=Y, padx=5, pady=10)
            button5=Button(frame4,text="SELECTED",command=play_selected_music)
            button5.pack(side=BOTTOM,padx=10)

        elif book==2:
            folder_path = "haunted house"
            listbox1 = Listbox(frame4, selectmode=SINGLE, height=15, width=60)
            scrollbar1 = Scrollbar(frame4, command=listbox1.yview)
            listbox1.config(yscrollcommand=scrollbar1.set)
            populate_listbox(folder_path)
            listbox1.bind("<<ListboxSelect>>", on_listbox_select)
            listbox1.pack(side=LEFT, padx=5, pady=10)
            scrollbar1.pack(side=RIGHT, fill=Y, padx=5, pady=10)
            button6 = Button(frame4, text="SELECTED", command=play_selected_music)
            button6.pack(side=BOTTOM,padx=10)

        elif book==3:
            folder_path = "worlds best litrature"
            listbox1 = Listbox(frame4, selectmode=SINGLE, height=15, width=60)
            scrollbar1 = Scrollbar(frame4, command=listbox1.yview)
            listbox1.config(yscrollcommand=scrollbar1.set)
            populate_listbox(folder_path)
            listbox1.bind("<<ListboxSelect>>", on_listbox_select)
            listbox1.pack(side=LEFT, padx=5, pady=10)
            scrollbar1.pack(side=RIGHT, fill=Y, padx=5, pady=10)
            button7 = Button(frame4, text="SELECTED", command=play_selected_music)
            button7.pack(side=BOTTOM,padx=10)

        elif book==4:
            folder_path = "The Falcon on the Baltic"
            listbox1 = Listbox(frame4, selectmode=SINGLE, height=15, width=60)
            scrollbar1 = Scrollbar(frame4, command=listbox1.yview)
            listbox1.config(yscrollcommand=scrollbar1.set)
            populate_listbox(folder_path)
            listbox1.bind("<<ListboxSelect>>", on_listbox_select)
            listbox1.pack(side=LEFT, padx=5, pady=10)
            scrollbar1.pack(side=RIGHT, fill=Y, padx=5, pady=10)
            button8 = Button(frame4, text="SELECTED", command=play_selected_music)
            button8.pack(side=BOTTOM,padx=10)

        elif book==6:
            exit()



    def show_audiobooks_screen(username):
        frame3=Frame(root,width=200,height=10)
        frame3.place(x=400,y=30)
        label10=Label(frame3,text=f"hello,let us start {username}",bg="#AA98A9")
        label10.pack(fill=X)
        canvas1=Canvas(frame3,width=700,height=30)
        canvas1.pack()
        image_paths = ["boys life.png", "haunted house.png", "the world best litrature.png","The Falcon on the Baltic.png"]
        images = []
        for image_path in image_paths:
            image = Image.open(image_path)
            image = ImageTk.PhotoImage(image)
            images.append(image)
        for i, image in enumerate(images):
            button3=Button(canvas1,image=image,command=lambda idx=i: audiobook_select(images[idx]))
            button3.pack(side=LEFT,padx=10)
        label11=Label(frame3,text="Which book want to select?")
        label11.pack()
        radio1=Radiobutton(frame3,text="boys life",value=1,variable=var)
        radio1.pack()
        radio2 = Radiobutton(frame3, text="haunted house", value=2, variable=var)
        radio2.pack()
        radio3 = Radiobutton(frame3, text="the world best literature", value=3, variable=var)
        radio3.pack()
        radio4 = Radiobutton(frame3, text="The Falcon on the Baltic", value=4, variable=var)
        radio4.pack()
        radio6=Radiobutton(frame3,text="EXIT",variable=var,value=6)
        radio6.pack()
        button4=Button(frame3,text="SUBMIT",command=audiobook_playback)
        button4.pack()

    var = IntVar()
    var1 = StringVar()
    var1.set("looking for the further process...")
    label16 = Label(root, textvariable=var1, relief=SUNKEN, font="airal 12",anchor="w")
    label16.pack(side=BOTTOM,fill=X)
    label1 = Label(text="WELCOME TO VOICEVOYAGE", font="arial 15 bold", bg="grey")
    label1.pack(fill=X)
    frame1 = Frame(root)
    frame1.pack(anchor="w")
    label8 = Label(frame1, text="SIGN UP FORM", font="arial 15 bold")
    label8.grid(row=0)
    label2 = Label(frame1, text="FULL NAME", font="arial 12")
    label2.grid(row=1, column=0)
    entry1 = Entry(frame1, font="arial 12")
    entry1.grid(row=1, column=1, padx=10)
    label3 = Label(frame1, text="PHONE NUMBER", font="arial 12")
    label3.grid(row=2, column=0)
    entry2 = Entry(frame1, font="arial 12")
    entry2.grid(row=2, column=1, padx=10)
    label4 = Label(frame1, text="USERNAME", font="arial 12")
    label4.grid(row=3, column=0)
    entry3 = Entry(frame1, font="arial 12")
    entry3.grid(row=3, column=1, padx=10)
    label5 = Label(frame1, text="PASSWORD", font="arial 12")
    label5.grid(row=4, column=0)
    entry4 = Entry(frame1, font="arial 12", show="*")
    entry4.grid(row=4, column=1, padx=5)
    button1 = Button(frame1, text="SIGN UP", command=signup)
    button1.grid(row=5, column=1)
    frame2 = Frame(root)
    frame2.pack(anchor="w", pady=1)
    label9 = Label(frame2, text="LOGIN FORM", font="arial 15 bold")
    label9.grid(row=0)
    label6 = Label(frame2, text="USERNAME", font="arial 12")
    label6.grid(row=1, column=0)
    entry5 = Entry(frame2, font="arial 12")
    entry5.grid(row=1, column=1, padx=18)
    label7 = Label(frame2, text="PASSWORD", font="arial 12")
    label7.grid(row=2, column=0)
    entry6 = Entry(frame2, show="*", font="arial 12")
    entry6.grid(row=2, column=1, padx=18)
    button2 = Button(frame2, text="LOGIN", command=login)
    button2.grid(row=3, column=1)

    root.mainloop()

# main function
audiobook()
