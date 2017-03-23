from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import math

class CompositeResizeApp:

    def __init__(self, root, image):
        self.imageData = image.tobytes()
        self.numPixels = image.width * image.height
        self.imageMode = image.mode
        self.width = image.width
        
        root.title("Composite resize")
        # fix entry box issue
        # as a side-effect this may create the window without a frame
        root.overrideredirect(True)

        frame = Frame(root)

        widthFrame = Frame(frame)
        
        widthLabel = Label(widthFrame, text="Width: ")
        widthLabel.pack(side=LEFT)
        self.widthBox = Spinbox(widthFrame, from_=0, to=65536)
        self.widthBox.pack(side=LEFT)
        self.widthBox.delete(0, END)
        self.widthBox.insert(INSERT, str(self.width))

        updateButton = Button(widthFrame, text="Update",
                              command=self._updateImage)
        updateButton.pack(side=LEFT)

        saveButton = Button(widthFrame, text="Save",
                            command=self._saveImage)
        saveButton.pack(side=LEFT)

        quitButton = Button(widthFrame, text="Quit", command=exit)
        quitButton.pack(side=LEFT)
        
        widthFrame.pack(side=TOP, fill="x")

        self.imageCanvas = Canvas(frame)
        self.imageCanvas.pack(side=TOP)

        frame.pack()

        self._updateImage()

    def _updateImage(self):
        try:
            width = int(self.widthBox.get())
        except BaseException:
            self.widthBox.delete(0, END)
            self.widthBox.insert(INSERT, str(self.width))
            return
        height = int(math.floor(float(self.numPixels) / float(width)))
        self.image = Image.frombytes(self.imageMode, (width, height),
                                     self.imageData)
        
        self.imageCanvas.delete("all")
        self.imageCanvas.config(width=image.width, height=image.height)
        self.photoImage = ImageTk.PhotoImage(self.image)
        self.imageSprite = self.imageCanvas.create_image(
            self.image.width/2, self.image.height/2, image=self.photoImage)
        self.imageCanvas.update()

        self.width = width

    def _saveImage(self):
        file = filedialog.asksaveasfile()
        if file == None:
            return
        self.image.save(file.name)

if __name__ == "__main__":
    root = Tk()
    # move the window to the top right corner
    root.geometry('+0+0')
    
    file = filedialog.askopenfile(title="Choose an image...")
    if file == None:
        exit()

    image = Image.open(file.name)
    
    app = CompositeResizeApp(root, image)
    root.mainloop()
