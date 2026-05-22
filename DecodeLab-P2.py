import customtkinter as ctk
from tkinter import messagebox


ctk.set_appearance_mode("dark")          
ctk.set_default_color_theme("dark-blue") 

class PremiumCryptoEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("DecodeLabs | Advanced Cryptographic Engine")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self._build_header()
        self._build_input_section()
        self._build_controls()
        self._build_output_section()

    def _build_header(self):
        title = ctk.CTkLabel(self.main_frame, text="SECURE TERMINAL", 
                             font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        title.pack(pady=(20, 5))
        
        subtitle = ctk.CTkLabel(self.main_frame, text="Symmetric Encryption System (Caesar Protocol)", 
                                font=ctk.CTkFont(family="Roboto", size=12), text_color="gray")
        subtitle.pack(pady=(0, 20))

    def _build_input_section(self):
        input_label = ctk.CTkLabel(self.main_frame, text="RAW DATA INPUT", 
                                   font=ctk.CTkFont(size=11, weight="bold"))
        input_label.pack(anchor="w", padx=30)

        self.input_text = ctk.CTkTextbox(self.main_frame, height=100, corner_radius=10, 
                                         border_width=1)
        self.input_text.pack(padx=30, pady=(5, 20), fill="x")

    def _build_controls(self):

        control_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        control_frame.pack(padx=30, fill="x", pady=5)
        
        shift_label = ctk.CTkLabel(control_frame, text="CRYPTOGRAPHIC SHIFT KEY (0-25):", 
                                   font=ctk.CTkFont(size=11, weight="bold"))
        shift_label.pack(anchor="w")

        self.shift_slider = ctk.CTkSlider(control_frame, from_=0, to=25, number_of_steps=25, 
                                          command=self._update_shift_label)
        self.shift_slider.set(5)
        self.shift_slider.pack(pady=(5, 15), fill="x")
        
        self.shift_display = ctk.CTkLabel(control_frame, text="Key: 5", font=ctk.CTkFont(weight="bold"))
        self.shift_display.pack(pady=(0, 15))

        btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_frame.pack(fill="x")

        encrypt_btn = ctk.CTkButton(btn_frame, text="ENCRYPT DATA", height=40, corner_radius=8,
                                    command=lambda: self.process_data("encrypt"))
        encrypt_btn.pack(side="left", expand=True, padx=(0, 5))

        decrypt_btn = ctk.CTkButton(btn_frame, text="DECRYPT DATA", height=40, corner_radius=8, 
                                    fg_color="#4A4A4A", hover_color="#333333",
                                    command=lambda: self.process_data("decrypt"))
        decrypt_btn.pack(side="right", expand=True, padx=(5, 0))

    def _build_output_section(self):
        output_label = ctk.CTkLabel(self.main_frame, text="SYSTEM OUTPUT", 
                                    font=ctk.CTkFont(size=11, weight="bold"))
        output_label.pack(anchor="w", padx=30, pady=(20, 0))

        self.output_text = ctk.CTkTextbox(self.main_frame, height=100, corner_radius=10, 
                                          border_width=1, state="disabled", fg_color="#1A1A1A")
        self.output_text.pack(padx=30, pady=(5, 15), fill="x")

        self.status_bar = ctk.CTkLabel(self.root, text="STATUS: System Ready.", 
                                       font=ctk.CTkFont(size=12, weight="bold"))
        self.status_bar.pack(side="bottom", pady=10)

    def _update_shift_label(self, value):
        self.shift_display.configure(text=f"Key: {int(value)}")

    def process_data(self, mode):
        raw_text = self.input_text.get("1.0", "end-1c").strip()
        if not raw_text:
            self.status_bar.configure(text="STATUS: Error - No input data provided.", text_color="red")
            return

        shift = int(self.shift_slider.get())
        
        if mode == "decrypt":
            shift = 26 - (shift % 26)
        else:
            shift = shift % 26
            
        result = ""
        for char in raw_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char

        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", result)
        self.output_text.configure(state="disabled")
        
        self.status_bar.configure(text=f"STATUS: {mode.upper()}ION SUCCESSFUL. Data Secured.", 
                                  text_color="#00FF00" if mode == "encrypt" else "#00BFFF")

if __name__ == "__main__":
    app = ctk.CTk()
    engine = PremiumCryptoEngine(app)
    app.mainloop()
