import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import os

from PIL.ImageColor import colormap


class MyTestCase(unittest.TestCase):

    def test_make_color_map(self):
        # im = np.random.choice([0, 1, 10], size=(90, 90), p=[0.5, 0.3, 0.2])
        # im2 = im / 10.
        # clist = [(0, "white"), (1. / 10., "green"), (1, "red")]
        # cmap = plt.cm.colors.LinearSegmentedColormap.from_list("name", clist)
        # mpimg.imsave(__file__ + '.png', im, cmap=cmap)

        CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
        file_name = "test/1ee8d83f26004582a4ff6d832452c514.jpg"
        image_path = (CONFIG_PATH + "/../static/image/" + file_name)
        img = mpimg.imread(image_path)
        colors_from_img = img[:, 0, :]

        my_cmap = plt.cm.colors.LinearSegmentedColormap.from_list('my_cmap', colors_from_img)
        mpimg.imsave(__file__ + '.png', img, cmap=my_cmap)
        # cmap = plt.cm.colors.LinearSegmentedColormap.from_list("name", clist)
        # plt.imshow(indexedImage)
        # colormap(plt.gca, plt.jet(256))
        # plt.colorbar(plt.gca)

    def test_color_map(self):
        np.random.seed(0)
        arr = np.random.standard_normal((8, 100))

        plt.subplot(2, 2, 1)
        # plt.scatter(arr[0], arr[1], c=arr[1], cmap='spring')
        plt.scatter(arr[0], arr[1], c=arr[1])
        plt.spring()
        plt.title('spring')

        plt.subplot(2, 2, 2)
        plt.scatter(arr[2], arr[3], c=arr[3])
        plt.summer()
        plt.title('summer')

        plt.subplot(2, 2, 3)
        plt.scatter(arr[4], arr[5], c=arr[5])
        plt.autumn()

        plt.title('autumn')

        plt.subplot(2, 2, 4)
        plt.scatter(arr[6], arr[7], c=arr[7])
        plt.winter()
        plt.title('winter')

        plt.tight_layout()
        plt.show()
        # print(plt.spring())
        # print(plt.summer())
        # print(plt.autumn())
        # print(plt.winter())

    def test_plt(self):


        # 샘플 그림을 그립시다.
        plt.style.use("default")
        CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
        file_name = "test/4bffe91c93344157a33c94c15c08f867.jpg"
        image_path = (CONFIG_PATH + "/../static/image/"+file_name)
        result_path = (CONFIG_PATH + "/../static/result/"+file_name)

        jpg_img_arr = mpimg.imread(image_path)
        jpg_IMG = Image.open(image_path)
        print(type(jpg_img_arr))  # 얘는 np.array
        print(type(jpg_IMG))  # 얘는 PIL.JpegImagePlugin.JpegImageFile' 오브젝트
        print((jpg_img_arr == np.array(jpg_IMG)).mean())  # 다행히 np.array로 변환이 쉬움.

        height, width, layer = jpg_img_arr.shape

        f, axes = plt.subplots(2, 2, figsize=(8, 8 * height / width))
        ## original img plotting
        axes[0][0].imshow(jpg_img_arr[:, :, :]), axes[0][0].axis('off')
        axes[0][0].set_xticks([]), axes[0][0].set_yticks([])  # 이걸 하지 않으면 tick이 남아있어서 간격이 생김.
        # Red, Green, Blue로 구분하여 표현. colormap 또한, 그 형식에 맞춰서 표현
        # 실제 그림을 보면 색깔별로 어느 정도 구분되어 있는 것을 알 수 있음.
        hsv = plt.cm.get_cmap('hsv')
        # print(hsv.colors)

        print("hsv(range(12)):",hsv(range(12)))
        print("hsv(np.linspace(0,1,12)):",hsv(np.linspace(0,1,12)))
        cmaps = [plt.cm.get_cmap('my_cmap'), plt.cm.get_cmap('gray'), plt.cm.autumn, plt.cm.Pastel2]
        for i in range(1, 4):
            axes[i // 2][i % 2].imshow(jpg_img_arr[:, :, i - 1], cmap=cmaps[i - 1])
            axes[i // 2][i % 2].set_xticks([]), axes[i // 2][i % 2].set_yticks([])  # 이걸 하지 않으면 tick이 남아있어서 간격이 생김.
            axes[i // 2][i % 2].axis('off')
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
        ## sutplots_adjust는 subplot 간에 간격을 붙이려고 쓴건데, 쓰고보니 어떻게 쓰는건지 모르겠음. 그냥 모르겠음...
        plt.margins(0, 0, tight=False)
        # pad_inches를 0으로 두고 저장하면, 공백없이 저장됨.
        plt.savefig(result_path, pad_inches=0)
        plt.show()


if __name__ == '__main__':
    unittest.main()
