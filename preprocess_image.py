from PIL import Image

def preprocess_image(image_name, size, rgbnumber = 66):
    img = Image.open(image_name)
    x, y = img.size
    x1, y1 = size, y*size//x
    # print(x1, y1)
    img = img.resize((x1, y1), 1)
    colorback = (rgbnumber,rgbnumber,rgbnumber)
    im = Image.new("RGB", (x1, x1), colorback)
    im.paste(img, (0, (size-y1)//2)) 
    im.convert('L').save(image_name, 'jpeg') 
       
if __name__ == "__main__":
    size = 1280
    image_name = "d.jpg"
    preprocess_image(image_name, size)