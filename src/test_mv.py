import shutil
import os


ab_path = os.path.dirname(os.path.abspath(__file__))
o_path = os.path.join(ab_path,"../public/temp/1617697492014_20210331_이미지_4.jpg")
n_path = os.path.join(ab_path,"../public/image/1617697492014_20210331_이미지_4.jpg")
shutil.move(o_path, n_path)
