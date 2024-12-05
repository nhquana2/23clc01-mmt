import customtkinter as ctk
import re
from tkinter import filedialog
from .handle_GUI import *

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("GUI/theme.json")  
ctk.set_widget_scaling(0.9)

def open_main_app(window, root):
    window.destroy()
    window = MainPage(master = root)

class LoginApp(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.grid(row = 0, column = 0, sticky = "nsew")
        # Window properties
        master.title("Login Interface")
        master.geometry("400x300")
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=1)

        # Title label
        self.title_label = ctk.CTkLabel(self, text="Login", font=("Inter", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=40)

        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter your username", font=("Inter", 13))
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter your password", show="*",font=("Inter", 13))
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.message_label = ctk.CTkLabel(self, text="")
        self.message_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "1" and password == "1":
            self.message_label.configure(text="Login successful!", text_color="green")
            self.after(500, self.open)  
        else:
            self.message_label.configure(text="Invalid credentials", text_color="red")

    def open(self):
        open_main_app(self, self.master)




def open_file_explorer(path_label):
    file_path = filedialog.askopenfilename(title="Select a File to Upload")
    if file_path:
        path_label.configure(text=file_path)

def open_dir_explorer(path_label):
    dir_path = filedialog.askdirectory(title="Select a Directory to Upload")
    if dir_path:
        path_label.configure(text=dir_path)

class Upper_Upload_Tab(ctk.CTkFrame):
    def __init__(self, master, label, progress):
        super().__init__(master)
        self.grid(row = 0, column = 0 ,sticky="nsew")
        self.grid_columnconfigure((1,2,3,4), weight=1)
        self.grid_rowconfigure((0,1), weight=0)
        self.grid_rowconfigure(2, weight=1)

        #self.label = ctk.CTkLabel(self, text="This is the upper frame", text_color="white")
        #self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.IP_label = ctk.CTkLabel(self, text="Enter your server's IP:", font=("Inter", 18), anchor= "s")
        self.IP_label.grid(row = 2, column=1, padx=10, pady=10, sticky="se")

        self.port_label = ctk.CTkLabel(self, text="Enter your server's Port:", font=("Inter", 18))
        self.port_label.grid(row = 3, column=1, padx=10, pady=10, sticky = "se")
        self.get_ip = ctk.CTkEntry(self)
        self.get_ip.grid(row = 2,column=2, padx=10, pady=10, sticky="sw")
        self.get_port = ctk.CTkEntry(self)
        self.get_port.grid(row = 3,column=2, padx=10, pady=10, sticky="sw")

        #
        upload_label = ctk.CTkLabel(self, text="Choose a file or directory to upload:",font=("Inter", 18))
        upload_label.grid(row=4, column=1, padx=20, pady=(20,10), sticky="se")

        #self.path_label = ctk.CTkLabel(self, text="No file selected", anchor="w", width=400,font=("Inter", 18), wraplength= 400)
        #self.path_label.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.path_label = label
        self.upload_progress = progress
        folder_button = ctk.CTkButton(self, text="Select Folder", command=lambda: open_dir_explorer(self.path_label), anchor= "center",font=("Inter", 18))
        folder_button.grid(row=5, column=2, padx=10, pady=5, sticky = "sw")
        file_button = ctk.CTkButton(self, text="Select File", command=lambda: open_file_explorer(self.path_label), anchor= "center",font=("Inter", 18))
        file_button.grid(row=4, column=2, padx=10, pady=5, sticky = "sw")
        upload_button = ctk.CTkButton(  
            self, text="Upload", font=("Inter", 18),
            command=lambda: handle_upload(self.get_ip.get(), self.get_port.get(),self.path_label, self.upload_progress)
        )
        upload_button.grid(row=5, column=1, padx=10, pady=5, sticky = "se")


class Lower_Upload_Tab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row = 1, column = 0 ,sticky="nsew")
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        self.path_label = ctk.CTkLabel(self, text="No file selected",font=("Inter", 18))
        self.path_label.grid(row=0, column=1, padx=20, pady=10)

        self.upload_progress = ctk.CTkLabel(self, text="",font=("Inter", 18))
        self.upload_progress.grid(row=1, column=1, padx=20, pady=10)
        
    def get_label(self):
        return self.path_label
    def get_progress(self):
        return self.upload_progress


class Upload_Tab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # Make row 0 resizable (for upper frame)
        self.grid_rowconfigure(1, weight=1)  # Make row 1 resizable (for lower frame)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 resizable (for the whole parent)
        lower = Lower_Upload_Tab(self)

        Upper_Upload_Tab(self, lower.get_label(), lower.get_progress())
        
class Upper_Download_Tab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row = 0, column = 0 ,sticky="nsew")
        self.grid_columnconfigure((1,2,3,4), weight=1)
        self.grid_rowconfigure((0,1), weight=0)
        self.grid_rowconfigure(2, weight=1)

        #self.label = ctk.CTkLabel(self, text="This is the upper frame", text_color="white")
        #self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.IP_label = ctk.CTkLabel(self, text="Enter your server's IP:", font=("Inter", 18), anchor= "s")
        self.IP_label.grid(row = 2, column=1, padx=10, pady=10, sticky="se")

        self.port_label = ctk.CTkLabel(self, text="Enter your server's Port:", font=("Inter", 18))
        self.port_label.grid(row = 3, column=1, padx=10, pady=10, sticky = "se")
        self.ip = ctk.CTkEntry(self)
        self.ip.grid(row = 2,column=2, padx=10, pady=10, sticky="sw")
        self.port = ctk.CTkEntry(self)
        self.port.grid(row = 3,column=2, padx=10, pady=10, sticky="sw")

       
    def get_ip(self):
        print(f"{self.ip.get()}")
        return self.ip.get()
    def get_port(self):
        return self.port.get()
        
       # download_label = ctk.CTkLabel(self, text="Enter file name to download:")
        #download_label.grid(row=4, column=1, padx=20, pady=10, sticky = "se")

        

class Lower_Download_Tab(ctk.CTkFrame):
    def __init__(self, master, upper_frame):
        super().__init__(master)
        self.grid(row = 1, column = 0 ,sticky="nsew")
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        

        download_label = ctk.CTkLabel(self, text="Enter file name to download:")
        download_label.grid(row=1, column=1, padx=20, pady=10)

        self.download_entry = ctk.CTkEntry(self, width=400)
        self.download_entry.grid(row=2, column=1, padx=20, pady=10)

        self.download_progress = ctk.CTkLabel(self, text="")
        self.download_progress.grid(row=4, column=1, padx=20, pady=10)

        download_button = ctk.CTkButton(
            self, text="Download", 
            command=lambda: handle_download(self.download_entry, self.download_progress, upper_frame)
        )
        download_button.grid(row=3, column=1, padx=20, pady=10)
        

class Download_Tab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # Make row 0 resizable (for upper frame)
        self.grid_rowconfigure(1, weight=1)  # Make row 1 resizable (for lower frame)
        self.grid_columnconfigure(0, weight=1)  # Make column 0 resizable (for the whole parent)
        upper = Upper_Download_Tab(self)
        Lower_Download_Tab(self, upper)        
    

class MainPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        master.title("File Transfer Client")
        master.geometry("900x430")
        master.minsize(900,430)
        self.grid(row = 0, column = 0, sticky = "nsew")
        #3 3 
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width = 180, corner_radius=0, border_color="black", border_width= 2)
        self.sidebar_frame.grid(row=0, column=0, rowspan = 4, sticky = "nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark","Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=[ "90%", "100%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #Tab view
        self.tab = ctk.CTkTabview(self)
        self.tab.grid(row = 0, column = 1, sticky = "nsew")
        # Add tabs
        upload_tab = self.tab.add("Upload Files")
        upload_tab.grid_columnconfigure(1, weight = 1)
        upload_tab.grid_rowconfigure(0, weight = 1)

        Upload_Tab(upload_tab)
        download_tab = self.tab.add("Download Files")
        download_tab.grid_columnconfigure(1, weight = 1)
        download_tab.grid_rowconfigure(0, weight = 1)
        Download_Tab(download_tab)



    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


