import sys

from PIL import Image, ImageDraw, ImageFont


class SkyrimStatusMeme:
    font = ImageFont.truetype("userbot/fonts/impact.ttf", 60)
    background = Image.open('userbot/images/skyrim_background.png', 'r')
    finalText = ""
    finalSize = [300, 200]
    imgx = 300
    finalImage = None

    def __init__(self, status, level):
        self.finalText = status.upper() + " : " + level
        offset_counter = 0
        while self.GetSize()[0] > (self.finalSize[0] - 100):
            self.finalSize[0] += 300
            offset_counter += 1
        backgroundImage = Image.new('RGB', self.finalSize, color='#FFF')
        count = 0
        for _ in range(0, offset_counter + 1):
            backgroundImage.paste(self.background, (count, 0))
            count += self.imgx
        draw = ImageDraw.Draw(backgroundImage)
        posx = (backgroundImage.width - self.GetSize()[0]) / 2
        posy = (backgroundImage.height - self.GetSize()[1]) / 2
        draw.text((posx + 3, posy + 3), self.finalText, fill="black", font=self.font)
        draw.text((posx, posy), self.finalText, fill="white", font=self.font)
        self.finalImage = backgroundImage

    def SaveFile(self, filename):
        self.finalImage.save(filename)

    def GetSize(self):
        return self.font.getsize(self.finalText)


if __name__ == '__main__':
    inst = SkyrimStatusMeme(sys.argv[1], sys.argv[2])
    inst.SaveFile('userbot/downloads/skyrim.png')
