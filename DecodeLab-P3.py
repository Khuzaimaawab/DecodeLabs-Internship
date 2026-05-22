import customtkinter as ctk
import re
from urllib.parse import urlparse

# --- SYSTEM THEME SETTINGS ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class PhishingTriageToolkit(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DecodeLabs | Phishing Triage Toolkit (Proj 3)")
        
        # Base resolution (Responsive Dual-Pane)
        self.geometry("1100x550")
        self.resizable(True, True)
        
        # Auto-Maximize Window (Cross-Platform)
        try:
            self.state('zoomed')  # Works on Windows/Linux
        except:
            self.attributes('-zoomed', True)  # Fallback for macOS

        # Configure responsive grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- THREAT INTELLIGENCE DATABASES ---
        self.authority_keywords = ['ceo', 'executive', 'director', 'manager', 'it support', 'admin', 'helpdesk']
        self.urgency_keywords = ['urgent', 'immediate', 'act now', 'asap', 'expire', 'verify', 'alert', 'immediately']
        self.fear_keywords = ['compromised', 'breach', 'suspend', 'block', 'terminate', 'account locked', 'unauthorized']
        self.dangerous_attachments = ['.exe', '.bat', '.scr', '.vbs', '.js', '.iso', '.zip']
        
        # New: Trusted Roots for Subdomain Validation
        self.trusted_roots = ['microsoft.com', 'paypal.com', 'amazon.com', 'apple.com', 'decodelabs.tech']
        
        self._build_header()
        
        # Create Left and Right Panes
        self.left_pane = ctk.CTkFrame(self, fg_color="transparent")
        self.left_pane.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))
        
        self.right_pane = ctk.CTkFrame(self, fg_color="transparent")
        self.right_pane.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))

        self._build_input_section()
        self._build_output_section()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=15)
        
        ctk.CTkLabel(header_frame, text="PHISHING TRIAGE TOOLKIT", font=ctk.CTkFont("Roboto", 24, "bold")).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Project 3: Human Firewall & Social Engineering Detection", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w")

    # --- LEFT PANE: INPUTS ---
    def _build_input_section(self):
        # 1. Header Analysis
        header_frame = ctk.CTkFrame(self.left_pane, corner_radius=8)
        header_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(header_frame, text="1. HEADER ANALYSIS", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        input_grid = ctk.CTkFrame(header_frame, fg_color="transparent")
        input_grid.pack(fill="x", padx=15, pady=(0, 15))
        input_grid.grid_columnconfigure(1, weight=1) 

        ctk.CTkLabel(input_grid, text="Display Name:", font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        self.sender_name = ctk.CTkEntry(input_grid, placeholder_text="e.g., PayPal Support")
        self.sender_name.grid(row=0, column=1, sticky="ew", pady=5)

        ctk.CTkLabel(input_grid, text="Return-Path Email:", font=ctk.CTkFont(size=11)).grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        self.sender_email = ctk.CTkEntry(input_grid, placeholder_text="e.g., alert@update-paypal.com")
        self.sender_email.grid(row=1, column=1, sticky="ew", pady=5)

        # 2. Raw Payload
        payload_frame = ctk.CTkFrame(self.left_pane, corner_radius=8)
        payload_frame.pack(fill="both", expand=True, pady=10)

        ctk.CTkLabel(payload_frame, text="2. RAW PAYLOAD (Message Body)", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        self.payload_text = ctk.CTkTextbox(payload_frame, corner_radius=5)
        self.payload_text.pack(padx=15, pady=(0, 15), fill="both", expand=True)

        # Execute Button
        ctk.CTkButton(self.left_pane, text="EXECUTE TRIAGE ANALYSIS", height=45, font=ctk.CTkFont(weight="bold", size=14), command=self.analyze_threat).pack(fill="x", pady=(10, 0))

    # --- RIGHT PANE: OUTPUTS ---
    def _build_output_section(self):
        output_frame = ctk.CTkFrame(self.right_pane, corner_radius=8)
        output_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(output_frame, text="3. TRIAGE DECISION TREE", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))

        # Status Board
        status_board = ctk.CTkFrame(output_frame, fg_color="#FFFFFF", corner_radius=8)
        status_board.pack(fill="x", padx=15, pady=10)

        self.status_label = ctk.CTkLabel(status_board, text="STATUS: AWAITING PAYLOAD", font=ctk.CTkFont(size=18, weight="bold"))
        self.status_label.pack(pady=(15, 5))
        
        self.action_label = ctk.CTkLabel(status_board, text="REQUIRED ACTION: NONE", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray")
        self.action_label.pack(pady=(0, 15))

        # Red Flag Log
        ctk.CTkLabel(output_frame, text="Identified Red Flags & Context:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        self.log_text = ctk.CTkTextbox(output_frame, state="disabled", fg_color="#FFFFFF", text_color="#FF4500", font=ctk.CTkFont("Courier", 12))
        self.log_text.pack(padx=15, pady=(0, 15), fill="both", expand=True)

    # --- THREAT ANALYSIS ENGINE ---
    def analyze_threat(self):
        name = self.sender_name.get().lower()
        email = self.sender_email.get().lower()
        payload = self.payload_text.get("1.0", "end-1c").lower()
        
        if not payload and not email:
            return

        red_flags = []
        threat_score = 0

        # 1. Header Mismatch Check
        if name and email:
            domain = email.split('@')[-1] if '@' in email else ""
            if any(brand in name for brand in ['paypal', 'amazon', 'microsoft', 'apple', 'bank']) and not any(brand in domain for brand in ['paypal', 'amazon', 'microsoft', 'apple', 'bank']):
                red_flags.append("[!] SENDER MISMATCH: Display name claims authority, but email domain is untrusted.")
                threat_score += 2

        # 2. Cognitive Triggers
        if any(word in payload for word in self.urgency_keywords):
            red_flags.append("[-] COGNITIVE TRIGGER (Urgency): Artificial time constraint detected.")
            threat_score += 1
            
        if any(word in payload for word in self.fear_keywords):
            red_flags.append("[-] COGNITIVE TRIGGER (Fear): Threatening language used to force compliance.")
            threat_score += 1

        if any(word in payload for word in self.authority_keywords):
            red_flags.append("[-] COGNITIVE TRIGGER (Authority): Impersonation of management/IT detected.")
            threat_score += 1

        # 3. Dangerous Attachments
        if any(ext in payload for ext in self.dangerous_attachments):
            red_flags.append("[!] MALWARE RISK: Suspicious file extension referenced in payload.")
            threat_score += 2

        # 4. PATCHED: The Subdomain Trap Check (with Trusted Root & Punctuation Filter)
        urls = re.findall(r'(https?://[^\s]+)', payload)
        for url in urls:
            try:
                # BUG FIX: Strip trailing sentence punctuation the regex might have grabbed
                clean_url = url.rstrip(".,;!?\"')")
                
                parsed_uri = urlparse(clean_url)
                domain = parsed_uri.netloc
                
                # Secondary safety: ensure no trailing dots exist on the domain itself
                domain = domain.rstrip('.') 
                parts = domain.split('.')
                
                if len(parts) > 2: 
                    # Extract the true root (the last two parts)
                    true_root = '.'.join(parts[-2:])
                    
                    # If the true root is NOT in our trusted whitelist, flag it.
                    if true_root not in self.trusted_roots:
                        red_flags.append(f"[!] SUBDOMAIN TRAP: Deep URL structure ({domain}). True root '{true_root}' is untrusted.")
                        threat_score += 2
            except:
                pass

        # --- TRIAGE DECISION TREE LOGIC ---
        if threat_score == 0:
            status = "STATUS: SAFE"
            status_color = "#00FF00" # Green
            action = "ACTION: CLOSE"
            action_color = "#00FF00"
            log_output = "No recognizable cognitive triggers or technical red flags detected."
        elif threat_score <= 2:
            status = "STATUS: SUSPICIOUS"
            status_color = "#FFA500" # Orange
            action = "ACTION: WARN USER"
            action_color = "#FFA500"
            log_output = "\n".join(red_flags)
        else:
            status = "STATUS: MALICIOUS"
            status_color = "#FF0000" # Red
            action = "ACTION: BLOCK DOMAIN & ESCALATE"
            action_color = "#FF0000"
            log_output = "\n".join(red_flags)

        # Update UI Safely
        self.status_label.configure(text=status, text_color=status_color)
        self.action_label.configure(text=action, text_color=action_color)
        
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("end", log_output)
        self.log_text.configure(state="disabled")

if __name__ == "__main__":
    app = PhishingTriageToolkit()
    app.mainloop()