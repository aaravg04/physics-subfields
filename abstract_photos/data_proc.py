# biophys/abstract_photos/data_proc.py

import os
import pandas as pd
from tkinter import Tk, Label, Entry, Button, Canvas
from PIL import Image, ImageTk

def process_images(data_directory):
    # Create a DataFrame to store the results
    results = pd.DataFrame(columns=['filename', 'input_string'])
    
    # Load existing results if the CSV file exists
    if os.path.exists("text_image_link.csv"):
        results = pd.read_csv("text_image_link.csv")

    previous_input = ""  # Variable to store the previous input string

    # Iterate through each image in the data directory
    for filename in sorted(os.listdir(data_directory), key=lambda x: int(x.split("_")[1].split(".")[0])):
        # Check if the filename is already in results to skip processed images
        if filename in results['filename'].values:
            continue  # Skip already processed images

        print(filename)
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Add more formats if needed
            # Display the image and take input
            root = Tk()
            img_path = os.path.join(data_directory, filename)
            img = Image.open(img_path)

            # Set maximum display size
            max_display_size = (800, 800)  # Maximum size for display

            # Calculate new dimensions while maintaining aspect ratio
            img.thumbnail(max_display_size, Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            # Create a canvas to display the image
            canvas = Canvas(root, width=img.width, height=img.height)
            canvas.pack()

            # Display the image on the canvas
            canvas.create_image(0, 0, anchor='nw', image=img_tk)

            # Resize the window to fit the canvas with padding
            padding = 20  # Padding around the image
            window_width = img.width + padding
            window_height = min(img.height + padding + 100, 800)  # Limit height to 800
            root.geometry(f"{window_width}x{window_height}")

            entry = Entry(root)
            entry.pack(pady=(padding // 2))
            entry.insert(0, previous_input)  # Pre-fill with previous input

            def submit():
                nonlocal previous_input  # Use the nonlocal variable
                input_string = entry.get()
                results.loc[len(results)] = [filename, input_string]
                previous_input = input_string  # Update previous input
                results.to_csv("text_image_link.csv", index=False)  # Save after each submission
                root.destroy()

            def skip():
                nonlocal previous_input  # Use the nonlocal variable
                results.loc[len(results)] = [filename, previous_input]  # Use previous input
                results.to_csv("text_image_link.csv", index=False)  # Save after skipping
                root.destroy()

            # Bind keyboard shortcuts
            root.bind('<Command-Return>', lambda event: submit())  # Cmd + Enter
            root.bind('<Command-k>', lambda event: skip())        # Cmd + K

            submit_button = Button(root, text="Submit", command=submit)
            submit_button.pack(pady=(padding // 2))

            skip_button = Button(root, text="Skip", command=skip)
            skip_button.pack(pady=(padding // 2))

            root.mainloop()

    # Final save of the DataFrame to a CSV file
    results.to_csv("text_image_link.csv", index=False)

# Call the function with the appropriate directory
process_images('data')
