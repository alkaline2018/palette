# importing Image module from PIL package
from PIL import Image
from PIL import ImageFilter
import PIL
import os
import numpy as np
import requests

from color_util import ColorUtil

if __name__ == "__main__":
    # opening a  image
    CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_SIZE = (50, 50)
    im = Image.open(CONFIG_PATH + "/../static/image/cafe.jpg").convert("L").convert("RGB")
    # url = "https://imgnews.pstatic.net/image/029/2021/03/12/0002660482_001_20210312070406814.jpg?type=w647"
    # im = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    im = im.resize(IMAGE_SIZE, Image.LANCZOS)
    im.save("../static/result/cafe_resize.jpg")
    # text_list = ["1", "L", "P", "RGB", "RGBA"]
    # text_list = [Image.NEAREST, Image.BOX, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS]
    text_list = [Image.LANCZOS]
    util = ColorUtil()
    # for text in text_list:
    #     # im3 = Image.open(CONFIG_PATH + "/../static/image/변환_157547385_753950011898658_4461242577108582890_n.jpg").convert(text, colors=16).resize((500, 500), Image.LANCZOS)
    #     im3 = Image.open(CONFIG_PATH + "/../static/image/ccb4c7f67589088bdd3320df96aa16bc.png").convert("RGB", colors=256)
    #     # im3 = Image.open(CONFIG_PATH + "/../static/image/ccb4c7f67589088bdd3320df96aa16bc.png").convert("1").resize((300, 300), text)
    #
    #     im3.save("../static/result/2_3_"+str(text)+".png")
    #
    #     pixels5 = list(im3.getdata())
    #     pixels6 = [util.convert_rgb2hex(i) for i in pixels5]
    #     pixels3 = [util.get_normaliztion_hex_by_rgb(i) for i in pixels5]
    #     width3, height3 = im3.size
    #     pixels3 = [pixels3[i * width3:(i + 1) * width3] for i in range(height3)]
    #     pixels6 = [pixels6[i * width3:(i + 1) * width3] for i in range(height3)]
    #     print(f'pixels3: {pixels3[100]}')
    #     print(f'pixels5: {pixels6[100]}')


    # im2 = Image.open(CONFIG_PATH + "/../static/image/대출2.jpg").convert("L")
    im2 = Image.open(CONFIG_PATH + "/../static/image/cafe_3.jpg").convert("L").convert("RGB")
    # url = "https://imgnews.pstatic.net/image/215/2021/03/12/A202103120018_1_20210312063856183.jpg?type=w647"
    # im2 = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    im2 = im2.resize(IMAGE_SIZE, Image.LANCZOS)
    im2.save("../static/result/cafe_4_resize.jpg")

    # getting colors
    # multiband images (RBG)
    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    pixels2 = list(im2.getdata())
    width2, height2 = im2.size
    pixels2 = [pixels2[i * width2:(i + 1) * width2] for i in range(height2)]
    # im11 = Image.Image.getdata(im)
    # print(pixels)
    # im22 = Image.Image.getdata(im2)
    p_list = [x[1::2] for x in pixels[1::2]]
    p_list2 = [x[1::2] for x in pixels2[1::2]]

    # print("print:\n", p_list)
    # print("print2:\n", p_list2)

    if p_list == p_list2:
        print("같다")
    else:
        print("다르다")
        s_result = 0
        s_result2 = 0
        for h in range(len(p_list)):
            for w in range(len(p_list[h])):
                if p_list[h][w] == p_list2[h][w]:
                    s_result = s_result + 1
                else:
                    s_result2 = s_result2 + 1
                    # if s_result2 % 1000 == 0:
                        # print(f"color != :\n\t{p_list[h][w]} : {p_list2[h][w]}")

        print(s_result)
        print(s_result2)
        nomal_p_list = [[util.get_normaliztion_hex_by_rgb(p) for p in p_li] for p_li in p_list]
        nomal_p_list2 = [[util.get_normaliztion_hex_by_rgb(p) for p in p_li] for p_li in p_list2]
        if nomal_p_list == nomal_p_list2:
            print("그래도 같다")
        else:
            result = 0
            result2 = 0
            for h in range(len(nomal_p_list)):
                for w in range(len(nomal_p_list[h])):
                    if nomal_p_list[h][w] == nomal_p_list2[h][w]:
                        result = result + 1
                    else:
                        result2 = result2 + 1
                        if result2 % 100 == 0:
                            print(f"color != :\n\t{nomal_p_list[h][w]} : {nomal_p_list2[h][w]}")
            print(result)
            print(result2)
            # print(nomal_p_list)
            # print(nomal_p_list2)

            print("그래도 다르다")




