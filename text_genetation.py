from PIL import Image, ImageDraw, ImageFont


def wmgenerator(size, msg, rgbnumber = 66):
	W, H = (size, size)
	im = Image.new("RGB", (W,H), "gray")
	draw = ImageDraw.Draw(im)
	font = ImageFont.truetype("shrifts/ToyzRegular.ttf", 10) # 11
	colortext = (rgbnumber,rgbnumber,rgbnumber) # "darkgray"
	draw.text((3, 3), msg, fill=colortext, font=font)
	im.save("text.png", "PNG")

if __name__ == "__main__":
	size = 39 # 46
	msg = "+79998\n887766"
	wmgenerator(size, msg)