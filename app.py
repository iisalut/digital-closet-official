from ttkbootstrap import ttk
from ttkbootstrap.constants import *


from tkinter import *
from tkinter import messagebox, Canvas
from tkinter.filedialog import askopenfilename

import json
import os
import random
import time


from PIL import Image, ImageTk, UnidentifiedImageError, ImageGrab
import pillow_heif
pillow_heif.register_heif_opener()

import requests
from geopy.geocoders import Nominatim
import ssl
import certifi
from rembg import remove



#themed window using ttkbootstrap
window = ttk.Window(themename="flatly")
window.title("Digital Closet")

# Set window size and configure grid
window.geometry("1200x850")  # Set a specific window size
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Create a style
style = ttk.Style()
style.configure('Custom.TFrame', background='beige')
style.configure('blue.TFrame', background='#031438')

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
style.configure("mid_beige.TLabel",
                font=("Pangolin", 24),
                foreground="beige",
                background="#031438",
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
custom_user_tags=[]
edit_custom_user_tags=[]

username= ""

password=""
all_custom_tags = set()  # set avoids duplicates but tuples does not
global search_tags

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
            else:  # This else belongs to the ,for loop - runs if no break occurs
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


# ---- Global drag variables ----
drag_data = {
    "widget": None,
    "x": 0,
    "y": 0
}

def on_start_drag(event):
    widget = event.widget
    drag_data["widget"] = widget
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def on_drag_motion(event):
    widget = drag_data["widget"]
    if widget:
        x = widget.winfo_x() + event.x - drag_data["x"]
        y = widget.winfo_y() + event.y - drag_data["y"]


        x = max(0, min(x, 600 - 120))
        y = max(0, min(y, 750 - 120))

        widget.place(x=x, y=y)

def on_end_drag(event):
    drag_data["widget"] = None

#-----new  tag system-----
def add_tags_to_pool(new_tags, json_path="closet.json"):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Ensure tag_pool exists
    if "tag_pool" not in data:
        data["tag_pool"] = []

    existing_tags_lower = {tag.lower() for tag in data["tag_pool"]}

    for tag in new_tags:
        if tag.lower() not in existing_tags_lower:
            data["tag_pool"].append(tag)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
def load_search_tags(json_path="closet.json"):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        return data.get("tag_pool", [])
    except:
        return []
def ensure_tag_pool(json_path="closet.json"):
    default_tags = [
        "summer", "winter", "fall", "spring", "black", "white",
        "red", "blue", "yellow", "pink", "brown", "green",
        "pants", "denim", "jacket", "skirt", "top", "dress",
        "casual", "formal"
    ]

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if "tag_pool" not in data:
        data["tag_pool"] = default_tags.copy()
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)




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
#</editor-fold

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
#<editor-fold 1">
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
#</editor-fold>
# HOME PAGE (page4)
#<editor-fold 1">
page4 = ttk.Frame(window, style="Custom.TFrame")
page4.grid(row=0, column=0, sticky="nsew")
page4.grid_propagate(False)

home_head_label = ttk.Label(page4, text="hello "+username+"this is your HomePage", style="Header.TLabel")
home_head_label.pack(padx=10, pady=10)
pack_frame = ttk.Frame(page4, style="Custom.TFrame")
pack_frame.pack(pady=60)  # Remove fill='x' if not needed

home_upload_button = ttk.Button(pack_frame, text="Upload clothes", bootstyle=PRIMARY, width=15, command=lambda: next_page(page5))
home_upload_button.pack(side='left', padx=10)

home_inventory_button = ttk.Button(pack_frame, text="Inventory", bootstyle='primary', width=15, command=lambda: [next_page(page6), display_clothes_grid(grid_frame, username)]
)
home_inventory_button.pack(side='left', padx=10)

home_closet_button = ttk.Button(pack_frame, text="Make outfits", bootstyle=PRIMARY, width=15,
                               command=lambda: [
                                   next_page(page8),
                                   display_clothes_plangrid(plan_frame, username, plan_mini_canvas, plan_mini_canvas_images),
                                   display_clothes_plangrid(plan2_frame, username, plan_mini_canvas, plan_mini_canvas_images)
                               ])
home_closet_button.pack(side='left', padx=10)


home_saved_button = ttk.Button(pack_frame, text="Saved outfits", bootstyle=PRIMARY, width=15, command=lambda: [next_page(page9),display_saved_outfits(fit_grid_frame, fit_canvas_frame, username)])
home_saved_button.pack(side='left', padx=10)

home_bottom_frame=ttk.Frame(page4, style="blue.TFrame", width=900, height=900)
home_bottom_frame.pack( padx=10)
home_bottom_frame.pack_propagate(False)


# weather icons
weather_codes = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    71: ("Slight snow", "🌨️"),
    73: ("Moderate snow", "🌨️"),
    75: ("Heavy snow", "❄️"),
    80: ("Rain showers", "🌧️"),
    95: ("Thunderstorm", "⛈️"),
    99: ("Thunderstorm with hail", "⛈️❄️")
}

def get_lat_lon(city):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    geolocator = Nominatim(user_agent="weather_app", ssl_context=ssl_context)
    location = geolocator.geocode(city)
    if not location:
        raise ValueError("City not found.")
    return location.latitude, location.longitude, location.address

def fetch_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )
    resp = requests.get(url)
    return resp.json()

def search_weather():
    city = weather_entry.get().strip()
    if not city:
        messagebox.showwarning("Missing Input", "Please enter a city.")
        return

    try:
        #  Get lat/lon from the city
        lat, lon, location_name = get_lat_lon(city)

        # need to Fetch weather data
        data = fetch_weather(lat, lon)
        current = data.get("current_weather", {})
        temperature = current.get("temperature")
        code = current.get("weather code")

        # Get description and emoji
        description, emoji = weather_codes.get(code, ("Unknown", "❓"))

        # Update UI labels
        weather_location_text.config(text=location_name)
        weather_temperature_text.config(text=f"{temperature}°C")
        weather_info_text.config(text=description)
        weather_image.config(text=emoji, font=("Arial", 48))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather:\n{e}")



weather_frame = ttk.Frame(home_bottom_frame, style="Custom.TFrame",width=950, height=350)
weather_frame.pack(anchor='w',padx=10,pady=10)
weather_frame.pack_propagate(False)
weather_head= ttk.Label(weather_frame, text="Weather Updates", style="mid.TLabel")
weather_head.pack(padx=10, pady=10)

weather_text1=ttk.Label(weather_frame, text="Enter your city !", style="small.TLabel")
weather_text1.pack(padx=10, pady=1)

weather_entry_frame=ttk.Frame(weather_frame, style="Custom.TFrame")
weather_entry_frame.pack(pady=10)

weather_entry= ttk.Entry(weather_entry_frame, width=15)
weather_entry.pack(padx=10, pady=2, side='left')

weather_search_button=ttk.Button(weather_entry_frame,width=2,text="🔍")
weather_search_button.pack(pady=10,side='right')
weather_search_button.config(command=search_weather)

weather_location_text=ttk.Label(weather_frame, text="Location", style="mid.TLabel")
weather_location_text.pack(padx=10, pady=1)

weather_image= ttk.Label(weather_frame)
weather_image.pack(padx=10, pady=3)

weather_temperature_text=ttk.Label(weather_frame, text="Temperature", style="mid.TLabel")
weather_temperature_text.pack(padx=10, pady=1)

weather_info_text=ttk.Label(weather_frame, text="weather Info", style="mid.TLabel")
weather_info_text.pack(padx=10, pady=1)

#----color palette challenge !!-------

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

style = ttk.Style()

def generate_palette():
    for widget in color_palette_swatch_frame.winfo_children():
        widget.destroy()

    for i in range(3):
        color = random_color()

        style_name = f"Color{i}.TFrame"
        style.configure(style_name, background=color, relief="raised")

        swatch = ttk.Frame(color_palette_swatch_frame, style=style_name, width=90, height=130)
        swatch.grid(row=0, column=i, padx=2, pady=2)
        swatch.grid_propagate(False)

        label = ttk.Label(color_palette_swatch_frame, text=color, style="small.TLabel")
        label.grid(row=1, column=i, pady=3)


# Challenge frame
challenge_frame = ttk.Frame(home_bottom_frame, style="Custom.TFrame", height=400, width=950, relief="solid", borderwidth=1)
challenge_frame.pack(padx=10, fill="x")  # fill horizontal



challenge_text1=ttk.Label(challenge_frame, text="Fun Challenges !", style="mid.TLabel")
challenge_text1.pack(padx=10, pady=1)

# Color palette on the left
color_palette_frame = ttk.Frame(challenge_frame, style="blue.TFrame", width=450, height=300, relief="solid", borderwidth=1)
color_palette_frame.pack(side="left", padx=10, pady=10)
color_palette_frame.pack_propagate(False)  # let it expand to children

color_palette_text1=ttk.Label(color_palette_frame, text="palette generator", style="mid_beige.TLabel")
color_palette_text1.pack(padx=10, pady=1)
color_palette_swatch_frame = ttk.Frame(color_palette_frame)
color_palette_swatch_frame.pack(pady=10)
color_palette_btn = ttk.Button(color_palette_frame, text="Generate Colors",command=generate_palette)
color_palette_btn.pack(pady=5)

# ---- Aesthetic Generator ----

aesthetic_words = [
    "Cottage Core",
    "Dark Acadamia",
    "Minimalistic",
    "Maximalistic",
    "Acubi Style",
    "Goth Style",
    "Sporty"

]

aesthetic_images=[
    "build/app/aesthetic_images/cottage_core.jpg",
    "build/app/aesthetic_images/dark_academia.jpg",
    "build/app/aesthetic_images/minimalistic.jpg",
    "build/app/aesthetic_images/maximalistic.jpg",
    "build/app/aesthetic_images/acubi.jpg",
    "build/app/aesthetic_images/ goth.jpg",
    "build/app/aesthetic_images/ sporty.jpg"
]

aesthetic_generator_outer = ttk.Frame(challenge_frame, style="blue.TFrame", width=400, height=300, relief="solid", borderwidth=1)
aesthetic_generator_outer.pack(side="right", padx=10, pady=10)
aesthetic_generator_outer.pack_propagate(False)


aesthetic_generator_text1 = ttk.Label(aesthetic_generator_outer, text="Aesthetic Generator", style="mid_beige.TLabel")
aesthetic_generator_text1.pack(pady=5)


display_frame = ttk.Frame(aesthetic_generator_outer,style="Custom.TFrame")
display_frame.pack(expand=True, fill="both", pady=10, padx=10)

button_frame = ttk.Frame(aesthetic_generator_outer)
button_frame.pack(pady=5)


def generate_aesthetic_word():

    for widget in display_frame.winfo_children():
        widget.destroy()
    index=random.randint(0,len(aesthetic_words)-1)
    word=aesthetic_words[index]
    image_path=aesthetic_images[index]

    img= Image.open(image_path)
    img=img.resize((120,120), Image.Resampling.LANCZOS)
    photo=ImageTk.PhotoImage(img)
    image_label=ttk.Label(display_frame, image=photo)
    image_label.image = photo
    image_label.pack()

    label=ttk.Label(display_frame, text=word, style="mid.TLabel")
    label.pack(pady=5)

aesthetic_generator_btn = ttk.Button(button_frame, text="Generate Aesthetic", command=generate_aesthetic_word)
aesthetic_generator_btn.pack()


#</editor-fold>

#--------- upload_photo_page----(page5)
#<editor-fold 1">
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
        print("curr_img: " + img_path)
        print("curr_user: " + username)
        if not img_path:
            return

        # heic to png conversion
        if img_path.lower().endswith(".heic"):
            img = Image.open(img_path)
            png_path = os.path.splitext(img_path)[0] + ".png"
            img.save(png_path)
            img_path = png_path  # updates path to PNG version

        img = Image.open(img_path)


        # 1. Remove bg (used Hoverboard Cube's code as reference)
        with open(img_path, "rb") as f:
            input_img = f.read()
        output_img_bytes = remove(input_img)

        # Save to a temporary transparent image file
        transparent_output_path = os.path.splitext(img_path)[0] + "_transparent.png"
        with open(transparent_output_path, "wb") as out_file:
            out_file.write(output_img_bytes)

        #  Open the saved transparent image
        img = Image.open(transparent_output_path).convert("RGBA")

        # 3. Resize to fit frame
        frame_width = photo_frame.winfo_width() or 600
        frame_height = photo_frame.winfo_height() or 600
        scale = min(frame_width / img.width, frame_height / img.height, 1)
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)

        img_path = transparent_output_path

        img_tk = ImageTk.PhotoImage(img)
        for widget in photo_frame.winfo_children():
            widget.destroy()
        photo_label = Label(photo_frame, image=img_tk, bg="#f7f3e6")
        photo_label.image = img_tk
        photo_label.place(relx=0.5, rely=0.5, anchor="center")

    except UnidentifiedImageError:
        messagebox.showerror(title='Error', message="Please upload a valid image file.")
    except Exception as e:
        messagebox.showerror(title='Error', message=f"An unexpected error occurred: {e}")

upload_but_frame = ttk.Frame(page5, width=700, height=200, style="Custom.TFrame")
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

    custom_user_tags.clear()
    for widget in custom_tags_display.winfo_children():
        widget.destroy()

    # Clear stored image path
    global img_path
    img_path = ""
upload_clear_button = ttk.Button(upload_but_frame, text="Clear all ",width=15 ,command=clear_all_uploads)
upload_clear_button.pack(padx=10, side='left')

# attribute frame for clothes
# Tags frame on the right
upload_tags_frame = ttk.Frame(container_frame, width=500, height=700, style="Custom.TFrame")
upload_tags_frame.pack(side='left', fill='both', expand=True)
upload_tags_frame.pack_propagate(False)

q1_label = ttk.Label(upload_tags_frame, text=" Type ?", style="small.TLabel")
q1_label.pack(pady=10)

attribute_type = StringVar(value="Choose type")
dress_type_menu = OptionMenu(upload_tags_frame, attribute_type, "Dress", "---","Top", "Pants", "Skirt","jacket" ,command=lambda type_value: print("type chosen : "+type_value))

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
dress_color_menu = OptionMenu(upload_tags_frame, attribute_color, "---","Black", "White", "Red", "Blue", "Green", "yellow", command=lambda color_value: print("color chosen ; "+color_value))

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
dress_season_menu = OptionMenu(upload_tags_frame, attribute_season, "---","Summer", "Winter", "Fall", "Spring", command=lambda season_value: print("season chosen ; "+season_value))

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
dress_occasion_menu = OptionMenu(upload_tags_frame, attribute_occasion, "---","Casual", "Work/Office", "Formal", "Party","Lounge/ Home wear", command=lambda occasion_value: print("occasion chosen ; "+occasion_value))

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
dress_material_menu = OptionMenu(upload_tags_frame, attribute_material, "---","Cotton", "denim", "wool","khaki","ribbed","leather", command=lambda material_value: print("material chosen ; "+material_value))

dress_material_menu.pack(pady=10)
dress_material_menu.pack(pady=10)
dress_material_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)
def add_custom_tag():
    tag = custom_tag_entry.get().strip()
    if tag and tag not in custom_user_tags:
        custom_user_tags.append(tag)

        #
        tag_frame = Frame(custom_tags_display, bg="#f7f3e6", bd=0)
        tag_frame.pack(side="left", padx=5, pady=2)

        # Tag label
        tag_label = Label(tag_frame, text=tag, bg="#d9e2ec", font=("Pangolin", 10), padx=10, pady=5, relief="ridge")
        tag_label.pack(side="left")

        # "x" icon
        remove_btn = Button(tag_frame, text="✕", font=("Arial", 10), bg="#f7f3e6", fg="red", bd=0, relief="flat", command=lambda: remove_custom_tag(tag, tag_frame))
        remove_btn.pack(side="left", padx=(2, 0))

        custom_tag_entry.delete(0, END)


q6_label = ttk.Label(upload_tags_frame, text="Custom Tags", style="small.TLabel")
q6_label.pack(pady=10)

def show_custom_tag_suggestions(event=None):
    user_input = custom_tag_entry.get().lower()
    autocomplete_listbox.delete(0, END)

    if not user_input:
        autocomplete_listbox.place_forget()
        return

    matches = [tag for tag in search_tags if user_input in tag.lower()]
    if matches:
        for tag in matches:
            autocomplete_listbox.insert(END, tag)
        autocomplete_listbox.place(
            x=custom_tag_entry.winfo_x(),
            y=custom_tag_entry.winfo_y() + custom_tag_entry.winfo_height()
        )
        autocomplete_listbox.lift()
    else:
        autocomplete_listbox.place_forget()

def select_custom_tag_suggestion(event=None):
    selection = autocomplete_listbox.curselection()
    if selection:
        selected_tag = autocomplete_listbox.get(selection[0])
        custom_tag_entry.delete(0, END)
        custom_tag_entry.insert(0, selected_tag)
        autocomplete_listbox.place_forget()

def confirm_custom_tag(event=None):
    value = custom_tag_entry.get().strip().lower()
    if value:
        if value not in search_tags:
            search_tags.append(value)
            print(f"Added '{value}' to search_tags")  # Debug/log
        else:
            print(f"'{value}' already in search_tags")  # Optional
    autocomplete_listbox.place_forget()
    custom_tag_entry.delete(0, END)

custom_tag_entry = Entry(upload_tags_frame, width=20)
custom_tag_entry.pack(pady=5)

autocomplete_listbox = Listbox(upload_tags_frame, height=3)
autocomplete_listbox.place_forget()

custom_tag_entry.bind('<KeyRelease>', show_custom_tag_suggestions)
custom_tag_entry.bind('<Return>', confirm_custom_tag)
autocomplete_listbox.bind('<<ListboxSelect>>', select_custom_tag_suggestion)


add_tag_button = ttk.Button(upload_tags_frame, text="Add Tag", width=10, bootstyle="secondary", command=add_custom_tag)
add_tag_button.pack(pady=5)

custom_tags_display = Frame(upload_tags_frame, bg="#f7f3e6")
custom_tags_display.pack(pady=5)
def remove_custom_tag(tag, tag_frame):
    if tag in custom_user_tags:
        custom_user_tags.remove(tag)
    tag_frame.destroy()  # Removes the UI for this tag search

def save_clothing_data():
    selected_image_path = img_path
    selected_type = attribute_type.get()
    selected_color = attribute_color.get()
    selected_season = attribute_season.get()
    selected_occasion = attribute_occasion.get()
    selected_material = attribute_material.get()
    filename = "closet.json"
    data = {}

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    # Add official tags
    official_tags = [selected_type, selected_color, selected_season, selected_occasion, selected_material]
    all_tags = []

    for tag in official_tags:
        tag = tag.strip().lower()
        if tag:
            all_tags.append(tag)
            if tag not in search_tags:
                search_tags.append(tag)

    # Add custom tags
    for tag in custom_user_tags:
        if tag:
            all_tags.append(tag)
            if tag not in search_tags:
                search_tags.append(tag)


    if "tag_pool" not in data:
        data["tag_pool"] = []

    current_pool = {t.lower() for t in data["tag_pool"]}
    for tag in all_tags:
        if tag.lower() not in current_pool:
            data["tag_pool"].append(tag)

    # Clothing item dictionary
    clothing_item = {
        "image_path": selected_image_path,
        "type": selected_type,
        "color": selected_color,
        "season": selected_season,
        "occasion": selected_occasion,
        "material": selected_material,
        "custom_tags": custom_user_tags[:]
    }

    if username not in data:
        data[username] = {}

    data[username][selected_image_path] = clothing_item

    # Save everything
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    msg_after_upload()


def msg_after_upload():
    saved_msg = ttk.Label(upload_tags_frame, text=" Item uploaded !", style="small.TLabel", width=15)
    saved_msg.pack(pady=2)
    window.after(1000, saved_msg.destroy)

upload_save_button= ttk.Button(upload_tags_frame,bootstyle=PRIMARY, width=15, text="Save", command=save_clothing_data )
upload_save_button.pack(pady=20)
#</editor-fold>
#----------Inventory (page6)-------
#<editor-fold 1">
page6=ttk.Frame(window, style="Custom.TFrame")
page6.grid(row=0, column=0, sticky="nsew")
#page6.grid_propagate(False)

# Header at top

inventory_header = ttk.Label(page6, text="Inventory", style="Header.TLabel")
inventory_header.pack(pady=0)

inventory_search_frame = ttk.Frame(page6,width=500, height=100,style="Custom.TFrame")
inventory_search_frame.pack(pady=10, padx=0)
inventory_search_frame.pack_propagate(False)
# creating autocomplete search bar

def show_suggestions(event=None):
    user_input= inventory_entry.get().lower()
    autocomplete_Listbox.delete(0, END)

    if user_input =="":
        autocomplete_Listbox.place_forget()
        return

    matches=[]
    for tag in search_tags:
        if user_input in tag.lower():
            matches.append(tag)
    if matches:
        for tag in matches:
            autocomplete_Listbox.insert(END, tag)

        # places listbox under entry
        autocomplete_Listbox.place(
            x=inventory_entry.winfo_x(),
            y=inventory_entry.winfo_y()+inventory_entry.winfo_height(
            )
        )
        autocomplete_Listbox.lift()
    else:
        autocomplete_Listbox.place_forget()
def select_suggestions(event):
    selection= autocomplete_Listbox.curselection()
    if selection:
        selected_tag = autocomplete_Listbox.get(selection[0])
        inventory_entry.delete(0, END)
        inventory_entry.insert(0, selected_tag)
        autocomplete_Listbox.place_forget()

inventory_entry = ttk.Entry(inventory_search_frame, width=30)
inventory_entry.pack(pady=10,side="left" )
inventory_entry.bind("<KeyRelease>", show_suggestions)

def search_inventory():
    selected_tag = inventory_entry.get().strip().lower()
    if selected_tag == "":
        # If no search, show all items
        display_clothes_grid(grid_frame, username=username)
    else:
        display_filtered_clothes(grid_frame, username=username, selected_tag=selected_tag)


def display_clothes_plangrid(grid_frame, username, target_canvas, target_images_list, json_path="closet.json", columns=2):
    # Clear previous widgets
    for widget in grid_frame.winfo_children():
        widget.destroy()

    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("Could not load JSON file:", e)
        return

    if username not in data:
        print("No clothing data for", username)
        return

    items = data[username]  # dict: {image_path: tags_dict}

    row = 0
    col = 0

    for image_path, tags in items.items():
        new_img = image_path.strip()

        try:
            print("Trying to open:", new_img)
            img = Image.open(new_img).convert('RGBA')
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            inventory_cloth_label = Label(
                grid_frame,
                image=photo,
                cursor="hand2"
            )

            inventory_cloth_label.image = photo
            inventory_cloth_label.grid(row=row, column=col, padx=10, pady=10)

            def clone_to_planner_on_canvas(event, img_path, canvas=target_canvas, images_list=target_images_list):
                try:
                    img = Image.open(img_path).convert("RGBA")
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    images_list.append(photo)  # Use the passed images list

                    if img_path.strip() not in used_items:
                        used_items.append(img_path.strip())

                    width = canvas.winfo_width()
                    height = canvas.winfo_height()

                    x = random.randint(0, max(0, width - 150))
                    y = random.randint(0, max(0, height - 150))

                    image_id = canvas.create_image(x, y, image=photo, anchor="nw")  # Use passed canvas

                    def start_drag(e, id=image_id):
                        canvas._drag_data = (id, e.x, e.y)

                    def on_drag(e):
                        item_id, start_x, start_y = canvas._drag_data
                        dx = e.x - start_x
                        dy = e.y - start_y
                        canvas.move(item_id, dx, dy)
                        canvas._drag_data = (item_id, e.x, e.y)

                    def on_double_click(e, id=image_id):
                        canvas.delete(id)
                        # Remove from used_items
                        if img_path.strip() in used_items:
                            used_items.remove(img_path.strip())


                        global currently_loaded_snapshot
                        if currently_loaded_snapshot:
                            with open("closet.json", 'r') as file:
                                data = json.load(file)
                                if username in data and "outfits" in data[username]:
                                    if currently_loaded_snapshot in data[username]["outfits"]:
                                        outfit_items = data[username]["outfits"][currently_loaded_snapshot]
                                        if img_path.strip() in outfit_items:
                                            outfit_items.remove(img_path.strip())
                                        with open("closet.json", 'w') as file:
                                            json.dump(data, file, indent=4)
                                        print(f"Removed {img_path.strip()} from outfit")



                    canvas.tag_bind(image_id, "<Button-1>", start_drag)
                    canvas.tag_bind(image_id, "<B1-Motion>", on_drag)
                    canvas.tag_bind(image_id, "<Double-Button-1>", on_double_click)
                    canvas.tag_bind(image_id, "<Command-Button-1>",lambda e, id=image_id, path=img_path: show_resize_options(id, path, canvas,images_list))

                except Exception as e:
                    print("Error cloning to canvas:", e)

            # Bind click event
            inventory_cloth_label.bind("<Button-1>", lambda e, p=new_img: clone_to_planner_on_canvas(e, p))

            print("Displayed label for:", new_img)

            col += 1
            if col >= columns:
                col = 0
                row += 1

        except Exception as e:
            print(f"Could not display cloth for {new_img}:", e)

def display_filtered_clothes(grid_frame, username, selected_tag, json_path="closet.json", columns=4):
    # Clear previous results
    for widget in grid_frame.winfo_children():
        widget.destroy()

    # Load data
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("Could not load JSON file:", e)
        return

    if username not in data:
        print("No clothing data for", username)
        return

    selected_tag = selected_tag.lower().strip()
    items = data[username]
    filtered_items = {}

    for image_path, tags in items.items():
        tag_list = []

        # Collect all values as lowercase strings
        if isinstance(tags, dict):
            for key, value in tags.items():
                if key == "custom_tags" and isinstance(value, list):
                    tag_list.extend([str(v).lower() for v in value])
                else:
                    tag_list.append(str(value).lower())
        elif isinstance(tags, list):
            tag_list = [str(value).lower() for value in tags]
        else:
            tag_list = []

        # Check if the selected tag exists in any tag
        if selected_tag in tag_list:
            filtered_items[image_path] = tags

    # Display filtered items in grid
    for index, (image_path, tags) in enumerate(filtered_items.items()):
        try:
            img = Image.open(image_path.strip())
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            btn = ttk.Button(
                grid_frame,
                image=photo,
                command=lambda path=image_path: open_edit_page(path)
            )
            btn.image = photo

            row = index // columns
            col = index % columns
            btn.grid(row=row, column=col, padx=10, pady=10)

        except Exception as e:
            print(f"Error loading {image_path}:", e)

    if not filtered_items:
        print("No results found for:", selected_tag)


def display_filtered_clothes_plan(grid_frame, center_frame, username, selected_tag, json_path="closet.json", columns=4):
    for widget in grid_frame.winfo_children():
        widget.destroy()

    # Load data
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("Could not load JSON file:", e)
        return

    if username not in data:
        print("No clothing data for", username)
        return

    selected_tag = selected_tag.lower().strip()
    items = data[username]
    filtered_items = {}

    for image_path, tags in items.items():
        tag_list = []

        if isinstance(tags, dict):
            for key, value in tags.items():
                if key == "custom_tags" and isinstance(value, list):
                    tag_list.extend([str(v).lower() for v in value])
                else:
                    tag_list.append(str(value).lower())
        elif isinstance(tags, list):
            tag_list = [str(value).lower() for value in tags]

        if selected_tag in tag_list:
            filtered_items[image_path] = tags

    row = 0
    col = 0

    for image_path, tags in filtered_items.items():
        try:
            new_img = image_path.strip()
            img = Image.open(new_img).convert("RGBA")
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = Label(grid_frame, image=photo, cursor="hand2")
            label.image = photo
            label.grid(row=row, column=col, padx=10, pady=10)

            # FIX: Create a proper closure to capture the image path
            def make_clone_function(img_path):
                def clone_to_planner_on_canvas(event):
                    try:
                        img = Image.open(img_path).convert("RGBA")
                        img = img.resize((150, 150), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)

                        # FIXED: Use the correct canvas reference
                        fit_plan_mini_canvas_images.append(photo)

                        # FIXED: Add to used_items tracking
                        if img_path.strip() not in used_items:
                            used_items.append(img_path.strip())

                        width = fit_plan_mini_canvas.winfo_width()
                        height = fit_plan_mini_canvas.winfo_height()

                        x = random.randint(0, max(0, width - 150))
                        y = random.randint(0, max(0, height - 150))

                        image_id = fit_plan_mini_canvas.create_image(x, y, image=photo, anchor="nw")

                        def start_drag(e, id=image_id):
                            fit_plan_mini_canvas._drag_data = (id, e.x, e.y)

                        def on_drag(e):
                            item_id, start_x, start_y = fit_plan_mini_canvas._drag_data
                            dx = e.x - start_x
                            dy = e.y - start_y
                            fit_plan_mini_canvas.move(item_id, dx, dy)
                            fit_plan_mini_canvas._drag_data = (item_id, e.x, e.y)

                        def on_double_click(e, id=image_id):
                            fit_plan_mini_canvas.delete(id)
                            # FIXED: Remove from used_items when deleted
                            if img_path.strip() in used_items:
                                used_items.remove(img_path.strip())

                        fit_plan_mini_canvas.tag_bind(image_id, "<Button-1>", start_drag)
                        fit_plan_mini_canvas.tag_bind(image_id, "<B1-Motion>", on_drag)
                        fit_plan_mini_canvas.tag_bind(image_id, "<Double-Button-1>", on_double_click)

                    except Exception as e:
                        print("Error cloning to canvas:", e)

                return clone_to_planner_on_canvas

            # FIXED: Use the closure function
            label.bind("<Button-1>", make_clone_function(new_img))

            col += 1
            if col >= columns:
                col = 0
                row += 1

        except Exception as e:
            print(f"Error displaying filtered item {image_path}:", e)

    if not filtered_items:
        print("No results found for:", selected_tag)

#--------- snapshot feature----
used_items = [] # stores current cloth items :D

currently_loaded_snapshot = None  # Global tracker for deleting old snapshot

def take_snapshot(widget, username, json_path="closet.json"):
    plan_mini_canvas.update()
    x = plan_mini_canvas.winfo_rootx()
    y = plan_mini_canvas.winfo_rooty()
    w = x + plan_mini_canvas.winfo_width()
    h = y +plan_mini_canvas.winfo_height()

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"snapshot_{username}_outfit_{timestamp}.png"


    snapshot = ImageGrab.grab(bbox=(x, y, w, h))
    snapshot.save(filename)


    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if username not in data:
        data[username] = {}

    if "outfits" not in data[username] or not isinstance(data[username]["outfits"], dict):
        data[username]["outfits"] = {}


    global currently_loaded_snapshot
    if currently_loaded_snapshot:
        old_file = currently_loaded_snapshot
        try:
            os.remove(old_file)
            print(f"Deleted old snapshot: {old_file}")
        except:
            print(f"Could not delete old file: {old_file}")
        data[username]["outfits"].pop(old_file, None)
        currently_loaded_snapshot = None  # Reset after deleting


    data[username]["outfits"][filename] = used_items.copy()

    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo("Saved", f"Outfit saved as {filename}")

    print (used_items)

def clear_outfit_frame():
    plan_mini_canvas.delete("all")
    used_items.clear()
    global currently_loaded_snapshot
    currently_loaded_snapshot = None
    messagebox.showinfo("Cleared", "Outfit cleared")


def display_saved_outfits(grid_frame, display_frame, username, json_path="closet.json", columns=2):

    # Clear previous widgets
    for widget in grid_frame.winfo_children():
        widget.destroy()

    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        # Check if user exists
        if username not in data:
            print(f"Username '{username}' not found in data.")
            return

        user_data = data[username]

        # Check if outfits exist for this user
        if "outfits" not in user_data:
            print(f"No outfits found for user '{username}'.")
            return

        outfits = user_data["outfits"]

        # Iterate through outfits
        for index, (snapshot_name, outfit_clothes_paths) in enumerate(outfits.items()):
            print(f"Outfit {index+1}: {snapshot_name} with {len(outfit_clothes_paths)} items")

            try:
                # Load snapshot image (the outfit's saved snapshot image)
                img = Image.open(snapshot_name.strip())
                img = img.resize((300, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                frame = ttk.Frame(grid_frame)
                frame.grid(row=index // columns, column=index % columns, padx=10, pady=10)

                def on_snapshot_click(key=snapshot_name):
                    load_outfit(key, display_frame=fit_plan_mini_canvas, username=username)
                    display_clothes_plangrid(fit_plan_frame, username, fit_plan_mini_canvas,
                                             fit_plan_mini_canvas_images)
                    display_clothes_plangrid(fit_plan2_frame, username, fit_plan_mini_canvas,
                                             fit_plan_mini_canvas_images)

                btn = ttk.Button(
                    frame,
                    image=photo,
                    command= on_snapshot_click

                )
                btn.image = photo  # Keep a reference!
                btn.pack()
            except Exception as e:
                print(f"Error loading snapshot image '{snapshot_name}':", e)

    except Exception as e:
        print("Error loading JSON file or parsing data:", e)



# Drag state tracking
drag_data = {
    "widget": None,
    "x": 0,
    "y": 0
}


def show_resize_options(image_id, img_path, canvas, images_list):
    # no more simple dialog :(

    # ---------stylizing the dialog box----------(watched yt tutorial)
    dialog = Toplevel()
    dialog.title("Resize options")
    dialog.geometry("300x300")
    dialog.resizable(False, False)
    dialog.transient()  # allows it to stay on top of main window !!
    dialog.grab_set()  # allows interaction
    selected_size = None
    ttk.Label(dialog, text="Choose a size").pack(pady=20)

    def select_small():
        nonlocal selected_size  # Use nonlocal instead of global
        selected_size = (100, 100)
        dialog.destroy()

    def select_medium():
        nonlocal selected_size
        selected_size = (200, 200)
        dialog.destroy()

    def select_large():
        nonlocal selected_size
        selected_size = (300, 300)
        dialog.destroy()

    ttk.Button(dialog, text="Small", command=select_small, width=20).pack(pady=5)
    ttk.Button(dialog, text="Medium", command=select_medium, width=20).pack(pady=5)
    ttk.Button(dialog, text="Large", command=select_large, width=20).pack(pady=5)
    ttk.Button(dialog, text="Cancel", command=dialog.destroy, width=20).pack(pady=10)

    dialog.wait_window()
    if selected_size is None:
        return

    new_size = selected_size

    try:
        img = Image.open(img_path).convert("RGBA")
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        images_list.append(photo)

        coords = canvas.coords(image_id)
        x, y = coords[0], coords[1]

        canvas.delete(image_id)
        new_image_id = canvas.create_image(x, y, image=photo, anchor="nw")

        # Re-bind events
        def start_drag(e, id=new_image_id):
            canvas._drag_data = (id, e.x, e.y)

        def on_drag(e):
            if hasattr(canvas, '_drag_data'):
                item_id, start_x, start_y = canvas._drag_data
                dx = e.x - start_x
                dy = e.y - start_y
                canvas.move(item_id, dx, dy)
                canvas._drag_data = (item_id, e.x, e.y)

        def on_double_click(e, id=new_image_id):
            canvas.delete(id)
            if img_path.strip() in used_items:
                used_items.remove(img_path.strip())

        canvas.tag_bind(new_image_id, "<Button-1>", start_drag)
        canvas.tag_bind(new_image_id, "<B1-Motion>", on_drag)
        canvas.tag_bind(new_image_id, "<Double-Button-1>", on_double_click)
        canvas.tag_bind(new_image_id, "<Command-Button-1>",
                        lambda e, id=new_image_id, path=img_path: show_resize_options(id, path, canvas, images_list))


    except Exception as e:
        messagebox.showerror("Error", f"Failed to resize image: {e}")



def load_outfit(snapshot_key, display_frame, username, json_path="closet.json"):
    global currently_loaded_snapshot, used_items, fit_plan_mini_canvas_images
    currently_loaded_snapshot = snapshot_key

    # ---- Switch to page10 ----
    page10.tkraise()

    # ---- Clear current outfit ----
    fit_plan_mini_canvas.delete("all")  # Use delete instead of destroying children
    used_items.clear()
    fit_plan_mini_canvas_images.clear()

    # ---- Load the outfit ----
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            outfit_paths = data[username]["outfits"].get(snapshot_key, [])
    except Exception as e:
        print("Error loading outfit:", e)
        return

    for path in outfit_paths:
        try:
            img = Image.open(path.strip()).convert("RGBA")
            img = img.resize((150, 150), Image.Resampling.LANCZOS)

            # Create transparent background and paste with alpha
            transparent_bg = Image.new("RGBA", img.size, (0, 0, 0, 0))
            transparent_bg.paste(img, (0, 0), img)
            img_tk = ImageTk.PhotoImage(transparent_bg)

            # Random position
            import random
            x = random.randint(100, 300)
            y = random.randint(100, 300)

            # Add image to canvas
            canvas_id = fit_plan_mini_canvas.create_image(x, y, image=img_tk, anchor="nw")
            fit_plan_mini_canvas_images.append(img_tk)  # Prevent garbage collection
            used_items.append(path.strip())

            # --- Make draggable ---
            def on_drag(event, cid=canvas_id):
                fit_plan_mini_canvas.coords(cid,
                    event.x - 75,
                    event.y - 75
                )

            # --- Make deletable ---
            def on_right_click(event, cid=canvas_id, p=path.strip()):
                if messagebox.askyesno("Delete", "Do you want to delete this item?"):
                    if p in used_items:
                        used_items.remove(p)
                    fit_plan_mini_canvas.delete(cid)


            fit_plan_mini_canvas.tag_bind(canvas_id, "<B1-Motion>", on_drag)
            fit_plan_mini_canvas.tag_bind(canvas_id, "<Double-Button-1>", on_right_click)
            fit_plan_mini_canvas.tag_bind(canvas_id, "<Command-Button-1>",lambda e, id=canvas_id, p=path.strip(): show_resize_options(id, p,fit_plan_mini_canvas,fit_plan_mini_canvas_images))

        except Exception as e:
            print(f"Error displaying item {path}:", e)



inventory_search_button= ttk.Button(inventory_search_frame,text="search", width=5, command=search_inventory)
inventory_search_button.pack(pady=10, side="left")

inventory_clear_button= ttk.Button(inventory_search_frame,text="clear filters", width=8, command= lambda : display_clothes_grid(grid_frame, username))
inventory_clear_button.pack(pady=10, side="right", padx=10)

search_tags=load_search_tags()
autocomplete_Listbox=Listbox(inventory_search_frame,height=3)

autocomplete_Listbox.bind("<<ListboxSelect>>", select_suggestions)

# Create a canvas with scrollbar
canvas_frame = ttk.Frame(page6, style="Custom.TFrame",width=700, height=700)
canvas_frame.pack(pady=10, padx=0, )

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

    # Clear previous widgets
    for widget in grid_frame.winfo_children():
        widget.destroy()

    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("Could not load JSON file:", e)
        return

    if username not in data:
        print("No clothing data for", username)
        return

    items = data[username]  # dict: {image_path: tags_dict}

    row = 0
    col = 0

    for image_path, tags in items.items():
        new_img = image_path.strip()

        try:
            print("Trying to open:", new_img)
            img = Image.open(new_img)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            inventory_cloth_button = ttk.Button(
                grid_frame,
                image=photo,
                command=lambda path=new_img: open_edit_page(path)
            )
            inventory_cloth_button.image = photo  # prevent image from being garbage collected
            inventory_cloth_button.grid(row=row, column=col, padx=10, pady=10)

            print("Displayed button for:", new_img)

            col += 1
            if col >= columns:
                col = 0
                row += 1

        except Exception as e:
            print(f"Could not display cloth for {new_img}:", e)


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

    load_edit_custom_tags(item.get("custom_tags", []))


def load_edit_custom_tags(tag_list):
    global edit_custom_user_tags
    edit_custom_user_tags.clear()
    for widget in edit_custom_tags_display.winfo_children():
        widget.destroy()

    for tag in tag_list:
        edit_custom_user_tags.append(tag)
        tag_frame = Frame(edit_custom_tags_display, bg="#f7f3e6", bd=0)
        tag_frame.pack(side="left", padx=5, pady=2)

        tag_label = Label(tag_frame, text=tag, bg="#d9e2ec", font=("Pangolin", 10), padx=10, pady=5, relief="ridge")
        tag_label.pack(side="left")

        remove_btn = Button(tag_frame, text="✕", font=("Arial", 10), bg="#f7f3e6", fg="red", bd=0, relief="flat",
                            command=lambda t=tag, f=tag_frame: remove_edit_custom_tag(t, f))
        remove_btn.pack(side="left", padx=(2, 0))



def display_filtered_clothes_plan_page8(grid_frame, center_frame, username, selected_tag, json_path="closet.json",
                                        columns=4):
    for widget in grid_frame.winfo_children():
        widget.destroy()

    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("Could not load JSON file:", e)
        return

    if username not in data:
        print("No clothing data for", username)
        return

    selected_tag = selected_tag.lower().strip()
    items = data[username]
    filtered_items = {}

    for image_path, tags in items.items():
        tag_list = []

        if isinstance(tags, dict):
            for key, value in tags.items():
                if key == "custom_tags" and isinstance(value, list):
                    tag_list.extend([str(v).lower() for v in value])
                else:
                    tag_list.append(str(value).lower())
        elif isinstance(tags, list):
            tag_list = [str(value).lower() for value in tags]

        if selected_tag in tag_list:
            filtered_items[image_path] = tags

    row = 0
    col = 0

    for image_path, tags in filtered_items.items():
        try:
            new_img = image_path.strip()
            img = Image.open(new_img).convert("RGBA")
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = Label(grid_frame, image=photo, cursor="hand2")
            label.image = photo
            label.grid(row=row, column=col, padx=10, pady=10)

            def make_clone_function(img_path):
                def clone_to_planner_on_canvas(event):
                    try:
                        img = Image.open(img_path).convert("RGBA")
                        img = img.resize((150, 150), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)

                        plan_mini_canvas_images.append(photo)

                        if img_path.strip() not in used_items:
                            used_items.append(img_path.strip())

                        width = plan_mini_canvas.winfo_width()
                        height = plan_mini_canvas.winfo_height()

                        x = random.randint(0, max(0, width - 150))
                        y = random.randint(0, max(0, height - 150))

                        image_id = plan_mini_canvas.create_image(x, y, image=photo, anchor="nw")

                        def start_drag(e, id=image_id):
                            plan_mini_canvas._drag_data = (id, e.x, e.y)

                        def on_drag(e):
                            item_id, start_x, start_y = plan_mini_canvas._drag_data
                            dx = e.x - start_x
                            dy = e.y - start_y
                            plan_mini_canvas.move(item_id, dx, dy)
                            plan_mini_canvas._drag_data = (item_id, e.x, e.y)

                        def on_double_click(e, id=image_id):
                            plan_mini_canvas.delete(id)
                            if img_path.strip() in used_items:
                                used_items.remove(img_path.strip())

                        plan_mini_canvas.tag_bind(image_id, "<Button-1>", start_drag)
                        plan_mini_canvas.tag_bind(image_id, "<B1-Motion>", on_drag)
                        plan_mini_canvas.tag_bind(image_id, "<Double-Button-1>", on_double_click)
                        plan_mini_canvas.tag_bind(image_id, "<Command-Button-1>",
                                                  lambda e, id=image_id, path=img_path: show_resize_options(id, path,
                                                                                                            plan_mini_canvas,
                                                                                                            plan_mini_canvas_images))

                    except Exception as e:
                        print("Error cloning to canvas:", e)

                return clone_to_planner_on_canvas

            label.bind("<Button-1>", make_clone_function(new_img))

            col += 1
            if col >= columns:
                col = 0
                row += 1

        except Exception as e:
            print(f"Error displaying filtered item {image_path}:", e)

    if not filtered_items:
        print("No results found for:", selected_tag)


def randomize_outfit(canvas, images_list, username, json_path="closet.json"):


    # Clears the current outfit
    canvas.delete("all")
    used_items.clear()
    images_list.clear()


    with open(json_path, 'r') as file:
        data = json.load(file)

    if username not in data:
        messagebox.showerror("Error", f"User {username} not found")
        return

    user_data = data[username]

    # Get all clothing items (exclude 'outfits' key)
    clothes_items = []
    for key, value in user_data.items():
        if key != "outfits" and isinstance(value, dict) and "image_path" in value:
            clothes_items.append(value)

    if not clothes_items:
        messagebox.showwarning("No Clothes", "No clothing items found!")
        return

    # Pick 3 random items
    num_items = min(3, len(clothes_items))
    random_clothes = random.sample(clothes_items, num_items)

    # Put them on canvas
    for item in random_clothes:
        img_path = item["image_path"]
        img = Image.open(img_path).convert("RGBA")
        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        images_list.append(photo)
        used_items.append(img_path.strip())

        #  position
        x = random.randint(50, 300)
        y = random.randint(50, 300)

        image_id = canvas.create_image(x, y, image=photo, anchor="nw")

        # drag and drop
        def start_drag(e, id=image_id):
            canvas._drag_data = (id, e.x, e.y)

        def on_drag(e):
            if hasattr(canvas, '_drag_data'):
                item_id, start_x, start_y = canvas._drag_data
                dx = e.x - start_x
                dy = e.y - start_y
                canvas.move(item_id, dx, dy)
                canvas._drag_data = (item_id, e.x, e.y)

        def on_double_click(e, id=image_id, path=img_path):
            canvas.delete(id)
            if path.strip() in used_items:
                used_items.remove(path.strip())

        canvas.tag_bind(image_id, "<Button-1>", start_drag)
        canvas.tag_bind(image_id, "<B1-Motion>", on_drag)
        canvas.tag_bind(image_id, "<Double-Button-1>", on_double_click)
        canvas.tag_bind(image_id, "<Command-Button-1>",
                lambda e, id=image_id, path=img_path: show_resize_options(id, path, canvas, images_list))





#</editor-fold>
#-----special exclusive edit page---page7
#<editor-fold 1">
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
edit_tags_frame = ttk.Frame(edit_frame, width=500, height=670, style="Custom.TFrame")
edit_tags_frame.pack(side='left', fill='both', expand=True)
edit_tags_frame.pack_propagate(False)


edit_q1_label = ttk.Label(edit_tags_frame, text=" Type ?", style="small.TLabel")
edit_q1_label.pack(pady=10)

edit_attribute_type = StringVar(value="Choose type")
edit_type_menu = OptionMenu(edit_tags_frame, edit_attribute_type, "---","Dress", "Top", "Pants", "Skirt","jacket" ,command=lambda type_value: print("type chosen : "+type_value))

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
edit_color_menu = OptionMenu(edit_tags_frame, edit_attribute_color, "---","Black", "White", "Red", "Blue", "Green", "yellow", command=lambda color_value: print("color chosen ; "+color_value))

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
edit_season_menu = OptionMenu(edit_tags_frame,edit_attribute_season, "---","Summer", "Winter", "Fall", "Spring", command=lambda season_value: print("season chosen ; "+season_value))

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
edit_occasion_menu = OptionMenu(edit_tags_frame, edit_attribute_occasion, "---","Casual", "Work/Office", "Formal", "Party","Lounge/ Home wear", command=lambda occasion_value: print("occasion chosen ; "+occasion_value))

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
edit_material_menu = OptionMenu(edit_tags_frame, edit_attribute_material, "---","Cotton", "denim", "wool","khaki","ribbed","leather", command=lambda material_value: print("material chosen ; "+material_value))

edit_material_menu.pack(pady=10)
edit_material_menu.pack(pady=10)
edit_material_menu.config(
    bg="#5C7285", fg="#333333",
    font=("Pangolin", 15),  # bigger font size here
    width=15,               # wider width here
    padx=10, pady=5         # add some padding inside button
)

def add_edit_custom_tag():
    tag = edit_custom_tag_entry.get().strip()
    if tag and tag not in edit_custom_user_tags:
        edit_custom_user_tags.append(tag)

        tag_frame = Frame(edit_custom_tags_display, bg="#f7f3e6", bd=0)
        tag_frame.pack(side="left", padx=5, pady=2)

        tag_label = Label(tag_frame, text=tag, bg="#d9e2ec", font=("Pangolin", 10), padx=10, pady=5, relief="ridge")
        tag_label.pack(side="left")

        remove_btn = Button(tag_frame, text="✕", font=("Arial", 10), bg="#f7f3e6", fg="red", bd=0, relief="flat",
                            command=lambda: remove_edit_custom_tag(tag, tag_frame))
        remove_btn.pack(side="left", padx=(2, 0))

        edit_custom_tag_entry.delete(0, END)

def remove_edit_custom_tag(tag, tag_frame):
    if tag in edit_custom_user_tags:
        edit_custom_user_tags.remove(tag)
    tag_frame.destroy()



edit_custom_tag_entry = Entry(edit_tags_frame, width=20)
edit_custom_tag_entry.pack(pady=5)

edit_add_tag_button = ttk.Button(edit_tags_frame, text="Add Tag", width=10, bootstyle="secondary", command=add_edit_custom_tag)
edit_add_tag_button.pack(pady=5)

edit_custom_tags_display = Frame(edit_tags_frame, bg="#f7f3e6")
edit_custom_tags_display.pack(pady=5)

def edit_clothing_data():
    global current_editing_path, all_custom_tags
    selected_image_path = current_editing_path

    updated_type = edit_attribute_type.get()
    updated_color = edit_attribute_color.get()
    updated_season = edit_attribute_season.get()
    updated_occasion = edit_attribute_occasion.get()
    updated_material = edit_attribute_material.get()

    filename = "closet.json"

    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        messagebox.showerror("Error", "Could not read clothing data.")
        return

    if username not in data or selected_image_path not in data[username]:
        messagebox.showerror("Error", "Clothing item not found.")
        return

    # Update all fields
    item = data[username][selected_image_path]
    item["type"] = updated_type
    item["color"] = updated_color
    item["season"] = updated_season
    item["occasion"] = updated_occasion
    item["material"] = updated_material
    item["custom_tags"] = edit_custom_user_tags[:]

    # Add custom tags to global session tag set
    for tag in edit_custom_user_tags:
        all_custom_tags.add(tag)


    all_tags = [
        updated_type, updated_color, updated_season,
        updated_occasion, updated_material
    ] + edit_custom_user_tags

    # Skip defaults/empties like "---"
    add_tags_to_pool([
        tag.lower() for tag in all_tags if tag and tag != "---"
    ])

    # Save back to file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo("Saved", "Item updated in your closet.")

def delete_outfit_data():
    global current_editing_path, all_custom_tags
    selected_image_path = current_editing_path

    with open("closet.json", "r") as f:
        data = json.load(f)

    if selected_image_path in data.get(username, {}):
        # Optionally remove tags from global list
        tags_to_remove = set(data[username][selected_image_path].get("custom_tags", []))
        del data[username][selected_image_path]

        # Rebuild global tag list (since other items may use same tags)
        all_custom_tags.clear()
        for item in data.get(username, {}).values():
            for tag in item.get("custom_tags", []):
                all_custom_tags.add(tag)

        with open("closet.json", "w") as f:
            json.dump(data, f, indent=4)

    display_clothes_grid(grid_frame, username)
    next_page(page6)




edit_save_button= ttk.Button(edit_tags_frame,bootstyle=PRIMARY, width=15, text="Save", command= edit_clothing_data)
edit_save_button.pack(pady=5)

edit_delete_button= ttk.Button(edit_tags_frame,bootstyle=PRIMARY, width=15, text="delete item", command=delete_outfit_data )
edit_delete_button.pack(pady=0)


#</editor-fold>

#----------- make outfits page (page8)-----------
#<editor-fold 2">
page8 = ttk.Frame(window, style="Custom.TFrame")
page8.grid(row=0, column=0, sticky="nsew")
page8.grid_propagate(False)

plan_header = ttk.Label(page8, text="Outfit Planner", style="Header.TLabel")
plan_header.pack(pady=10, padx=10)

plan_sub_header = ttk.Label(page8, text="cmd+click for resize options", style="small.TLabel")
plan_sub_header.pack(pady=10, padx=10)

big_frame = ttk.Frame(page8, style="Custom.TFrame")
big_frame.pack(pady=10, padx=0)

# ----- Left Frame -----

# ---- Outfit Planner LEFT PANEL (page8) ----
plan_left_frame = ttk.Frame(big_frame, width=350, height=900)
plan_left_frame.pack(pady=1, padx=3, side="left")

# --- Entry section at the top ---
entry_section = ttk.Frame(plan_left_frame, style="Custom.TFrame")
entry_section.pack(fill="x", pady= 0,side="top")

plan_entry = ttk.Entry(entry_section, width=25)
plan_entry.pack(side="left", padx=(5, 5))
plan_entry.bind("<KeyRelease>", lambda e: show_plan_suggestions())

plan_search_button = ttk.Button(entry_section, text="search", width=6, command=lambda: search_outfit_inventory())
plan_search_button.pack(side="left")

plan_autocomplete_Listbox = Listbox(plan_left_frame, height=3)
plan_autocomplete_Listbox.place_forget()
plan_autocomplete_Listbox.bind("<<ListboxSelect>>", lambda e: select_plan_suggestions())

# --- Scrollable canvas for clothing items ---
plan_canvas = Canvas(plan_left_frame, bg="beige", width=350, height=800)
plan_scrollbar = ttk.Scrollbar(plan_left_frame, orient="vertical", command=plan_canvas.yview)
plan_frame = ttk.Frame(plan_canvas, style="Custom.TFrame")

plan_canvas.configure(yscrollcommand=plan_scrollbar.set)
plan_scrollbar.pack(side="right", fill="y")
plan_canvas.pack(side="left", fill="both", expand=True)
plan_canvas.create_window((0, 0), window=plan_frame, anchor="nw")
plan_frame.bind("<Configure>", lambda e: plan_canvas.configure(scrollregion=plan_canvas.bbox("all")))

# --- Autocomplete suggestions ---
def show_plan_suggestions():
    user_input = plan_entry.get().lower()
    plan_autocomplete_Listbox.delete(0, END)

    if user_input == "":
        plan_autocomplete_Listbox.place_forget()
        return

    matches = [tag for tag in search_tags if user_input in tag.lower()]
    if matches:
        for tag in matches:
            plan_autocomplete_Listbox.insert(END, tag)
        plan_autocomplete_Listbox.place(
            x=plan_entry.winfo_x(),
            y=plan_entry.winfo_y() + plan_entry.winfo_height()
        )
        plan_autocomplete_Listbox.lift()
    else:
        plan_autocomplete_Listbox.place_forget()

def select_plan_suggestions():
    selection = plan_autocomplete_Listbox.curselection()
    if selection:
        selected_tag = plan_autocomplete_Listbox.get(selection[0])
        plan_entry.delete(0, END)
        plan_entry.insert(0, selected_tag)
        plan_autocomplete_Listbox.place_forget()

# --- Search handler for planner ---
def search_outfit_inventory():
    selected_tag = plan_entry.get().strip().lower()
    if selected_tag == "":
        display_clothes_plangrid(plan_frame, username, plan_mini_canvas, plan_mini_canvas_images)
    else:
        display_filtered_clothes_plan_page8(plan_frame, plan_center_frame, username=username, selected_tag=selected_tag)



# ----- Center Frame -----
plan_center_frame = ttk.Frame(big_frame, width=600, height=900, style="Custom.TFrame")
plan_center_frame.pack(pady=1, padx=20, side="left")
plan_center_frame.pack_propagate(False)


plan_mini_canvas = Canvas(plan_center_frame, width=600, height=750, bg="white", highlightthickness=1, highlightbackground="gray")
plan_mini_canvas.pack(pady=1, padx=20)
plan_mini_canvas_images = []


plan_button_frame = ttk.Frame(plan_center_frame, style="Custom.TFrame")
plan_button_frame.pack(side='bottom', pady=1,anchor='s')  # Frame at the bottom


plan_back_button = ttk.Button(plan_button_frame, text="back", width=6, command=lambda: next_page(page4))
plan_back_button.pack(side="left", padx=10)

plan_save_button = ttk.Button(plan_button_frame, text="save", width=6, command=lambda: take_snapshot(plan_mini_canvas, username))
plan_save_button.pack(side="left", padx=10)

plan_clear_button = ttk.Button(plan_button_frame, text="clear", width=6, command=lambda: clear_outfit_frame())
plan_clear_button.pack(side="left", padx=10)

plan_randomize_button=ttk.Button(plan_button_frame, text="randomize", width=8,command=lambda:randomize_outfit(plan_mini_canvas, plan_mini_canvas_images, username))
plan_randomize_button.pack(side="left", padx=10)


# ----- Right Frame -----
plan_right_frame = ttk.Frame(big_frame, width=350, height=900)
plan_right_frame.pack(pady=1, padx=3, side="left")

entry2_section = ttk.Frame(plan_right_frame, style="Custom.TFrame")
entry2_section.pack(fill="x", pady=0, side="top")

plan2_entry = ttk.Entry(entry2_section, width=25)
plan2_entry.pack(side="left", padx=(5, 5))
plan2_entry.bind("<KeyRelease>", lambda e: show_plan2_suggestions())

plan2_search_button = ttk.Button(entry2_section, text="search", width=6, command=lambda: search_outfit_inventory2())
plan2_search_button.pack(side="left")

plan2_autocomplete_Listbox = Listbox(plan_right_frame, height=3)
plan2_autocomplete_Listbox.place_forget()
plan2_autocomplete_Listbox.bind("<<ListboxSelect>>", lambda e: select_plan2_suggestions())


plan2_canvas = Canvas(plan_right_frame, bg="beige", width=350, height=900)
plan2_scrollbar = ttk.Scrollbar(plan_right_frame, orient="vertical", command=plan2_canvas.yview)
plan2_frame = ttk.Frame(plan2_canvas, style="Custom.TFrame")

plan2_canvas.configure(yscrollcommand=plan2_scrollbar.set)
plan2_scrollbar.pack(side="right", fill="y")
plan2_canvas.pack(side="left", fill="both", expand=True)
plan2_canvas.create_window((0, 0), window=plan2_frame, anchor="nw")
plan2_frame.bind("<Configure>", lambda e: plan2_canvas.configure(scrollregion=plan2_canvas.bbox("all")))


def show_plan2_suggestions():
    user_input = plan2_entry.get().lower()
    plan2_autocomplete_Listbox.delete(0, END)

    if user_input == "":
        plan2_autocomplete_Listbox.place_forget()
        return

    matches = [tag for tag in search_tags if user_input in tag.lower()]
    if matches:
        for tag in matches:
            plan2_autocomplete_Listbox.insert(END, tag)
        plan2_autocomplete_Listbox.place(
            x=plan2_entry.winfo_x(),
            y=plan2_entry.winfo_y() + plan2_entry.winfo_height()
        )
        plan2_autocomplete_Listbox.lift()
    else:
        plan2_autocomplete_Listbox.place_forget()

def select_plan2_suggestions():
    selection = plan2_autocomplete_Listbox.curselection()
    if selection:
        selected_tag = plan2_autocomplete_Listbox.get(selection[0])
        plan2_entry.delete(0, END)
        plan2_entry.insert(0, selected_tag)
        plan2_autocomplete_Listbox.place_forget()

def search_outfit_inventory2():
    selected_tag = plan2_entry.get().strip().lower()
    if selected_tag == "":
        display_clothes_plangrid(plan2_frame, username, plan_mini_canvas, plan_mini_canvas_images)
    else:
        display_filtered_clothes_plan_page8(plan2_frame, plan_center_frame, username=username, selected_tag=selected_tag)


# ----- Mousewheel binding -----
def bind_mousewheel_to(canvas):
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

bind_mousewheel_to(plan_canvas)
bind_mousewheel_to(plan2_canvas)
#</editor-fold>

#----------- display all outfits page (page9)----
#<editor-fold>
page9 = ttk.Frame(window, style="Custom.TFrame")
page9.grid(row=0, column=0, sticky="nsew")
page9.grid_propagate(False)

fit_header = ttk.Label(page9, text="Outfit Planner", style="Header.TLabel")
fit_header.pack(pady=10, padx=10)

fit_canvas_frame = ttk.Frame(page9, style="Custom.TFrame",width=800, height=900)
fit_canvas_frame.pack(pady=10, padx=0, )

fit_canvas = Canvas(fit_canvas_frame, bg="beige",width=680, height=760)  # Just using Canvas since it's imported
fit_scrollbar = ttk.Scrollbar(fit_canvas_frame, orient="vertical", command=fit_canvas.yview)
fit_grid_frame = ttk.Frame(fit_canvas, style="Custom.TFrame")


fit_canvas.configure(yscrollcommand=fit_scrollbar.set)
fit_scrollbar.pack(side="right", fill="y")
fit_canvas.pack(side="left" )

fit_canvas.create_window((0, 0), window=fit_grid_frame, anchor="nw")

fit_button_frame = ttk.Frame(page9,style="Custom.TFrame")
fit_button_frame.pack(pady=10, padx=10,side="bottom")

fit_back_button = ttk.Button(fit_button_frame, text="Back", command=lambda: next_page(page4))
fit_back_button.pack(pady=10, padx=10)

def configure_scroll_region(event):
    fit_canvas.configure(scrollregion=fit_canvas.bbox("all"))

fit_grid_frame.bind("<Configure>", configure_scroll_region)

#</editor-fold
#------------page10(outfit edit)------
#<editor-fold>
def add_image_to_fit_canvas(image_path, canvas, image_list, x=100, y=100):
    try:
        img = Image.open(image_path).convert("RGBA")


        new_size = (150, 150)
        transparent_img = Image.new("RGBA", new_size, (0, 0, 0, 0))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        transparent_img.paste(img, (0, 0), img)
        img_tk = ImageTk.PhotoImage(transparent_img)

        canvas.create_image(x, y, image=img_tk, anchor="nw")
        image_list.append(img_tk)

    except Exception as e:
        print(f"[ERROR] Failed to add image: {e}")

page10 = ttk.Frame(window,style="Custom.TFrame")
page10.grid(row=0, column=0, sticky="nsew")
page10.grid_propagate(False)

fit_edit_header = ttk.Label(page10, text="Edit Outfit", style="Header.TLabel")
fit_edit_header.pack(pady=10, padx=10)

fit_plan_header = ttk.Label(page10, text="Outfit Planner", style="Header.TLabel")
plan_header.pack(pady=10, padx=10)

fit_big_frame = ttk.Frame(page10, style="Custom.TFrame")
fit_big_frame.pack(pady=10, padx=0)

# ----- Left Frame -----

# ---- Outfit Planner LEFT PANEL (page10) ----
fit_plan_left_frame = ttk.Frame(fit_big_frame, width=350, height=900)
fit_plan_left_frame.pack(pady=1, padx=3, side="left")

# --- Entry section at the top ---
fit_entry_section = ttk.Frame(fit_plan_left_frame, style="Custom.TFrame")
fit_entry_section.pack(fill="x", pady=0, side="top")

fit_plan_entry = ttk.Entry(fit_entry_section, width=25)
fit_plan_entry.pack(side="left", padx=(5, 5))
fit_plan_entry.bind("<KeyRelease>", lambda e: fit_show_plan_suggestions())

fit_plan_search_button = ttk.Button(fit_entry_section, text="search", width=6, command=lambda: fit_search_outfit_inventory())
fit_plan_search_button.pack(side="left")

fit_plan_autocomplete_Listbox = Listbox(fit_plan_left_frame, height=3)
fit_plan_autocomplete_Listbox.place_forget()
fit_plan_autocomplete_Listbox.bind("<<ListboxSelect>>", lambda e: fit_select_plan_suggestions())

# --- Scrollable canvas for clothing items ---
fit_plan_canvas = Canvas(fit_plan_left_frame, bg="beige", width=350, height=800)
fit_plan_scrollbar = ttk.Scrollbar(fit_plan_left_frame, orient="vertical", command=fit_plan_canvas.yview)
fit_plan_frame = ttk.Frame(fit_plan_canvas, style="Custom.TFrame")

fit_plan_canvas.configure(yscrollcommand=fit_plan_scrollbar.set)
fit_plan_scrollbar.pack(side="right", fill="y")
fit_plan_canvas.pack(side="left", fill="both", expand=True)
fit_plan_canvas.create_window((0, 0), window=fit_plan_frame, anchor="nw")
fit_plan_frame.bind("<Configure>", lambda e: fit_plan_canvas.configure(scrollregion=fit_plan_canvas.bbox("all")))

# --- Autocomplete suggestions ---
def fit_show_plan_suggestions():
    user_input = fit_plan_entry.get().lower()
    fit_plan_autocomplete_Listbox.delete(0, END)

    if user_input == "":
        fit_plan_autocomplete_Listbox.place_forget()
        return

    matches = [tag for tag in search_tags if user_input in tag.lower()]
    if matches:
        for tag in matches:
            fit_plan_autocomplete_Listbox.insert(END, tag)
        fit_plan_autocomplete_Listbox.place(
            x=fit_plan_entry.winfo_x(),
            y=fit_plan_entry.winfo_y() + fit_plan_entry.winfo_height()
        )
        fit_plan_autocomplete_Listbox.lift()
    else:
        fit_plan_autocomplete_Listbox.place_forget()

def fit_select_plan_suggestions():
    selection = fit_plan_autocomplete_Listbox.curselection()
    if selection:
        selected_tag = fit_plan_autocomplete_Listbox.get(selection[0])
        fit_plan_entry.delete(0, END)
        fit_plan_entry.insert(0, selected_tag)
        fit_plan_autocomplete_Listbox.place_forget()

# --- Search handler for planner ---
def fit_search_outfit_inventory():
    selected_tag = fit_plan_entry.get().strip().lower()
    if selected_tag == "":
        display_clothes_plangrid(fit_plan_frame, username=username)
    else:
        display_filtered_clothes_plan(fit_plan_frame, fit_plan_center_frame, username=username, selected_tag=selected_tag)

# ----- Center Frame -----
fit_plan_center_frame = ttk.Frame(fit_big_frame, width=600, height=900, style="Custom.TFrame")
fit_plan_center_frame.pack(pady=1, padx=20, side="left")
fit_plan_center_frame.pack_propagate(False)

fit_plan_mini_canvas = Canvas(fit_plan_center_frame, width=600, height=750, bg="white", highlightthickness=1, highlightbackground="gray")
fit_plan_mini_canvas.pack(pady=1, padx=20)
fit_plan_mini_canvas_images=[]

fit_plan_button_frame = ttk.Frame(fit_plan_center_frame, style="Custom.TFrame")
fit_plan_button_frame.pack(side='bottom', pady=1, anchor='s')  # This frame is at the bottom

# Pack buttons side by side inside the frame
fit_plan_back_button = ttk.Button(fit_plan_button_frame, text="back", width=6, command=lambda: next_page(page4))
fit_plan_back_button.pack(side="left", padx=10)

fit_plan_save_button = ttk.Button(fit_plan_button_frame, text="save", width=6, command=lambda: take_snapshot(fit_plan_mini_canvas, username))
fit_plan_save_button.pack(side="left", padx=10)

fit_plan_clear_button = ttk.Button(fit_plan_button_frame, text="clear", width=6, command=clear_outfit_frame)
fit_plan_clear_button.pack(side="left", padx=10)


def delete_edit_outfit_data(json_path="closet.json"):
    global currently_loaded_snapshot, username

    if not currently_loaded_snapshot:
        messagebox.showwarning("Warning", "No outfit selected to delete.")
        return

    if not messagebox.askyesno("Delete Outfit", "Are you sure you want to delete this entire outfit?"):
        return

    try:
        # Load and update JSON
        with open(json_path, 'r') as file:
            data = json.load(file)

        del data[username]["outfits"][currently_loaded_snapshot]

        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Delete image file
        if os.path.exists(currently_loaded_snapshot):
            os.remove(currently_loaded_snapshot)

        currently_loaded_snapshot = None
        messagebox.showinfo("Success", "Outfit deleted successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete outfit: {e}")

    next_page(page4)


fit_plan_delete_button = ttk.Button(fit_plan_button_frame, text="delete outfit", width=10, command=delete_edit_outfit_data)
fit_plan_delete_button.pack(side="left", padx=10)
# ----- Right Frame -----
fit_plan_right_frame = ttk.Frame(fit_big_frame, width=350, height=900)
fit_plan_right_frame.pack(pady=1, padx=3, side="left")

fit_entry2_section = ttk.Frame(fit_plan_right_frame, style="Custom.TFrame")
fit_entry2_section.pack(fill="x", pady=0, side="top")

fit_plan2_entry = ttk.Entry(fit_entry2_section, width=25)
fit_plan2_entry.pack(side="left", padx=(5, 5))
fit_plan2_entry.bind("<KeyRelease>", lambda e: fit_show_plan2_suggestions())

fit_plan2_search_button = ttk.Button(fit_entry2_section, text="search", width=6, command=lambda: fit_search_outfit_inventory2())
fit_plan2_search_button.pack(side="left")

fit_plan2_autocomplete_Listbox = Listbox(fit_plan_right_frame, height=3)
fit_plan2_autocomplete_Listbox.place_forget()
fit_plan2_autocomplete_Listbox.bind("<<ListboxSelect>>", lambda e: fit_select_plan2_suggestions())

fit_plan2_canvas = Canvas(fit_plan_right_frame, bg="beige", width=350, height=900)
fit_plan2_scrollbar = ttk.Scrollbar(fit_plan_right_frame, orient="vertical", command=fit_plan2_canvas.yview)
fit_plan2_frame = ttk.Frame(fit_plan2_canvas, style="Custom.TFrame")

fit_plan2_canvas.configure(yscrollcommand=fit_plan2_scrollbar.set)
fit_plan2_scrollbar.pack(side="right", fill="y")
fit_plan2_canvas.pack(side="left", fill="both", expand=True)
fit_plan2_canvas.create_window((0, 0), window=fit_plan2_frame, anchor="nw")
fit_plan2_frame.bind("<Configure>", lambda e: fit_plan2_canvas.configure(scrollregion=fit_plan2_canvas.bbox("all")))

def fit_show_plan2_suggestions():
    user_input = fit_plan2_entry.get().lower()
    fit_plan2_autocomplete_Listbox.delete(0, END)

    if user_input == "":
        fit_plan2_autocomplete_Listbox.place_forget()
        return

    matches = [tag for tag in search_tags if user_input in tag.lower()]
    if matches:
        for tag in matches:
            fit_plan2_autocomplete_Listbox.insert(END, tag)
        fit_plan2_autocomplete_Listbox.place(
            x=fit_plan2_entry.winfo_x(),
            y=fit_plan2_entry.winfo_y() + fit_plan2_entry.winfo_height()
        )
        fit_plan2_autocomplete_Listbox.lift()
    else:
        fit_plan2_autocomplete_Listbox.place_forget()

def fit_select_plan2_suggestions():
    selection = fit_plan2_autocomplete_Listbox.curselection()
    if selection:
        selected_tag = fit_plan2_autocomplete_Listbox.get(selection[0])
        fit_plan2_entry.delete(0, END)
        fit_plan2_entry.insert(0, selected_tag)
        fit_plan2_autocomplete_Listbox.place_forget()

def fit_search_outfit_inventory2():
    selected_tag = fit_plan2_entry.get().strip().lower()
    if selected_tag == "":
        display_clothes_plangrid(fit_plan2_frame, username=username)
    else:
        display_filtered_clothes_plan(fit_plan2_frame, fit_plan_center_frame, username=username, selected_tag=selected_tag)

# ----- Mousewheel binding -----
def fit_bind_mousewheel_to(canvas):
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

fit_bind_mousewheel_to(fit_plan_canvas)
fit_bind_mousewheel_to(fit_plan2_canvas)


#</editor-fold>

# Function to raise the frame
def next_page(frame):
    if frame == page4:
        home_head_label.config(text="hello " + username + " this is your HomePage")
    frame.tkraise()

# Configure all frames
for frame in (page1, page2, page3, page4, page5, page6, page7, page8, page9):
    frame.grid(row=0, column=0, sticky="nsew")

next_page(page1)  # Start by showing the welcome page

# Run the main loop
window.mainloop()




