from micropython import opt_level

opt_level(3)


class Screen:
    def __init__(self, tft, fb):
        self._tft = tft
        self._fb = fb

    def refresh(self, update=True):
        if update:
            self._tft.show(self._fb)

    @staticmethod
    def getColHex(t):
        color = 0
        if type(t) == int:
            color = (t << 16) + (t << 8) + (t)
        elif type(t) == tuple:
            if len(t) == 3:
                color = ((t[0] & 0xFF) << 16) + ((t[1] & 0xFF) << 8) + (t[2] & 0xFF)
            elif len(t) == 1:
                t = t[0] & 0xFF
                color = (t << 16) + (t << 8) + (t)
        return color

    def text(self, text, x: int, y: int, color=255, update=True):
        color = self.getColHex(color)
        if type(text) != str:
            text = str(text)
        self._fb.text(text, x, y, color)
        self.refresh(update)

    def textCh(self, text, x, y, color=255, update=True):
        color = self.getColHex(color)
        if type(text) == list:
            text = bytearray(text).decode()
        elif type(text) != str:
            text = str(text)
        for c in text:
            o = ord(c)
            if o < 127:
                self._fb.text(c, x, y + 4, color)
            else:
                self._fb.textch(o, x, y, color)
            x += 12
        self.refresh(update)

    def fill(self, color=255, update=True):
        color = self.getColHex(color)
        self._fb.fill(color)
        self.refresh(update)

    def clear(self, update=True):
        self._fb.fill(0)
        self.refresh(update)

    def pixel(self, x, y, color=255, update=True):
        color = self.getColHex(color)
        self._fb.pixel(x, y, color)
        self.refresh(update)

    def line(self, x1, y1, x2, y2, color=255, update=True):
        color = self.getColHex(color)
        self._fb.line(x1, y1, x2, y2, color)
        self.refresh(update)

    def rect(self, x, y, w, h, color=255, fill=0, update=True):
        color = self.getColHex(color)
        if fill:
            self._fb.fill_rect(x, y, w, h, color)
        else:
            self._fb.rect(x, y, w, h, color)
        self.refresh(update)

    def triangle(self, x1, y1, x2, y2, x3, y3, color=255, fill=0, update=True):
        color = self.getColHex(color)
        self._fb.triangle(x1, y1, x2, y2, x3, y3, color, fill)
        self.refresh(update)

    def circle(self, x, y, r, color=255, fill=0, update=True):
        color = self.getColHex(color)
        fill = self.getColHex(fill)
        self._fb.circle(x, y, r, color, fill)
        self.refresh(update)

    def loadBmp(self, path, x=0, y=0, update=True):
        self._fb.loadbmp(path, x, y)
        self.refresh(update)
