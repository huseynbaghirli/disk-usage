# -*- coding: utf-8 -*-
import os
import sys
import re
import paramiko
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from tkinter import ttk
import yaml
import base64

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DiskUsageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Usage Checker")
        
        # Set window size
        self.root.geometry("1600x900")
        self.root.configure(bg='#1c1c1c')
        
        # Font settings
        self.font_style = ("Courier", 15)
        
        # Title label
        self.title_label = tk.Label(root, text="Disk Usage Checker", font=("Helvetica", 28, "bold"), bg='#1c1c1c', fg='#f39c12')
        self.title_label.pack(pady=20)

        # Text area
        self.text_area = scrolledtext.ScrolledText(root, width=170, height=26, font=self.font_style, bg="#2c2c2c", fg="white", insertbackground="white", state='disabled')
        self.text_area.pack(pady=20)

        # Check button
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 14, 'bold'), borderwidth=4, focusthickness=3, focuscolor='none', padding=10, foreground='black', background='#3498db')
        style.map('TButton', foreground=[('active', 'white')], background=[('active', '#2980b9')])

        self.button_frame = tk.Frame(root, bg='#1c1c1c')
        self.button_frame.pack(pady=10)

        self.check_button = ttk.Button(self.button_frame, text="Check Disk Usage", command=self.check_disk_usage, style='TButton')
        self.check_button.pack(side='left', padx=10)

        self.night_mode_button = ttk.Button(self.button_frame, text="Toggle Night Mode", command=self.toggle_night_mode, style='TButton')
        self.night_mode_button.pack(side='left', padx=10)

        # Color settings
        self.text_area.tag_configure("header", font=("Courier", 14, "bold"), foreground="white")
        self.text_area.tag_configure("red", foreground="red")
        self.text_area.tag_configure("yellow", foreground="yellow")
        self.text_area.tag_configure("blue", foreground="blue")
        self.text_area.tag_configure("green", foreground="green")
        self.text_area.tag_configure("reset", foreground="white")
        
        # Initial text
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, "Click 'Check Disk Usage' button.\n", "header")
        self.text_area.config(state='disabled')
        
        self.night_mode = True  # Initial night mode state

    def toggle_night_mode(self):
        if self.night_mode:
            self.root.configure(bg='white')
            self.title_label.configure(bg='white', fg='#333')
            self.text_area.configure(bg="white", fg="black", insertbackground="black")
            self.button_frame.configure(bg='white')
            self.night_mode = False
        else:
            self.root.configure(bg='#1c1c1c')
            self.title_label.configure(bg='#1c1c1c', fg='#f39c12')
            self.text_area.configure(bg="#2c2c2c", fg="white", insertbackground="white")
            self.button_frame.configure(bg='#1c1c1c')
            self.night_mode = True

    def ssh_command(self, ip, password, command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, username='test', password=password)
            stdin, stdout, stderr = client.exec_command(command)
            result = stdout.read().decode('utf-8')
        except Exception as e:
            result = f"Error connecting to {ip}: {str(e)}"
        finally:
            client.close()
        return result

    def read_server_file(self):
        server_file = resource_path('servers.yaml')
        with open(server_file, 'r') as file:
            servers = yaml.safe_load(file)
        return servers

    def decrypt_password(self, encrypted_password):
        # In this example, we assume your password is encrypted with Base64.
        return base64.b64decode(encrypted_password).decode('utf-8')

    def check_disk_usage(self):
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, tk.END)
        encrypted_password = "eW91cl9wYXNzd29yZA=="  # Encrypted password
        
        password = self.decrypt_password(encrypted_password)
        
        servers = self.read_server_file()
        
        for group, data in servers.items():
            default_grep = data['grep']
            ips = data['ips']
            self.text_area.insert(tk.END, "\n{:^160}\n".format(group), "header")
            self.text_area.insert(tk.END, "{:<20} {:<30} {:<35} {:<10} {:<10} {:<10} {:<10}\n".format(
                "IP Address", "Hostname", "Filesystem", "Size", "Used", "Avail", "Use%", "Mounted on"))

            for ip_info in ips:
                if isinstance(ip_info, dict):
                    ip = ip_info['ip']
                    grep = ip_info.get('grep', default_grep)
                else:
                    ip = ip_info
                    grep = default_grep
                hostname = self.ssh_command(ip, password, 'hostname').strip()
                disk_usage = self.ssh_command(ip, password, f'df -h | grep {grep}')
                lines = disk_usage.split("\n")
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 6:
                        usage = int(parts[4].replace('%', ''))
                        color = "reset"
                        if usage > 90:
                            color = "red"
                        elif usage > 70:
                            color = "yellow"
                        elif usage > 50:
                            color = "blue"
                        else:
                            color = "green"
                        self.text_area.insert(tk.END, "{:<20} {:<30} {:<35} {:<10} {:<10} {:<10} {:<10}\n".format(
                            ip, hostname, parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]), color)

        self.text_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskUsageApp(root)
    root.mainloop()
