#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import requests
import argparse
import json
from datetime import datetime
import threading
import sys

class RelayControllerGUI:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.version = "Unknown"
        self.connected = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Network Relay Controller")
        self.root.resizable(False, False)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header with version and connection info
        self.header_var = tk.StringVar(value="Network Relay Controller")
        self.connection_var = tk.StringVar(value=f"Connected to: {host}:{port}")
        
        ttk.Label(self.main_frame, textvariable=self.header_var).grid(row=0, column=0, columnspan=3)
        ttk.Label(self.main_frame, textvariable=self.connection_var).grid(row=1, column=0, columnspan=3)
        ttk.Separator(self.main_frame, orient='horizontal').grid(row=2, column=0, columnspan=3, sticky='ew', pady=5)
        
        # Global control buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=5)
        
        self.all_on_btn = ttk.Button(button_frame, text="All ON", command=self.turn_all_on)
        self.all_on_btn.grid(row=0, column=0, padx=5)
        
        self.all_off_btn = ttk.Button(button_frame, text="All OFF", command=self.turn_all_off)
        self.all_off_btn.grid(row=0, column=1, padx=5)
        
        self.status_btn = ttk.Button(button_frame, text="Get Status", command=self.get_relay_status)
        self.status_btn.grid(row=0, column=2, padx=5)
        
        # Relay status and control
        self.relay_states = {}  # StringVar for LED display
        self.relay_status = {}  # Current state of each relay (True=ON, False=OFF)
        self.relay_buttons = {}
        
        for i in range(4):
            relay_id = i + 1
            # Relay status label with LED
            self.relay_states[relay_id] = tk.StringVar(value="●")
            self.relay_status[relay_id] = False  # Initialize all relays as OFF
            relay_frame = ttk.Frame(self.main_frame)
            relay_frame.grid(row=i+4, column=0, columnspan=3, pady=2)
            
            ttk.Label(relay_frame, text=f"Relay {relay_id}: ").grid(row=0, column=0)
            led_label = ttk.Label(relay_frame, textvariable=self.relay_states[relay_id], foreground='red', font=('TkDefaultFont', 18, 'bold'))
            led_label.grid(row=0, column=1)
            
            # Toggle button
            toggle_btn = ttk.Button(
                relay_frame, 
                text=f"Toggle {relay_id}",
                command=lambda x=relay_id: self.toggle_relay(x)
            )
            toggle_btn.grid(row=0, column=2, padx=5)
            self.relay_buttons[relay_id] = toggle_btn
        
        # Status bar
        self.status_var = tk.StringVar(value="Status: Disconnected")
        ttk.Label(self.main_frame, textvariable=self.status_var).grid(row=8, column=0, columnspan=3, pady=5)
        
        # Initialize connection
        self.initialize_connection()

    def initialize_connection(self):
        """Initialize connection and get initial status"""
        self.status_var.set("Status: Connecting...")
        threading.Thread(target=self._initialize_async).start()

    def _initialize_async(self):
        """Asynchronous initialization to prevent GUI freezing"""
        try:
            if self.check_health():
                self.get_version()
                self.get_relay_status()
                self.connected = True
                self.status_var.set("Status: Connected ✓")
            else:
                self.status_var.set("Status: Connection Failed")
        except Exception as e:
            self.handle_api_error(str(e))

    def check_health(self):
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/system/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_version(self):
        """Get controller version"""
        try:
            response = requests.get(f"{self.base_url}/system/version", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.version = data.get('version', 'Unknown')
                self.header_var.set(f"Network Relay Controller - v{self.version}")
        except Exception as e:
            self.handle_api_error(f"Version check failed: {str(e)}")

    def get_relay_status(self):
        """Get status of all relays"""
        def update_gui(data):
            for relay in data.get('relays', []):
                relay_id = relay['id']
                state = relay['state']
                if relay_id in self.relay_states:
                    is_on = state == 'ON'
                    color = 'green' if is_on else 'red'
                    self.relay_status[relay_id] = is_on  # Update stored state
                    self.relay_states[relay_id].set("●")
                    for widget in self.main_frame.winfo_children():
                        if isinstance(widget, ttk.Frame):
                            for child in widget.winfo_children():
                                if isinstance(child, ttk.Label) and \
                                   child.cget('textvariable') == str(self.relay_states[relay_id]):
                                    child.configure(foreground=color)

        try:
            response = requests.get(f"{self.base_url}/relay/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.root.after(0, update_gui, data)
                self.status_var.set("Status: Updated successfully")
            else:
                self.status_var.set("Status: Failed to get relay status")
        except Exception as e:
            self.handle_api_error(str(e))

    def toggle_relay(self, relay_id):
        """Toggle specific relay based on its current state"""
        try:
            # Get current state and determine target state
            current_state = self.relay_status.get(relay_id, False)
            # Send opposite command of current state
            command = "off" if current_state else "on"
            
            response = requests.post(
                f"{self.base_url}/relay/{relay_id}/{command}",
                timeout=5
            )
            if response.status_code == 200:
                self.get_relay_status()
            else:
                self.status_var.set(f"Status: Failed to {command} relay {relay_id}")
        except Exception as e:
            self.handle_api_error(str(e))

    def turn_all_on(self):
        """Turn all relays on"""
        try:
            response = requests.post(f"{self.base_url}/relay/all/on", timeout=5)
            if response.status_code == 200:
                self.get_relay_status()
            else:
                self.status_var.set("Status: Failed to turn all relays on")
        except Exception as e:
            self.handle_api_error(str(e))

    def turn_all_off(self):
        """Turn all relays off"""
        try:
            response = requests.post(f"{self.base_url}/relay/all/off", timeout=5)
            if response.status_code == 200:
                self.get_relay_status()
            else:
                self.status_var.set("Status: Failed to turn all relays off")
        except Exception as e:
            self.handle_api_error(str(e))

    def handle_api_error(self, error_msg):
        """Handle API errors"""
        self.status_var.set(f"Error: {error_msg}")
        self.connected = False

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Network Relay Controller GUI')
    parser.add_argument('--host', default='localhost',
                      help='Hostname or IP address of relay controller')
    parser.add_argument('-p', '--port', type=int, default=5000,
                      help='Port number of relay controller API')
    
    parser._optionals.title = 'Available options'
    parser._positionals.title = 'Positional arguments'
    
    return parser.parse_args()

def main():
    """Main entry point"""
    try:
        args = parse_arguments()
        app = RelayControllerGUI(args.host, args.port)
        app.root.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
