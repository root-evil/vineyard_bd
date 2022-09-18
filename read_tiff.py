from PIL import Image
import numpy as np
im = Image.open('./data/KRA_ADMIN_100m.tif')
# im.show()



imarray = np.array(im)

new_array = 1
print(imarray)