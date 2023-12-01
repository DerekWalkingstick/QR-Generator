import os, datetime, subprocess
import tkinter as tk
from segno import make_qr
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage

def on_button_click():
    # Get text from textbox
    text = text_widget.get("1.0", "end-1c")

    # Set image index for png names
    image_index = 0

    # Create empty list to hold dictionary of "file" -> filepath and "value" -> QR value
    png_files = []

    # Get the logged in user download folder
    downloads_folder = os.path.expanduser("~")  # Get the user's home directory
    downloads_folder = os.path.join(downloads_folder, "Downloads")  # Add "Downloads" folder to the path

    # Separate the serials based off enter key
    for row in text.split('\n'):
        # Check if row is empty space
        if row:
            # Make the QR
            qr = make_qr(row, error='h')  # 'h' corresponds to high error correction
            # Save the QR and scale it to 5
            qr.save(f"{downloads_folder}\\qr{image_index}.png", scale=5)
            # Add the filepath and the value to the list
            png_files.append({"file": f"{downloads_folder}\\qr{image_index}.png", "value": row})
            # Increase the name index
            image_index = image_index + 1

    # Create a list of flowable elements (images and values)
    elements = []
    # Create a simple stye layout
    styles = getSampleStyleSheet()
    # Create and normal layout with centered alignment
    normal_style = styles["Normal"]
    normal_style.alignment = 1

    # Loop through png list to create pdf and value labels
    for png_file in png_files:
        # Create a paragraph for the value
        text = Paragraph(png_file["value"], normal_style)
        # Add to pdf layout
        elements.append(text)

        # Open the png image and attach to pdf
        with PILImage.open(png_file["file"]) as img:
            # Get the height and width from the png
            img_width, img_height = img.size
            # Create an image file from the png
            image = Image(png_file["file"], width=img_width, height=img_height)
            # Add the new image to the pdf
            elements.append(image)

    # Create a PDF document with a timestamp file name
    file_name = f'{downloads_folder}\\combined_images_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.pdf'
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    
    # Build the PDF document
    doc.build(elements)

    # Remove the png qr files
    for png_file in png_files:
        os.remove(png_file["file"])

    # Clear the text in the textbox
    text_widget.delete("1.0", "end")

    # Open the pdf file
    subprocess.Popen(file_name,shell=True)

# Create the main application window
app = tk.Tk()
app.title("Text Box Application")

# Create a Text widget (big textbox)
text_widget = tk.Text(app, height=29, width=100)
text_widget.pack()

# Get the screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 800
window_height = 500

# Calculate the x and y coordinates for the center of the screen
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window's geometry to position it in the center of the screen
app.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a Button
button = tk.Button(app, text="Create QR PDF", command=on_button_click)
button.pack()

# Start the Tkinter event loop
app.mainloop()