from PIL import Image
from io import BytesIO
import base64

# img = Image.open("./backend/template/bird.png")

FIXED_WIDTH = 300
FIXED_HEIGHT = 200

resize = 0.1

with open("./backend/template/bird.png", "rb") as pdf_file:
    encoded_string = base64.b64encode(pdf_file.read())

img = Image.open(BytesIO(base64.b64decode(encoded_string)))
resize = FIXED_WIDTH/img.size[0] if (FIXED_WIDTH/img.size[0] > FIXED_HEIGHT/img.size[1]) else FIXED_HEIGHT/img.size[1]

x = img.size[0]
y = img.size[1]

img = img.resize(( int(x*resize), int(y*resize)),Image.ANTIALIAS)

# img.save("./backend/template/bird-2.png",optimize=True,quality=95)

buffered = BytesIO()
img.save(buffered, format="png")
img_str = base64.b64encode(buffered.getvalue())

print(img_str.decode("utf-8"))
