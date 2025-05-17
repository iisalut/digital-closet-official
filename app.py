import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
import json
import os
from PIL import Image, ImageTk, UnidentifiedImageError
import pillow_heif
pillow_heif.register_heif_opener()
from tkinter.filedialog import askopenfilename
from tkinter import messagebox




# Create a themed window using ttkbootstrap
window = ttk.Window(themename="flatly")
window.title("Digital Closet")

# Set window size and configure grid
window.geometry("1200x850")  # Set a specific window size
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Create a style
style = ttk.Style()
style.configure('Custom.TFrame', background='beige')
style.configure('Custom.TFrame', background='beige')
style.configure("Header.TLabel",
                font=("Pangolin", 34),
                foreground="brown",
                background="beige",
                anchor="center")
style.configure("mid.TLabel",
                font=("Pangolin", 24),
                foreground="brown",
                background="beige",
                anchor="center")
style.configure("small.TLabel",
                font=("Pangolin", 15),
                foreground="brown",
                background="beige",
                anchor="center")

#------definitions------

global username
username= ""
global password
password=""

def json_save():
    file = 'users.json'
    # Check if file exists, if not create empty list
    if os.path.exists(file):
        with open(file, 'r', newline='') as json_file:
            if json_file.read().strip():  # Check if file is not empty
                json_file.seek(0)  # Go back to start of file
                data = json.load(json_file)
            else:
                data = []
    else:
        data = []

    user_data = {'username': username, 'password': password}
    data.append(user_data)
    with open(file, 'w', newline='') as json_file:
        json.dump(data, json_file, indent=4)
    print("Saved username and password")
def save_username_password():
    global username
    global password
    username =signUp_username_entry.get().strip()
    password =signUp_password_entry.get().strip()

    has_dig=False
    for i in password:
        if i.isdigit():
            has_dig = True
    if len(password) < 5 or len(password) > 10:
        signUP_password_error.config(text=" Password must be between 5 and 10 characters.")
    elif has_dig == False:
        signUP_password_error.config(text="must contain at least 1 digit")
    elif username == "":
        signUP_username_error.config(text="Please enter your username")
    else:
        signUP_password_error.config(text="Sign up successful")
        json_save()
        signUp_next_button.config(state='normal')

def login_json():
    global check,username,password
    file = 'users.json'
    if os.path.exists(file):
        with open(file, 'r', newline='') as json_file:
            data = json.load(json_file)
            #print("Attempting login with:", username, password)#tests
            #print("Data in JSON:", data)#tests
            for user in data:
                if user['username'] == username and user['password'] == password:
                    print("User found: " + user['username']+" user password : " +user['password'])#tests
                    check = True
                    break
            else:  # This else belongs to the for loop - runs if no break occurs
                check = False
    else:
        check = False

def login_verification():
    global username, password
    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()
    login_json()
    if check==True:
        login_password_error.configure(text='Account found')
        login_next_button.config(state='normal')
    else:
        login_password_error.configure(text='Account not found')



# Page 1 - Welcome page
#<editor-fold desc="Welcome page 1">
page1 = ttk.Frame(window, style='Custom.TFrame')
page1.grid(row=0, column=0, sticky="nsew")
page1.grid_propagate(False)

# Add welcome text to page1
welcome_text = ttk.Label(page1, text="Welcome to your closet !!",
                        style="Header.TLabel")
welcome_text.pack(pady=50)

welcome_signUp_button = ttk.Button(page1, text="Sign Up",
                                 bootstyle='primary',
                                 command=lambda: next_page(page2),
                                   width=20)
welcome_signUp_button.pack(pady=10)

welcome_login_button = ttk.Button(page1, text="Login",
                                bootstyle=PRIMARY,
                                  width=20,
                                  command=lambda: next_page(page3))
welcome_login_button.pack(pady=10)
#</editor-foldl

# Page 2 - Sign Up page
# <editor-fold desc="Description">
page2 = ttk.Frame(window, style='Custom.TFrame')
page2.grid(row=0, column=0, sticky="nsew")
page2.grid_propagate(False)

signUp_text = ttk.Label(page2, text="Sign Up Page",style="Header.TLabel")
signUp_text.pack(pady=50)
signUp_username_text = ttk.Label(page2, text="Username",style="mid.TLabel")
signUp_username_text.pack(pady=2)
signUP_username_error=ttk.Label(page2, text="", style="small.TLabel")
signUP_username_error.pack(padx=1, pady=1)
signUp_username_entry = ttk.Entry(page2, width=30, bootstyle=PRIMARY)
signUp_username_entry.pack(pady=2)

signUp_password_text = ttk.Label(page2, text="Password",style="mid.TLabel")
signUp_password_text.pack(pady=2)
signUP_password_error=ttk.Label(page2, text="", style="small.TLabel")
signUP_password_error.pack(padx=1, pady=1)
signUp_password_entry = ttk.Entry(page2, width=30, bootstyle=PRIMARY)
signUp_password_entry.config(show="*")
signUp_password_entry.pack(pady=2)

signUp_submit_button = ttk.Button(page2, text="Submit",bootstyle=PRIMARY, width=15, command=save_username_password)
signUp_submit_button.pack(pady=10)

signUp_next_button = ttk.Button(page2, text="Next",bootstyle=PRIMARY, width=15,command=lambda: next_page(page4))
signUp_next_button.pack(pady=10)
signUp_next_button.config(state='disabled')

bottom_frame = ttk.Frame(page2, style="Custom.TFrame")
bottom_frame.pack(fill='x', side='bottom')
signUp_back_button = ttk.Button(bottom_frame, text="Back",bootstyle=PRIMARY, width=15, command=lambda :next_page(page1))
signUp_back_button.pack(pady=10,padx=10 ,side='left')
# </editor-fold>

#login page (page3)
page3 = ttk.Frame(window, style="Custom.TFrame")
page3.grid(row=0, column=0, sticky="nsew")
page3.grid_propagate(False)
# Page 3 - Login Page
page3 = ttk.Frame(window, style='Custom.TFrame')
page3.grid(row=0, column=0, sticky="nsew")
page3.grid_propagate(False)

login_head_label = ttk.Label(page3, text="Login", style="Header.TLabel")
login_head_label.pack(padx=10, pady=10)

login_username_label = ttk.Label(page3, text="Username", style="mid.TLabel")
login_username_label.pack(padx=10, pady=5)
login_username_entry = ttk.Entry(page3, width=30, bootstyle=PRIMARY)
login_username_entry.pack(padx=10, pady=1)

login_password_label = ttk.Label(page3, text="Password", style="mid.TLabel")
login_password_label.pack(padx=10, pady=5)
login_password_entry = ttk.Entry(page3, width=30, bootstyle=PRIMARY, show='*')
login_password_entry.pack(padx=10, pady=1)

login_password_error = ttk.Label(page3, text="", style="small.TLabel")
login_password_error.pack(padx=10, pady=5)

login_submit_button = ttk.Button(page3, text='Submit',  bootstyle=PRIMARY, width=15,command=login_verification)
login_submit_button.pack(padx=10, pady=10)

login_next_button = ttk.Button(page3, text="Next",bootstyle=PRIMARY, width=15, command=lambda: next_page(page4))
login_next_button.pack(pady=10)
login_next_button.config(state='disabled')

bottom_frame_login = ttk.Frame(page3, style="Custom.TFrame")
bottom_frame_login.pack(fill='x', side='bottom')
login_back_button = ttk.Button(bottom_frame_login, text="Back",bootstyle=PRIMARY, width=15, command=lambda :next_page(page1))
login_back_button.pack(pady=10,padx=10 ,side='left')

# HOME PAGE (page4)
page4 = ttk.Frame(window, style="Custom.TFrame")
page4.grid(row=0, column=0, sticky="nsew")
page4.grid_propagate(False)

home_head_label = ttk.Label(page4, text="hello "+username+"this is your HomePage", style="Header.TLabel")
home_head_label.pack(padx=10, pady=10)
pack_frame = ttk.Frame(page4, style="Custom.TFrame")
pack_frame.pack(pady=60)  # Remove fill='x' if not needed

home_upload_button = ttk.Button(pack_frame, text="Upload clothes", bootstyle=PRIMARY, width=15, command=lambda: next_page(page5))
home_upload_button.pack(side='left', padx=10)

home_closet_button = ttk.Button(pack_frame, text="Make outfits", bootstyle=PRIMARY, width=15)
home_closet_button.pack(side='left', padx=10)

home_saved_button = ttk.Button(pack_frame, text="Saved outfits", bootstyle=PRIMARY, width=15)
home_saved_button.pack(side='left', padx=10)
#--------- upload_photo_page----(page
page5=ttk.Frame(window, style="Custom.TFrame")
page5.grid(row=0, column=0, sticky="nsew")
page5.grid_propagate(False)
upload_head_label = ttk.Label(page5, text="Upload your clothes", style="Header.TLabel")
upload_head_label.pack(padx=10, pady=30)
photo_frame =Frame(page5, bg="#f7f3e6", width=600, height=600, bd=2, relief="ridge")
photo_frame.pack(padx=60 ,anchor='nw')

def upload_img():
    try:
        img_path = askopenfilename()
        print( "curr_img :"+img_path)
        print("curr_user :"+username)
        if not img_path:
            return  # User cancelled dialog

        img = Image.open(img_path)
        img_width, img_height = img.size

        # Get current frame size (in case it's dynamic)
        frame_width = photo_frame.winfo_width()
        frame_height = photo_frame.winfo_height()

        # If frame size isn't ready yet, default to 600x600
        if frame_width < 10 or frame_height < 10:
            frame_width, frame_height = 600, 600

        # Calculate scale to maintain aspect ratio and fit in frame
        scale = min(frame_width / img_width, frame_height / img_height, 1)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        if scale < 1:
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            #messagebox.showinfo(title='Attention', message="Image resized to fit the frame.")

        img_tk = ImageTk.PhotoImage(img)

        # Clear any previous images in the frame
        for widget in photo_frame.winfo_children():
            widget.destroy()

        photo_label = Label(photo_frame, image=img_tk, bg="#f7f3e6")
        photo_label.image = img_tk  # Prevent garbage collection
        photo_label.place(relx=0.5, rely=0.5, anchor="center")

    except UnidentifiedImageError:
        messagebox.showerror(title='Error', message="Please upload a valid image file.")
    except Exception as e:
        messagebox.showerror(title='Error', message=f"An unexpected error occurred: {e}")

upload_but_frame = ttk.Frame(page5, width=600, height=200, style="Custom.TFrame")
upload_but_frame.pack(padx=60, pady=10, anchor='nw')
upload_but_frame.pack_propagate(False)

upload_button = ttk.Button(upload_but_frame, text="Upload Image", bootstyle=PRIMARY, width=15 ,command= upload_img)
upload_button.pack(padx=10)

upload_back_button = ttk.Button(upload_but_frame, text="Back",bootstyle=PRIMARY, width=15, command=lambda :next_page(page4))
upload_back_button.pack(padx=1,pady=22 ,anchor='nw')
# attribute frame for clothes





# Function to raise the frame
def next_page(frame):
    if frame == page4:
        home_head_label.config(text="hello " + username + " this is your HomePage")
    frame.tkraise()

# Configure all frames
for frame in (page1, page2, page3, page4, page5):
    frame.grid(row=0, column=0, sticky="nsew")

next_page(page1)  # Start by showing the welcome page

# Run the main loop
window.mainloop()
#cahdod-duXxo7-zobroh