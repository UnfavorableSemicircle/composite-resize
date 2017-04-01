from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import math

def modePixelSize(mode):
    modeSizes = {"L": 1, "P": 1, "RGB": 3, "RGBA": 4, "CMYK": 4, "YCbCr": 3,
                 "LAB": 3, "HSV": 3, "I": 4, "F": 4}
    return modeSizes[mode]

def emptyBytes(length):
    return bytes([0 for i in range(0, int(length))])

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

        toolbar = Frame(frame)

        loadButton = Button(toolbar, text="Load Image",
                            command=self._loadButtonClicked)
        loadButton.pack(side=LEFT)
        
        self.appendButton = Button(toolbar, text="Append Image",
                                   command=self._appendButtonClicked)
        self.appendButton.pack(side=LEFT)

        self.trimButton = Button(toolbar, text="Trim End",
                                 command=self._trimEnd)
        self.trimButton.pack(side=LEFT)

        paddingLabel = Label(toolbar, text="Padding: ")
        paddingLabel.pack(side=LEFT)
        self.paddingBox = Spinbox(toolbar, from_=0, to=65536)
        self.paddingBox.pack(side=LEFT)
        self.paddingBox.bind('<Return>', self._updateImageEvent)
        self._clearPaddingBox()
        
        widthLabel = Label(toolbar, text="Width: ")
        widthLabel.pack(side=LEFT)
        self.widthBox = Spinbox(toolbar, from_=0, to=65536)
        self.widthBox.pack(side=LEFT)
        self.widthBox.bind('<Return>', self._updateImageEvent)
        self._updateWidthBox()

        self.updateButton = Button(toolbar, text="Update",
                                   command=self._updateImage)
        self.updateButton.pack(side=LEFT)

        self.saveButton = Button(toolbar, text="Save",
                                 command=self._saveImage)
        self.saveButton.pack(side=LEFT)

        #quitButton = Button(toolbar, text="Quit", command=exit)
        #quitButton.pack(side=LEFT)
        
        toolbar.pack(side=TOP, fill="x")

        self.imageCanvas = Canvas(frame)
        self.imageCanvas.pack(side=TOP)

        frame.pack()

        self._updateImage()

    def _enableInterface(self):
        self.appendButton.config(state=NORMAL)
        self.trimButton.config(state=NORMAL)
        self.widthBox.config(state=NORMAL)
        self.paddingBox.config(state=NORMAL)
        self.updateButton.config(state=NORMAL)
        self.saveButton.config(state=NORMAL)

    def _disableInterface(self):
        self.appendButton.config(state=DISABLED)
        self.trimButton.config(state=DISABLED)
        self.widthBox.config(state=DISABLED)
        self.paddingBox.config(state=DISABLED)
        self.updateButton.config(state=DISABLED)
        self.saveButton.config(state=DISABLED)

    def _trimEnd(self):
        pixelSize = modePixelSize(self.imageMode)
        i = self.numPixels - 1
        while i >= 0:
            pixels = self.imageData[i*pixelSize:(i+1)*pixelSize]
            if self.imageMode == 'RGBA':
                pixels = pixels[:3] # ignore alpha
            black = True
            for pixel in pixels:
                if pixel != 0:
                    black = False
                    break
            if not black:
                break
            i -= 1
        i += 1
        if i == self.numPixels:
            messagebox.showinfo("Trim", "Nothing to trim")
        else:
            pixelsTrimmed = self.numPixels - i
            self.imageData = self.imageData[:i*pixelSize]
            self.numPixels = i
            self._updateImage()
            messagebox.showinfo("Trim",
                "Trimmed " + str(pixelsTrimmed) + " pixels")

    def _updateWidthBox(self):
        prevState = self.widthBox['state']
        self.widthBox.config(state=NORMAL) # must be enabled to change value
        self.widthBox.delete(0, END)
        self.widthBox.insert(INSERT, str(self.width))
        self.widthBox.config(state=prevState)

    def _clearPaddingBox(self):
        prevState = self.paddingBox['state']
        self.paddingBox.config(state=NORMAL) # must be enabled to change value
        self.paddingBox.delete(0, END)
        self.paddingBox.insert(INSERT, '0')
        self.paddingBox.config(state=prevState)

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
        self._clearPaddingBox()
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

    def _updateImageEvent(self, event):
        self._updateImage()

    def _updateImage(self):
        if len(self.imageData) == 0:
            self._disableInterface()
            self.imageCanvas.delete("all")
            return
        
        try:
            width = float(self.widthBox.get())
        except BaseException:
            self._updateWidthBox()
        if width <= 0:
            self._updateWidthBox()

        try:
            padding = int(self.paddingBox.get())
        except BaseException:
            self._clearPaddingBox()
            padding = 0
        if padding <= 0:
            self._clearPaddingBox()
            padding = 0
        
        pixelBytes = modePixelSize(self.imageMode)
        if width % 1.0 == 0.0:
            imageData = self.imageData
        else:
            # width is a fraction
            widthError = 0
            imageData = bytes()
            i = 0
            while i < self.numPixels:
                addedPixels = int(math.floor(width))
                if widthError > 1:
                    addedPixels += 1
                    widthError -= 1
                widthError += width % 1.0
                nextI = i + addedPixels
                if nextI > self.numPixels:
                    nextI = self.numPixels
                imageData += self.imageData[i*pixelBytes : nextI*pixelBytes]
                missedPixels = int(math.ceil(width)) - addedPixels
                imageData += emptyBytes(missedPixels*pixelBytes)
                i = nextI

        imageData = emptyBytes(padding * pixelBytes) + imageData
        height = int(math.ceil(
            float(len(imageData)) / pixelBytes / math.ceil(width)))
        imageData += emptyBytes(math.ceil(width) * pixelBytes)
        self.image = Image.frombytes(self.imageMode,
                                     (int(math.ceil(width)), height),
                                     imageData)
        
        self.imageCanvas.delete("all")
        self.imageCanvas.config(width=self.image.width + 4,
                                height=self.image.height + 4)
        self.photoImage = ImageTk.PhotoImage(self.image)
        self.imageSprite = self.imageCanvas.create_image(
            self.image.width/2 + 2,
            self.image.height/2 + 2,
            image=self.photoImage)
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
