import customtkinter as ctk
from ui.app import TrafficSimulatorApp

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = TrafficSimulatorApp()
    app.mainloop()