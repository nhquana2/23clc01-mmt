import customtkinter as ctk
import re
from tkinter import filedialog


ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("GUI/theme.json")  
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window properties
        self.title("Login Interface")
        self.geometry("400x300")
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
            self.after(500, self.open_main_app)  
        else:
            self.message_label.configure(text="Invalid credentials", text_color="red")

    def open_main_app(self):
        self.destroy()  
        MainPage().mainloop()  




def open_file_explorer(path_label):
    file_path = filedialog.askopenfilename(title="Select a File to Upload")
    if file_path:
        path_label.configure(text=file_path)

def open_directory_explorer(path_label):
    directory_path = filedialog.askdirectory(title="Select a Directory to Upload")
    if directory_path:
        path_label.configure(text=directory_path)


class Upload_Tab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        #self.configure(fg_color = "blue")
        self.grid(row=0, column=0, rowspan = 4, columnspan = 4 ,sticky="nsew")  # Fill the parent tab frame

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure((1,3,4), weight=1)
        self.grid_rowconfigure((0,3), weight=0)
        self.grid_rowconfigure((1,2), weight=0)
        self.grid_rowconfigure(9, weight=1)

        # Widgets
        upload_label = ctk.CTkLabel(self, text="Choose a file or directory to upload:", anchor = "w",font=("Inter", 18))
        upload_label.grid(row=2, column=0, padx=20, pady=(20,10), sticky="ew")

        self.path_label = ctk.CTkLabel(self, text="No file selected", anchor="w", width=400,font=("Inter", 18))
        self.path_label.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        file_button = ctk.CTkButton(self, text="Select File", command=lambda: open_file_explorer(self.path_label), anchor= "center",font=("Inter", 18))
        file_button.grid(row=4, column=0, padx=10, pady=5, sticky = "")

        dir_button = ctk.CTkButton(self, text="Select Directory", command=lambda: open_directory_explorer(self.path_label),font=("Inter", 18))
        dir_button.grid(row=4, column=1, padx=10, pady=5, sticky = "")


        self.IP_label = ctk.CTkLabel(self, text="Enter your server's IP:", font=("Inter", 18))
        self.IP_label.grid(row = 0, column=0, columnspan=1, padx=10, pady=10, sticky="e")

        self.port_label = ctk.CTkLabel(self, text="Enter your server's Port:", font=("Inter", 18))
        self.port_label.grid(row = 1, column=0, columnspan=1, padx=10, pady=10, sticky="e")
        self.get_ip = ctk.CTkEntry(self)
        self.get_ip.grid(row = 0,column=1, columnspan=1, padx=10, pady=10, sticky="w")
        self.get_port = ctk.CTkEntry(self)
        self.get_port.grid(row = 1,column=1, columnspan=1, padx=10, pady=10, sticky="w")

        self.upload_progress = ctk.CTkLabel(self, text="",font=("Inter", 18))
        self.upload_progress.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

        upload_button = ctk.CTkButton(  
            self, text="Upload", font=("Inter", 18),
            command=lambda: self.handle_upload_ui(self.path_label, self.upload_progress)
        )
        upload_button.grid(row=6, column=0, columnspan=2, padx=20, pady=10)
    def validate_ip(self, ip):
        ip_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return re.match(ip_pattern, ip) is not None

    def validate_port(self, port):
        try:
            port = int(port)
            return 1 <= port <= 65535
        except ValueError:
            return False
        
    def handle_upload_ui(self, path_label, progress_label):
        path = path_label.cget("text")
        if not path or path == "No file selected":
            progress_label.configure(text="Please select a valid file or directory.")
            return
        progress_label.configure(text="Uploading...")
        # Thread(target=handle_upload_command, args=(path,)).start()
        #upload_file(path)
        server_ip = self.get_ip.get().strip()
        server_port = self.get_port.get().strip()

        if not server_ip or not self.validate_ip(server_ip):
            progress_label.configure(text="Invalid IP address. Please enter a valid IP.")
            return

        if not server_port or not self.validate_port(server_port):
            progress_label.configure(text="Invalid port. Please enter a valid port (1-65535).")
            return
        
        try:
        
            progress_label.configure(text=f"Uploading file to {server_ip}:{server_port}...")
            #upload_file
            progress_label.configure(text="Upload completed successfully.")
        except Exception as e:
            progress_label.configure(text=f"Error: {str(e)}")

class Download_Tab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=1, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)

        # Widgets
        download_label = ctk.CTkLabel(self, text="Enter file name to download:", anchor="w")
        download_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.download_entry = ctk.CTkEntry(self, width=400)
        self.download_entry.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.download_progress = ctk.CTkLabel(self, text="")
        self.download_progress.grid(row=2, column=0, padx=20, pady=10)

        download_button = ctk.CTkButton(
            self, text="Download", 
            command=lambda: print(f"Downloading {self.download_entry.get()}")
        )
        download_button.grid(row=3, column=0, padx=20, pady=10)

class MainPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Transfer Client")
        self.geometry("900x430")
        self.minsize(900,430)
        #3 3 
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width = 180, corner_radius=0, border_color="black", border_width= 2)
        self.sidebar_frame.grid(row=0, column=0, rowspan = 4, sticky = "nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark","Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #Tab view
        self.tab = ctk.CTkTabview(self)
        self.tab.grid(row = 0, column = 1, rowspan = 4, columnspan = 4, sticky = "nsew")
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


