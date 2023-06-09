import argparse
import os
import time
import logging
from PIL import Image
from plyer import notification

parser = argparse.ArgumentParser(description='Process multiple images expected same resolution.')
parser.add_argument('files', nargs='+', help='Path to the input files')
parser.add_argument('--ext', help='Image format default: .bmp', default='.bmp')
parser.add_argument('-d', '--direction', help='Reading direction (ltr or rtl, default: ltr)', default='ltr')
args = parser.parse_args()

try:
    temp, args.ext = args.ext.split(".")
except ValueError:
    pass

if args.direction != 'rtl':
    args.direction = 'ltr'

def join_images(folder_path, file_name):
    # ファイル名と拡張子を取得
    file_name, file_ext = os.path.splitext(file_name)
    file_name = file_name.split("_")[0]
    os.chdir(folder_path)

    # 分割した画像の最大行と最大列を探す
    max_rows, max_columns = 0, 0

    for file in os.listdir("."):
        if file.startswith(file_name) and file.endswith(file_ext):
            try:
                _, rows_columns = file.split("_")
                rows, columns = rows_columns.replace(file_ext, "").split("^")
            except ValueError:
                logging.debug('ValueError')
                return
            rows, columns = int(rows), int(columns)
            if rows > max_rows:
                max_rows = rows
            if columns > max_columns:
                max_columns = columns

    # ファイル名の配列を作成する NOTE: ("_")("^")
    image_files = [[f"{folder_path}//{file_name}_{r}^{c}{file_ext}" for c in range(1, max_columns+1)] for r in range(1, max_rows+1)]
    # 画像を読み込み、サイズを取得する
    images_rows = [Image.open(temp_name) for temp_name in image_files[0]]

    widths, heights = zip(*(i.size for i in images_rows))

    # 画像を横に並べたときの画像のサイズを計算する
    total_width = sum(widths)
    max_height = max(heights)

    # 画像を縦に並べたときの画像のサイズは乗算に決め打ち
    total_height = max_height * max_rows

    # 新しい画像を作成する
    new_image = Image.new("RGB", (total_width, total_height))

    for r in range(0, max_rows):
        # 画像を新しい画像に貼り付ける
        x_offset = 0
        y_offset = max_height * r
        images_rows = [Image.open(temp_name) for temp_name in image_files[r]]

        if args.direction == 'ltr':
            images_rows = images_rows[::-1]
        for x, image in enumerate(images_rows):
            new_image.paste(image, (x_offset, y_offset))
            x_offset += widths[x]

    new_image.save(f"{folder_path}//{file_name}-結.{args.ext}")

start_time = time.time()
for file_path in args.files:
    orig_folder_path, orig_file_name = os.path.split(file_path)
    if orig_folder_path == "":
        orig_folder_path = os.getcwd()
    # print('Processing folder:',orig_folder_path, 'file:', orig_file_name)
    if orig_file_name.count("_") != 1 or orig_file_name.count("^") != 1:
        print('Skip: allowed filename is {base}_{row}^{column}{.ext}', orig_file_name) # NOTE: ("_")("^")
        continue
    print('Processing file:', orig_file_name)
    join_images(orig_folder_path, orig_file_name)

py_name = os.path.basename(__file__)
print('Done.')
# 処理が3秒超えたら通知をする
end_time = time.time()
processing_time = end_time - start_time
if processing_time > 3:
    notification.notify(title=py_name, message="Done.", timeout=5)
