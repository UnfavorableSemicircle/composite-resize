# composite-resize

A GUI app to adjust the width of a composite (including fractional widths) or to join multiple composites together.

You will need Python 3, tkinter (included with Windows Python installations), and pillow.

- Click `Load Image` to load a new composite image.
- Click `Append Image` to append the data from another composite image to the existing data.
- Enter a number in the `Pixels` box and click `Insert` to insert that many black pixels at the end.
- Enter a number in the `Pixels` box and click `Remove` to remove that many pixels from the end.
- Click `Auto Trim` to automatically remove black pixels from the end of the image data. This might be useful if you are joining 2 composites together (composites images are sometimes padded with black).
- Adjust the `Padding` box and click `Update` or press Enter to add black pixels to the start of the image data.
- Adjust the `Width` box and click `Update` or press Enter to resize the composite. Fractional widths are supported.
- Click `Save` to save the final image. You must specify an extension.
