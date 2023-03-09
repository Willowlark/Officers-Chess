"""
Resize ... and reconfigures. images in a specified directory

Use case:  Images of varying size, need to be enlarged to exaxtly 1200 x 1200
"""
import os
import glob
import fire
from math import ceil, floor

from PIL import Image

SIZE=70
TILESIZE = 16
source_path = '/Users/bill/Code/special-pancake/Python/Officers Chess/images/fe7maps'
destination_path = os.path.join('/Users/bill/Code/special-pancake/Python/Officers Chess/images/Roll20 Maps/')

def sizes(source_path=source_path):

    # List of UNC Image File paths
    images = os.listdir(source_path)

    for image in images:
        if '.png' not in image:
            continue
        original = Image.open(os.path.join(source_path,image))

        # Match original aspect ratio
        dimensions = original.getbbox()
        
        # Calculate matched aspect ratio
        
        width =  int((SIZE-TILESIZE)*(dimensions[2]/TILESIZE)+dimensions[2])
        length = int((SIZE-TILESIZE)*(dimensions[3]/TILESIZE)+dimensions[3])
        print(image, f"Number of {TILESIZE} Tiles: ",dimensions[2]/TILESIZE, dimensions[3]/TILESIZE)

def convert(source_path=source_path, destination_path=destination_path, canvas=None):
    """Kracken Canvas size (4800, 2400)"""

    # List of UNC Image File paths
    images = os.listdir(source_path)

    for image in images:
        if '.png' not in image:
            continue
        original = Image.open(os.path.join(source_path,image))

        # Retain original attributes (ancillary chunks)
        info = original.info
        mode = original.mode
        if original.palette is not None:
            palette = original.palette.getdata()[1]
        else:
            palette = False

        # Match original aspect ratio
        dimensions = original.getbbox()
        print(dimensions)

        # Identify destination image background color
        if 'transparency' in info.keys():
            background = original.info['transparency']
        else:
            # Image does not have transparency set
            print(image)
            background = (64)

        # Get base filename and extension for destination
        filename, extension = image.split('.')
        
        # Calculate matched aspect ratio
        
        width =  int((SIZE-TILESIZE)*(dimensions[2]/TILESIZE)+dimensions[2])
        length = int((SIZE-TILESIZE)*(dimensions[3]/TILESIZE)+dimensions[3])
        
        size = (width, length)
        if canvas:
            # Set desired final image size
            padx = (canvas[0]-width)/2
            pady = (canvas[1]-length)/2
            
            # Calculate center position
            position = (
                int(ceil(padx/50)*50),
                int(ceil(pady/50)*50),
                int(canvas[0] - int(padx/50)*50),
                int(canvas[1] - int(pady/50)*50)
            )
            print(position)
            print(position[0] + (canvas[0]-position[2]) + width)
            print(position[1] + (canvas[1]-position[3]) + length)

        # Enlarge original image proportionally
        resized = original.resize(size, Image.LANCZOS)
        
        if canvas:
            # Then create sized canvas
            final = Image.new(mode, canvas, 'black')

            # Replicate original properties
            final.info = info
            if palette:
                final.putpalette(palette)

            # Center paste resized image to final canvas
            final.paste(resized, position)
        else: final = resized

        # final.show()
        final.save("{}{}.{}".format(destination_path, 'fe7'+filename, extension))
        
if __name__ == '__main__':
    try:  
        fire.Fire() 
    except NotImplementedError:
        pass