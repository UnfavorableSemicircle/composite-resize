from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import math

class CompositeResizeApp:

    def __init__(self, root):
        self.image = None
        self.imageData = bytes()
        self.numPixels = 0
        self.imageMode = None
        self.width = 0
        
        root.title("Composite resize")
        # uncomment to fix entry box issue (unable to select)
        # usually switching to another window (including the open dialog) will
        # fix this.
        # as a side-effect this line may create the window without a frame
        # root.overrideredirect(True)

        frame = Frame(root)

        widthFrame = Frame(frame)

        loadButton = Button(widthFrame, text="Load Image",
                            command=self._loadButtonClicked)
        loadButton.pack(side=LEFT)
        
        self.appendButton = Button(widthFrame, text="Append Image",
                                   command=self._appendButtonClicked)
        self.appendButton.pack(side=LEFT)
        
        widthLabel = Label(widthFrame, text="Width: ")
        widthLabel.pack(side=LEFT)
        self.widthBox = Spinbox(widthFrame, from_=0, to=65536)
        self.widthBox.pack(side=LEFT)
        self._updateWidthBox()

        self.updateButton = Button(widthFrame, text="Update",
                                   command=self._updateImage)
        self.updateButton.pack(side=LEFT)

        self.saveButton = Button(widthFrame, text="Save",
                                 command=self._saveImage)
        self.saveButton.pack(side=LEFT)

        #quitButton = Button(widthFrame, text="Quit", command=exit)
        #quitButton.pack(side=LEFT)
        
        widthFrame.pack(side=TOP, fill="x")

        self.imageCanvas = Canvas(frame)
        self.imageCanvas.pack(side=TOP)

        frame.pack()

        self._updateImage()

    def _enableInterface(self):
        self.appendButton.config(state=NORMAL)
        self.widthBox.config(state=NORMAL)
        self.updateButton.config(state=NORMAL)
        self.saveButton.config(state=NORMAL)

    def _disableInterface(self):
        self.appendButton.config(state=DISABLED)
        self.widthBox.config(state=DISABLED)
        self.updateButton.config(state=DISABLED)
        self.saveButton.config(state=DISABLED)

    def _updateWidthBox(self):
        prevState = self.widthBox['state']
        self.widthBox.config(state=NORMAL) # must be enabled to change value
        self.widthBox.delete(0, END)
        self.widthBox.insert(INSERT, str(self.width))
        self.widthBox.config(state=prevState)

    def _chooseImage(self):
        file = filedialog.askopenfile(title="Choose an image...")
        if file == None:
            return None

        try:
            image = Image.open(file.name)
        except BaseException as e:
            messagebox.showerror("Error reading image!", str(e))
            return None
        return image

    def _loadButtonClicked(self):
        image = self._chooseImage()
        if image == None:
            return
        
        self.imageData = image.tobytes()
        self.numPixels = image.width * image.height
        self.imageMode = image.mode
        self.width = image.width
        self._updateWidthBox()
        self._updateImage()

    def _appendButtonClicked(self):
        image = self._chooseImage()
        if image == None:
            return
        
        self.imageData += image.tobytes()
        self.numPixels += image.width * image.height
        if self.imageMode != image.mode:
            messagebox.showerror(
                "Warning!",
                "Appended image mode (" + image.mode + ") doesn't match "
                "existing image mode (" + self.imageMode + ")")
        self._updateImage()

    def _updateImage(self):
        if len(self.imageData) == 0:
            self._disableInterface()
            self.imageCanvas.delete("all")
            return
        
        try:
            width = int(self.widthBox.get())
        except BaseException:
            self._updateWidthBox()
            return
        if width <= 0:
            self._updateWidthBox()
            return
        height = int(math.floor(float(self.numPixels) / float(width)))
        self.image = Image.frombytes(self.imageMode, (width, height),
                                     self.imageData)
        
        self.imageCanvas.delete("all")
        self.imageCanvas.config(width=self.image.width,
                                height=self.image.height)
        self.photoImage = ImageTk.PhotoImage(self.image)
        self.imageSprite = self.imageCanvas.create_image(
            self.image.width/2, self.image.height/2, image=self.photoImage)
        self.imageCanvas.update()

        self.width = width

        self._enableInterface()

    def _saveImage(self):
        file = filedialog.asksaveasfile()
        if file == None:
            return
        try:
            try:
                self.image.save(file.name)
            except KeyError as e:
                self.image.save(file.name + ".png")
        except BaseException as e:
            messagebox.showerror("Error saving image!", str(e))

if __name__ == "__main__":
    root = Tk()
    # move the window to the top right corner
    root.geometry('+0+0')
    
    app = CompositeResizeApp(root)
    root.mainloop()
