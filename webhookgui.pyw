import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json
import time

# Define the functions for various webhook actions
def send_request(url, method='GET', data=None, files=None):
    try:
        if method == 'DELETE':
            response = requests.delete(url)
        elif method == 'POST':
            response = requests.post(url, json=data, files=files)
        else:
            response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def delete_webhook():
    url = url_entry.get()
    response = send_request(url, method='DELETE')
    if response:
        messagebox.showinfo("Success", "Webhook successfully deleted.")

def send_private_message():
    url = url_entry.get()
    message = private_message_entry.get()
    data = {"content": message}
    response = send_request(url, method='POST', data=data)
    if response:
        messagebox.showinfo("Success", "Private message successfully sent.")

def send_skid_hunter_message():
    url = url_entry.get()
    embed = {
        "embeds": [
            {
                "title": "This Webhook has been taken down",
                "description": "Webhook GUI by Unknown Destroyer",
                "fields": [
                    {
                        "name": "Webhook GUI",
                        "value": "Unknown Destroyer"
                    },
                    {
                        "name": "Links",
                        "value": "[TikTok - Unknown Destroyer](https://www.tiktok.com/@unknown_napim) & [YouTube - Sam Horde Songs](https://www.youtube.com/@samhordesongs)"
                    }
                ],
                "footer": {
                    "text": "Unknown Destroyer🤝SamHorde Songs🤝Skid Hunters🤝Anonymous"
                },
                "color": 16711680
            }
        ]
    }
    response = send_request(url, method='POST', data=embed)
    if response:
        messagebox.showinfo("Success", "Skid Hunter message successfully sent.")

def send_file():
    url = url_entry.get()
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = send_request(url, method='POST', files=files)
            if response.ok:
                messagebox.showinfo("Success", "File successfully sent.")
            else:
                messagebox.showerror("Error", "An error occurred while sending the file.")

def collect_info():
    source_url = url_entry.get()
    target_url = collect_info_target_entry.get()
    response = send_request(source_url)
    if response:
        data = response.json()
        send_request(target_url, method='POST', data=data)
        messagebox.showinfo("Success", "Information collected and sent successfully.")

def spam_message():
    url = url_entry.get()
    message = spam_message_entry.get()
    count = int(spam_count_entry.get())
    for _ in range(count):
        data = {"content": message}
        send_request(url, method='POST', data=data)
    messagebox.showinfo("Success", "Spam messages successfully sent.")

def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg='black')

def on_focusout(entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')

def animate_opening():
    root.update_idletasks()
    for i in range(1, 41):
        root.geometry(f"{i * 10 + 200}x{i * 5 + 150}+{int(root.winfo_x())}+{int(root.winfo_y() + i * 2)}")
        root.update()
        time.sleep(0.01)
    root.geometry("500x400")  # Set final size

def animate_closing():
    for i in range(40, 0, -1):
        root.geometry(f"{i * 10 + 200}x{i * 5 + 150}+{int(root.winfo_x())}+{int(root.winfo_y() + i * 2)}")
        root.update()
        time.sleep(0.01)
    root.destroy()

# GUI
root = tk.Tk()
root.title("Discord Webhook Tool")

# Center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

# Set initial size
root.geometry("500x400")

# Center the window
center_window(root, 500, 400)

# Webhook URL Entry
tk.Label(root, text="- Target Webhook URL -").pack(pady=10)
tk.Label(root, text="Webhook URL here:").pack()
url_entry = tk.Entry(root, width=50, fg='grey')
url_entry.insert(0, "Webhook URL here")
url_entry.bind("<FocusIn>", lambda e: on_entry_click(e, url_entry, "Webhook URL here"))
url_entry.bind("<FocusOut>", lambda e: on_focusout(url_entry, "Webhook URL here"))
url_entry.pack()

# Private Message Section
tk.Label(root, text="- Private Message -").pack(pady=10)
tk.Label(root, text="Your Message Here:").pack()
private_message_entry = tk.Entry(root, width=50, fg='grey')
private_message_entry.insert(0, "Your Message Here")
private_message_entry.bind("<FocusIn>", lambda e: on_entry_click(e, private_message_entry, "Your Message Here"))
private_message_entry.bind("<FocusOut>", lambda e: on_focusout(private_message_entry, "Your Message Here"))
private_message_entry.pack()
tk.Button(root, text="Send Private Message", command=send_private_message).pack(pady=5)

# Spam Message Section
tk.Label(root, text="- Spam Message -").pack(pady=10)
tk.Label(root, text="Message here:").pack()
spam_message_entry = tk.Entry(root, width=50, fg='grey')
spam_message_entry.insert(0, "Message here")
spam_message_entry.bind("<FocusIn>", lambda e: on_entry_click(e, spam_message_entry, "Message here"))
spam_message_entry.bind("<FocusOut>", lambda e: on_focusout(spam_message_entry, "Message here"))
spam_message_entry.pack()
tk.Label(root, text="Count here:").pack()
spam_count_entry = tk.Entry(root, width=10, fg='grey')
spam_count_entry.insert(0, "Count here")
spam_count_entry.bind("<FocusIn>", lambda e: on_entry_click(e, spam_count_entry, "Count here"))
spam_count_entry.bind("<FocusOut>", lambda e: on_focusout(spam_count_entry, "Count here"))
spam_count_entry.pack()
tk.Button(root, text="Spam Message", command=spam_message).pack(pady=5)

# Send File Section
tk.Label(root, text="- Send File -").pack(pady=10)
tk.Button(root, text="Select File", command=send_file).pack(pady=5)

# Collect Info Section
tk.Label(root, text="- Collect Info -").pack(pady=10)
tk.Label(root, text="The webhook URL will info sent:").pack()
collect_info_target_entry = tk.Entry(root, width=50, fg='grey')
collect_info_target_entry.insert(0, "The webhook URL will info sent")
collect_info_target_entry.bind("<FocusIn>", lambda e: on_entry_click(e, collect_info_target_entry, "The webhook URL will info sent"))
collect_info_target_entry.bind("<FocusOut>", lambda e: on_focusout(collect_info_target_entry, "The webhook URL will info sent"))
collect_info_target_entry.pack()
tk.Button(root, text="Collect Info", command=collect_info).pack(pady=5)

# Send Skid Hunter Message & Delete Webhook Section
tk.Label(root, text="- Send Skid Hunter Message & Delete the Webhook -").pack(pady=10)
tk.Button(root, text="Send Skid Hunter Message", command=send_skid_hunter_message).pack(side=tk.LEFT, padx=10, pady=5)
tk.Button(root, text="Delete Webhook", command=delete_webhook).pack(side=tk.RIGHT, padx=10, pady=5)

# Bind closing animation
root.protocol("WM_DELETE_WINDOW", animate_closing)



root.mainloop()
