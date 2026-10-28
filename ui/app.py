import threading
import customtkinter as ctk
from core.engine import SimulatorEngine


class TrafficSimulatorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Web Traffic Simulator")
        self.geometry("600x700")
        self.grid_columnconfigure(0, weight=1)

        self.is_running = False
        self.engine = SimulatorEngine(
            log_callback=self.log,
            on_finish_callback=self.on_simulator_finished
        )

        self._setup_ui()

    def _setup_ui(self):
        self.url_label = ctk.CTkLabel(self, text="Target URL:")
        self.url_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.url_entry = ctk.CTkEntry(self, width=560, placeholder_text="e.g., https://example.com")
        self.url_entry.grid(row=1, column=0, padx=20, pady=0)

        self.proxy_label = ctk.CTkLabel(
            self, text="Proxy List (1 per row - ip:port:user:pass or ip:port):"
        )
        self.proxy_label.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")
        self.proxy_textbox = ctk.CTkTextbox(self, width=560, height=150)
        self.proxy_textbox.grid(row=3, column=0, padx=20, pady=0)

        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        self.settings_frame.grid_columnconfigure((0, 1), weight=1)

        self.duration_label = ctk.CTkLabel(self.settings_frame, text="Time Spent on Page (Seconds):")
        self.duration_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.duration_entry = ctk.CTkEntry(self.settings_frame, width=100)
        self.duration_entry.insert(0, "15")
        self.duration_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.threads_label = ctk.CTkLabel(self.settings_frame, text="Maximum Concurrent Tabs:")
        self.threads_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.threads_entry = ctk.CTkEntry(self.settings_frame, width=100)
        self.threads_entry.insert(0, "10")
        self.threads_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.loop_label = ctk.CTkLabel(self.settings_frame, text="How Many Cycles Should the Proxy List Run Through?:")
        self.loop_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.loop_entry = ctk.CTkEntry(self.settings_frame, width=100)
        self.loop_entry.insert(0, "1")
        self.loop_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        self.headless_var = ctk.BooleanVar(value=False)
        self.headless_checkbox = ctk.CTkCheckBox(
            self.settings_frame, text="Headless Mode", variable=self.headless_var
        )
        self.headless_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.start_button = ctk.CTkButton(self, text="Start the Simulator", command=self.start_simulator)
        self.start_button.grid(row=5, column=0, padx=20, pady=10)

        self.log_label = ctk.CTkLabel(self, text="Status Report:")
        self.log_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")
        self.log_textbox = ctk.CTkTextbox(self, width=560, height=100, state="disabled")
        self.log_textbox.grid(row=7, column=0, padx=20, pady=(0, 20))

    def log(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def start_simulator(self):
        if self.is_running:
            return

        url = self.url_entry.get().strip()
        proxies = self.proxy_textbox.get("1.0", "end").strip().split('\n')
        proxies = [p.strip() for p in proxies if p.strip()]

        try:
            duration = int(self.duration_entry.get())
            max_tabs = int(self.threads_entry.get())
            loop_count = int(self.loop_entry.get())
        except ValueError:
            self.log("[ERROR] Duration, tab, and number of rounds must be numerical.")
            return

        if not url or not proxies:
            self.log("[ERROR] Please enter a URL and at least one proxy.")
            return

        self.is_running = True
        self.start_button.configure(state="disabled", text="Running...")
        self.log("System is starting...")

        threading.Thread(
            target=self.engine.run_async_loop,
            args=(url, proxies, duration, max_tabs, loop_count, self.headless_var.get()),
            daemon=True
        ).start()

    def on_simulator_finished(self):
        self.is_running = False
        self.start_button.configure(state="normal", text="Start Simulator")
        self.log("[INFO] All tasks have been completed.")