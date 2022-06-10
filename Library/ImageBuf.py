import framebuf

class ImageBuf(framebuf.FrameBuffer):
    def __init__(self, width, height, binimg):
        self.width = width
        self.height = height
        
        self.buffer = bytearray(binimg)  # bytearray(self.height * self.width * 2)
        # assert(len(self.buffer) == self.width * self.height * 2, "imagesize error")  # Not working well...
        
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)