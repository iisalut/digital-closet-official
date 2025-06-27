
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
from tkinter import Canvas




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
style.configure('test.TFrame', background='blue')
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
style.configure("MyCustom.TCombobox",
                fieldbackground="#ffe4e1",   # Background of the field (e.g., light pink)
                background="#ffe4e1",        # Background when dropdown is open
                foreground="#333333")

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

home_inventory_button = ttk.Button(pack_frame, text="Inventory", bootstyle=PRIMARY, width=15, command=lambda: [next_page(page6), display_clothes_grid(grid_frame, username)]
)
home_inventory_button.pack(side='left', padx=10)

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

# First, create a container frame to hold both the photo frame and tags frame side by side
container_frame = ttk.Frame(page5, style="Custom.TFrame")
container_frame.pack(padx=60, expand=True, fill='both')

# Photo frame on the left
photo_frame = Frame(container_frame, bg="#f7f3e6", width=600, height=600, bd=2, relief="ridge")
photo_frame.pack(side='left', padx=(0,50))  # Add padding between frames
photo_frame.pack_propagate(False)


img_path=""
def upload_img():
    global img_path
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

upload_but_frame = ttk.Frame(page5, width=900, height=200, style="Custom.TFrame")
upload_but_frame.pack(padx=100, pady=10, anchor='nw')
upload_but_frame.pack_propagate(False)

upload_back_button = ttk.Button(upload_but_frame, text="Back",bootstyle=PRIMARY, width=15, command=lambda :next_page(page4))
upload_back_button.pack(padx=10,pady=22 ,side='left')

upload_button = ttk.Button(upload_but_frame, text="Upload Image", bootstyle=PRIMARY, width=15 ,command= upload_img)
upload_button.pack(padx=1, side='left')


def clear_all_uploads():
    # Reset dropdowns
    attribute_type.set("Choose type")
    attribute_color.set("Choose color")
    attribute_season.set("Choose season")
    attribute_occasion.set("Choose occasion")
    attribute_material.set("Choose material")

    # Clear image from photo_frame
    for widget in photo_frame.winfo_children():
        widget.destroy()

    # Clear stored image path
    global img_path
    img_path = ""
upload_clear_button = ttk.Button(upload_but_frame, text="Clear all ",width=15 ,command=clear_all_uploads)
upload_clear_button.pack(padx=10, side='left')

# attribute frame for clothes
# Tags frame on the right
upload_tags_frame = ttk.Frame(container_frame, width=500, height=600, style="Custom.TFrame")
upload_tags_frame.pack(side='left', fill='both', expand=True)
upload_tags_frame.pack_propagate(False)

mid_label = ttk.Label(upload_tags_frame, text="Tags for your clothes", style="mid.TLabel")
mid_label.pack(pady=10)

q1_label = ttk.Label(upload_tags_frame, text=" Type ?", style="small.TLabel")
q1_label.pack(pady=10)

attribute_type = StringVar(value="Choose type")
dress_type_menu = OptionMenu(upload_tags_frame, attribute_type, "Dress", "Top", "Pants", "Skirt","jacket" ,command=lambda type_value: print("type chosen : "+type_value))

dress_type_menu.pack(pady=10)
dress_type_menu.pack(pady=10)
dress_type_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)
q2_label = ttk.Label(upload_tags_frame, text=" Color ?", style="small.TLabel")
q2_label.pack(pady=10)

attribute_color = StringVar(value="Choose color")
dress_color_menu = OptionMenu(upload_tags_frame, attribute_color, "Black", "White", "Red", "Blue", "Green", "yellow", command=lambda color_value: print("color chosen ; "+color_value))

dress_color_menu.pack(pady=10)
dress_color_menu.pack(pady=10)
dress_color_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

q3_label = ttk.Label(upload_tags_frame, text=" Season ?", style="small.TLabel")
q3_label.pack(pady=10)

attribute_season = StringVar(value="Choose season")
dress_season_menu = OptionMenu(upload_tags_frame, attribute_season, "Summer", "Winter", "Fall", "Spring", command=lambda season_value: print("season chosen ; "+season_value))

dress_season_menu.pack(pady=10)
dress_season_menu.pack(pady=10)
dress_season_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

q4_label = ttk.Label(upload_tags_frame, text=" Occasion ?", style="small.TLabel")
q4_label.pack(pady=10)

attribute_occasion = StringVar(value="Choose occasion")
dress_occasion_menu = OptionMenu(upload_tags_frame, attribute_occasion, "Casual", "Work/Office", "Formal", "Party","Lounge/ Homewear", command=lambda occasion_value: print("occasion chosen ; "+occasion_value))

dress_occasion_menu.pack(pady=10)
dress_occasion_menu.pack(pady=10)
dress_occasion_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

q5_label = ttk.Label(upload_tags_frame, text=" Material ?", style="small.TLabel")
q5_label.pack(pady=10)

attribute_material = StringVar(value="Choose material")
dress_material_menu = OptionMenu(upload_tags_frame, attribute_material, "Cotton", "denim", "wool","khaki","ribbed","leather", command=lambda material_value: print("material chosen ; "+material_value))

dress_material_menu.pack(pady=10)
dress_material_menu.pack(pady=10)
dress_material_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

def save_clothing_data():
    selected_image_path = img_path
    selected_type = attribute_type.get()
    selected_color = attribute_color.get()
    selected_season = attribute_season.get()
    selected_occasion = attribute_occasion.get()
    selected_material = attribute_material.get()
    filename = "closet.json"
    data = {}

    # Load existing file if present
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    # Prepare clothing data from your app's current state
    clothing_item = {
        "image_path": selected_image_path,
        "type": selected_type,
        "color": selected_color,
        "season": selected_season,
        "occasion": selected_occasion,
        "material": selected_material
    }

    # Add under current user
    if username not in data:
        data[username] = {}

    data[username][selected_image_path]= clothing_item

    # Save updated JSON
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    msg_after_upload()

def msg_after_upload():
    saved_msg = ttk.Label(upload_tags_frame, text=" Item uploaded !", style="small.TLabel", width=15)
    saved_msg.pack(pady=2)
    window.after(1000, saved_msg.destroy)

upload_save_button= ttk.Button(upload_tags_frame,bootstyle=PRIMARY, width=15, text="Save", command=save_clothing_data )
upload_save_button.pack(pady=20)

#----------Inventory (page6)-------
page6=ttk.Frame(window, style="Custom.TFrame")
page6.grid(row=0, column=0, sticky="nsew")
page6.grid_propagate(False)

# Header at top
inventory_header = ttk.Label(page6, text="Inventory", style="Header.TLabel")
inventory_header.pack(pady=10)

# Create a canvas with scrollbar
canvas_frame = ttk.Frame(page6, style="Custom.TFrame",width=700, height=700)
canvas_frame.pack(pady=10, padx=10)

canvas = Canvas(canvas_frame, bg="beige",width=760, height=500)  # Just using Canvas since it's imported
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
grid_frame = ttk.Frame(canvas, style="Custom.TFrame")

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Pack scrollbar and canvas
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left" )

# Create a window inside the canvas with the grid_frame
canvas.create_window((0, 0), window=grid_frame, anchor="nw")

# Update scroll region when the size of grid_frame changes
def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

grid_frame.bind("<Configure>", configure_scroll_region)

# Back button at bottom
inventory_back_button = ttk.Button(page6, text="Back", bootstyle=PRIMARY,width=15,
                                 command=lambda: next_page(page4))
inventory_back_button.pack(side="bottom", pady=20)

# Optional: Bind mousewheel to scroll
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

def display_clothes_grid(grid_frame, username, json_path="closet.json", columns=4):
    from PIL import Image, ImageTk
    from tkinter import ttk

    # Clear previous widgets
    for widget in grid_frame.winfo_children():
        widget.destroy()

    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("could not load json file", e)
        return

    if username not in data:
        print("no clothing data for " + username)
        return

    items = data[username]  # dict: {image_path: tags_dict}

    for index, (image_path, tags) in enumerate(items.items()):
        new_img = image_path.strip()

        try:
            img = Image.open(new_img)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(img)

            # Capture current image_path in default argument to avoid late binding
            inventory_cloth_button = ttk.Button(
                grid_frame,
                image=photo,
                command=lambda path=new_img: open_edit_page(path)
            )
            inventory_cloth_button.image = photo

            row = index // columns
            col = index % columns
            inventory_cloth_button.grid(row=row, column=col, padx=10, pady=10)

            print("button clicked on : " + new_img)
        except Exception as e:
            print(f"could not display cloth for {new_img} :", e)

def show_detail_image(path):
    try:
        img = Image.open(path)
        img_width, img_height = img.size

        frame_width = photo_frame_edit.winfo_width() or 600
        frame_height = photo_frame_edit.winfo_height() or 600
        scale = min(frame_width / img_width, frame_height / img_height, 1)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        if scale < 1:
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img)

        # Clear previous image widgets
        for widget in photo_frame_edit.winfo_children():
            widget.destroy()

        photo_label = Label(photo_frame_edit, image=img_tk, bg="#f7f3e6")
        photo_label.image = img_tk
        photo_label.place(relx=0.5, rely=0.5, anchor="center")

    except UnidentifiedImageError:
        messagebox.showerror(title='Error', message="Invalid image file.")
    except Exception as e:
        messagebox.showerror(title='Error', message=f"Error: {e}")

def open_edit_page(image_path):
    global current_editing_path
    current_editing_path = image_path

    next_page(page7)
    show_detail_image(image_path)

    # Load JSON and get the item data
    try:
        with open("closet.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("Failed to load JSON in open_edit_page:", e)
        return

    item = data.get(username, {}).get(image_path, {})

    # Set dropdowns with saved info or default
    edit_attribute_type.set(item.get("type", "Choose type"))
    edit_attribute_color.set(item.get("color", "Choose color"))
    edit_attribute_season.set(item.get("season", "Choose season"))
    edit_attribute_occasion.set(item.get("occasion", "Choose occasion"))
    edit_attribute_material.set(item.get("material", "Choose material"))

#-----special exclusive edit page---page7
page7=ttk.Frame(window, style="Custom.TFrame")
page7.grid(row=0, column=0, sticky="nsew")
page7.grid_propagate(False)

edit_head_label = ttk.Label(page7, text="edit your upload", style="Header.TLabel")
edit_head_label.pack(padx=10, pady=30)

container_frame_edit = ttk.Frame(page7, style="Custom.TFrame")
container_frame_edit.pack(padx=60, expand=True, fill='both')

# Photo frame on the left
photo_frame_edit = Frame(container_frame_edit, bg="#f7f3e6", width=600, height=600, bd=2, relief="ridge")
photo_frame_edit.pack(side='left', padx=(0,50))  # Add padding between frames
photo_frame_edit.pack_propagate(False)

edit_back_button= ttk.Button(page7,bootstyle=PRIMARY, width=15, text="back", command=lambda:next_page(page6))
edit_back_button.pack(pady=20)
edit_frame = ttk.Frame(container_frame_edit, style="Custom.TFrame")
edit_frame.pack(padx=10, pady=30)
edit_tags_frame = ttk.Frame(edit_frame, width=500, height=600, style="Custom.TFrame")
edit_tags_frame.pack(side='left', fill='both', expand=True)
edit_tags_frame.pack_propagate(False)

edit_mid_label = ttk.Label(edit_tags_frame, text="Tags for your clothes", style="mid.TLabel")
edit_mid_label.pack(pady=10)

edit_q1_label = ttk.Label(edit_tags_frame, text=" Type ?", style="small.TLabel")
edit_q1_label.pack(pady=10)

edit_attribute_type = StringVar(value="Choose type")
edit_type_menu = OptionMenu(edit_tags_frame, edit_attribute_type, "Dress", "Top", "Pants", "Skirt","jacket" ,command=lambda type_value: print("type chosen : "+type_value))

edit_type_menu.pack(pady=10)
edit_type_menu.pack(pady=10)
edit_type_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)
edit_q2_label = ttk.Label(edit_tags_frame, text=" Color ?", style="small.TLabel")
edit_q2_label.pack(pady=10)

edit_attribute_color = StringVar(value="Choose color")
edit_color_menu = OptionMenu(edit_tags_frame, edit_attribute_color, "Black", "White", "Red", "Blue", "Green", "yellow", command=lambda color_value: print("color chosen ; "+color_value))

edit_color_menu.pack(pady=10)
edit_color_menu.pack(pady=10)
edit_color_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

edit_q3_label = ttk.Label(edit_tags_frame, text=" Season ?", style="small.TLabel")
edit_q3_label.pack(pady=10)

edit_attribute_season = StringVar(value="Choose season")
edit_season_menu = OptionMenu(edit_tags_frame,edit_attribute_season, "Summer", "Winter", "Fall", "Spring", command=lambda season_value: print("season chosen ; "+season_value))

edit_season_menu.pack(pady=10)
edit_season_menu.pack(pady=10)
edit_season_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

edit_q4_label = ttk.Label(edit_tags_frame, text=" Occasion ?", style="small.TLabel")
edit_q4_label.pack(pady=10)

edit_attribute_occasion = StringVar(value="Choose occasion")
edit_occasion_menu = OptionMenu(edit_tags_frame, edit_attribute_occasion, "Casual", "Work/Office", "Formal", "Party","Lounge/ Homewear", command=lambda occasion_value: print("occasion chosen ; "+occasion_value))

edit_occasion_menu.pack(pady=10)
edit_occasion_menu.pack(pady=10)
edit_occasion_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

edit_q5_label = ttk.Label(edit_tags_frame, text=" Material ?", style="small.TLabel")
edit_q5_label.pack(pady=10)

edit_attribute_material = StringVar(value="Choose material")
edit_material_menu = OptionMenu(edit_tags_frame, edit_attribute_material, "Cotton", "denim", "wool","khaki","ribbed","leather", command=lambda material_value: print("material chosen ; "+material_value))

edit_material_menu.pack(pady=10)
edit_material_menu.pack(pady=10)
edit_material_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

def edit_clothing_data():
    global current_editing_path  # make sure you're using the shared value
    selected_image_path = current_editing_path

    updated_type = edit_attribute_type.get()
    updated_color = edit_attribute_color.get()
    updated_season = edit_attribute_season.get()
    updated_occasion = edit_attribute_occasion.get()
    updated_material = edit_attribute_material.get()

    filename = "closet.json"

    # if not os.path.exists(filename):
    #     messagebox.showerror("Error", "Clothing data file not found.")
    #     return

    with open(filename, "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            messagebox.showerror("Error", "Could not read clothing data.")
            return

    if username not in data:
        messagebox.showerror("Error", f"No data found for user {username}.")
        return
    user_data = data[username]
    user_data[selected_image_path]["type"] = updated_type
    user_data[selected_image_path]["color"] = updated_color
    user_data[selected_image_path]["season"] = updated_season
    user_data[selected_image_path]["occasion"] = updated_occasion
    user_data[selected_image_path]["material"] = updated_material

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo("Saved", "Item updated in your closet.")
    # Optionally go back to inventory and refresh:
    # next_page(page6)
    # display_clothes_grid(grid_frame, username)
def delete_clothing_data():
    global current_editing_path  # make sure you're using the shared value
    selected_image_path = current_editing_path
    with open ("closet.json", "r") as f:
        data= json.load(f)

    print("Trying to delete:", selected_image_path)
    print("Available keys:", list(data.get(username, {}).keys()))

    if selected_image_path in data.get(username, {}):
        del data[username][selected_image_path]
    with open('closet.json', 'w') as f:
        json.dump(data, f, indent=4)

    display_clothes_grid(grid_frame, username)
    next_page(page6)



edit_save_button= ttk.Button(edit_tags_frame,bootstyle=PRIMARY, width=15, text="Save", command= edit_clothing_data)
edit_save_button.pack(pady=20)

edit_delete_button= ttk.Button(edit_tags_frame,bootstyle=PRIMARY, width=15, text="delete item", command=delete_clothing_data )
edit_delete_button.pack(pady=20)



# Function to raise the frame
def next_page(frame):
    if frame == page4:
        home_head_label.config(text="hello " + username + " this is your HomePage")
    frame.tkraise()

# Configure all frames
for frame in (page1, page2, page3, page4, page5, page6, page7):
    frame.grid(row=0, column=0, sticky="nsew")






next_page(page1)  # Start by showing the welcome page

# Run the main loop
window.mainloop()
