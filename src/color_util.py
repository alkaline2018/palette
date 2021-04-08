class ColorUtil:

    def convert_rgb2hex(self, _rgb):
        hex = '#%02x%02x%02x' % _rgb
        return hex

    def get_normaliztion_hex_by_rgb(self, _rgb):
        hex = self.convert_rgb2hex(_rgb)
        normal_hex = self.convert_normaliztion_by_hex(hex)
        return normal_hex

    def convert_normaliztion_by_hex(self, _hex):
        nomal_hex = ("#" + _hex[1] + _hex[1] + _hex[3] + _hex[3] + _hex[5] + _hex[5])
        return nomal_hex
