import os
import subprocess
import tkinter as tk
from tkinter import ttk

def get_display_output():
    try:
        result = subprocess.run(["xrandr"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if " connected" in line:
                return line.split()[0]  # Extract the display name
    except Exception as e:
        print(f"Error detecting display output: {e}")
        return "VGA-1"  # Default fallback

def get_current_brightness():
    try:
        result = subprocess.run(["xrandr", "--verbose"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Brightness" in line:
                return float(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error getting brightness: {e}")
        return None  # Return None for errors

    return None  # Return None if Brightness not found

def set_brightness(value):
    display_output = get_display_output()  # Detect the correct output
    os.system(f"xrandr --output {display_output} --brightness {float(value)/100}")

def on_brightness_change(value):
    set_brightness(value)

def update_label(value, brightness_label):
    brightness_label.config(text=f"Brightness: {int(float(value))}%")

def decrease_brightness(event, slider, brightness_label):
    current_value = slider.get()
    new_value = max(10, current_value - 1)
    slider.set(new_value)
    on_brightness_change(new_value)
    update_label(new_value, brightness_label)

def increase_brightness(event, slider, brightness_label):
    current_value = slider.get()
    new_value = min(100, current_value + 1)
    slider.set(new_value)
    on_brightness_change(new_value)
    update_label(new_value, brightness_label)

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Monitor Brightness Control")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TScale", sliderlength=30, thickness=15)

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0)

    current_brightness = get_current_brightness() * 100 if get_current_brightness() else 100

    brightness_slider = ttk.Scale(
        frame, from_=10, to=100, orient='horizontal', length=300, style="TScale", command=on_brightness_change
    )
    brightness_slider.set(current_brightness)
    brightness_slider.grid(row=0, column=0, pady=20, padx=10)

    brightness_label = ttk.Label(frame, text=f"Brightness: {int(current_brightness)}%")
    brightness_label.grid(row=1, column=0)

    brightness_slider.config(command=lambda v: [on_brightness_change(v), update_label(v, brightness_label)])

    # Pass the slider and label as arguments to the key binding functions
    root.bind("<Left>", lambda event: decrease_brightness(event, brightness_slider, brightness_label))
    root.bind("<Right>", lambda event: increase_brightness(event, brightness_slider, brightness_label))
    root.bind("<Escape>", lambda event: root.quit())  # Close with Escape key

    root.mainloop()

if __name__ == "__main__":
    main()
