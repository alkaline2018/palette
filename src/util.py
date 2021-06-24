import os
import datetime

from PIL import ImageEnhance, ImageFilter


def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def get_dir_path_for_now(_parent_path, _strftime):
    now_date = datetime.datetime.now()
    now_dir_structure = now_date.strftime(_strftime)
    new_dir_path = _parent_path + now_dir_structure
    return new_dir_path

def convert_image_insert(palette, path, down_image_path, image_id, sp_mongo):
    file_name, file_ext = os.path.splitext(path)
    down_file_name, down_file_ext = os.path.splitext(down_image_path)

    img = palette.get_image()
    for i in range(1, 5):
        image_dict = palette.get_defalut_hash_dict().copy()
        image_dict["parentId"] = image_id
        if i == 1:
            # NOTE: 강조 후 그레이 스케일링하여 외곽선 따기
            convert_img = ImageEnhance.Contrast(img).enhance(2).convert("L").filter(ImageFilter.CONTOUR)
        elif i == 2:
            # NOTE: 강조
            convert_img = ImageEnhance.Contrast(img).enhance(2)
        elif i == 3:
            # NOTE: 그레이 스케일링
            convert_img = img.convert("L")
        elif i == 4:
            # NOTE: 밝기 업
            convert_img = ImageEnhance.Brightness(img).enhance(2)
        convert_img.save(file_name+"_"+str(i)+file_ext)
        # TODO: path가 이상할 것임 이 부분 제대로 하자.
        image_dict['path'] = down_file_name + "_" + str(i) + down_file_ext
        image_dict["collectDatetime"] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        _id = sp_mongo.insert_by_dict2(_dict=image_dict)
