import shutil
import os
from pathlib import Path


ab_path = os.path.dirname(os.path.abspath(__file__))
o_path = os.path.join(ab_path, "../public/temp/2020/copy.txt")
n_path = os.path.join(ab_path, "../public/images/2020/copy.txt")
n_dir = os.path.dirname(n_path)
print(n_dir)

if not os.path.exists(n_dir):
    os.makedirs(n_dir)
# shutil.move(o_path, n_path)
shutil.copy(o_path, n_path)
