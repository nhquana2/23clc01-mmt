from GUI.GUI import *


if __name__ == "__main__":
    root = ctk.CTk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0,weight=1)
    login = LoginApp(master = root)
    root.mainloop()