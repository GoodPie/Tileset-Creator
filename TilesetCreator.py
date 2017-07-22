import os
from math import sqrt, ceil
from tkinter import Frame, Tk, Label, Entry, Button, filedialog, StringVar, IntVar, messagebox
from tkinter.messagebox import showerror

from PIL import Image


class TilesetCreator(Frame):
    """
    Converts smaller individual tiles into one tileset image
    Will not keep aspect ratio so ensure that images are the correct aspect ratio before running
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.open_dir = StringVar()
        self.tile_width = IntVar()
        self.tile_height = IntVar()
        self.output_dir = StringVar()

        self.init_ui()

    def init_ui(self):
        """
        Initializes all the widgets and UI elements
        :return: None
        """
        # Configure the frame
        self.parent.title("Tileset Creator")
        self.parent.config(padx=4, pady=4)
        self.parent.resizable(0, 0)

        # Create the main widgets
        # Tile Width
        Label(self.parent, text="Tile Width: ").grid(row=0, column=0, columnspan=2)
        Entry(self.parent, width=3, textvariable=self.tile_width).grid(row=1, column=0, columnspan=2)
        self.tile_width.set(32)

        # Tile Height
        Label(self.parent, text="Tile Height: ").grid(row=2, column=0, columnspan=2)
        Entry(self.parent, width=3, textvariable=self.tile_height).grid(row=3, column=0, columnspan=2)
        self.tile_height.set(32)

        # Image Directory
        Label(self.parent, text="Image Directory: ").grid(row=4, column=0, columnspan=2)
        Entry(self.parent, width=32, textvariable=self.open_dir).grid(row=5, column=0)
        Button(self.parent, text="...", command=self.choose_in_dir).grid(row=5, column=1)

        # Output Directory
        Label(self.parent, text="Output Directory: ").grid(row=6, column=0, columnspan=2)
        Entry(self.parent, width=32, textvariable=self.output_dir).grid(row=7, column=0)
        Button(self.parent, text="...", command=self.choose_out_dir).grid(row=7, column=1)

        # Action button
        Button(self.parent, text="Create Tileset", command=self.create_tileset).grid(row=8, column=0, columnspan=2)

    def choose_in_dir(self):
        """
        Opens the Tkinter choose dir dialog and then sets the dir entry to the directory chosen
        :return: None
        """
        directory = filedialog.askdirectory()
        self.open_dir.set(directory)

    def choose_out_dir(self):
        """
        Opens the Tkinter choose dir dialog and then sets the output dir entry to the directory chosen
        :return: None
        """
        directory = filedialog.askdirectory()
        self.output_dir.set(directory)

    def create_tileset(self):
        """
        Create the tileset image by opening each of the tile images, resizing them to the appropriate size and then
        placing them in a larger image
        :return: None
        """
        # Ensure the directory isn't empty
        if self.open_dir.get() is None or self.open_dir.get() == "":
            showerror("Error", "Invalid directory selected")
            return

        file_count = 0
        for file in os.listdir(self.open_dir.get()):
            if file.endswith(".png") or file.endswith(".jpg"):
                file_count += 1

        # Ensure there are actual files
        if file_count <= 0:
            showerror("Error", "Could not find any .png or .jpg files")
            return

        # Amount of tiles across and down (total tiles = tiles * tiles)
        tiles = int(ceil(sqrt(file_count)))

        # Create the parent image for the tileset (where the tiles will be pasted)
        image_width = tiles * self.tile_width.get()
        image_height = tiles * self.tile_height.get()
        tileset = Image.new("RGBA", (image_width, image_height), "white")

        # Loop through all the images and paste them into the appropriate positions in the tileset
        row = 0
        column = 0
        for file in os.listdir(self.open_dir.get()):

            # Only worried about images ending with common formats (jpg and png)
            if file.endswith(".png") or file.endswith(".jpg"):

                # Open the image and scale down using LANCZOS (best scaling, poor performance)
                tile = Image.open(self.open_dir.get() + "/" + file)
                tile = tile.resize((self.tile_width.get(), self.tile_height.get()), Image.LANCZOS)

                # Paste the tile into the tileset
                y_pos = int(column * self.tile_width.get())
                x_pos = int(row * self.tile_height.get())
                tileset.paste(tile, (y_pos, x_pos))

                # Handle coordinate changes
                column += 1
                if column > tiles:
                    column = 0
                    row += 1

        # Save the output to the same directory this script was run
        outfile = self.output_dir.get() + "/tileset.png"
        tileset.save(outfile, "png")
        messagebox.showinfo("Complete", "Tileset saved to " + outfile)


def main():
    """
    Run the application
    :return: None
    """
    root = Tk()
    app = TilesetCreator(root)
    app.mainloop()


if __name__ == "__main__":
    main()
