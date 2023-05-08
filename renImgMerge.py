import argparse
import os
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

def join_images(folder_path, file_path):
    # ファイル名と拡張子を取得
    file_name, file_ext = file_path.split(".")
    orig_file_name = file_name.split('_')[0]
    os.chdir(folder_path)
    file_ext = '.' + file_ext
    # 分割した画像の最大行と最大列を探す
    max_rows, max_columns = 0, 0

    for file in os.listdir("."):
        if file.startswith(orig_file_name) and file.endswith(file_ext):
            try:
                _, rows_columns = file.split("_")
                rows, columns = rows_columns.replace(file_ext, "").split("x")
            except ValueError:
                logging.debug('ValueError')
                return
            rows, columns = int(rows), int(columns)
            if rows > max_rows:
                max_rows = rows
            if columns > max_columns:
                max_columns = columns

    # ファイル名の配列を作成する
    image_files = [[f"{folder_path}//{orig_file_name}_{r}x{c}{file_ext}" for c in range(1, max_columns+1)] for r in range(1, max_rows+1)]
    # 画像を読み込み、サイズを取得する
    images_rows = [Image.open(temp_name) for temp_name in image_files[0]]

    widths, heights = zip(*(i.size for i in images_rows))

    # 画像を横に並べたときの画像のサイズを計算する
    total_width = sum(widths)
    max_height = max(heights)

    # 画像を縦に並べたときの画像のサイズは乗算
    total_height = max_height * max_rows

    # 新しい画像を作成する
    new_image = Image.new("RGB", (total_width, total_height))

    for r in range(0, max_rows):
        # 画像を新しい画像に貼り付ける
        x_offset = 0
        y_offset = max_height * r
        # 画像を読み込み
        images_rows = [Image.open(temp_name) for temp_name in image_files[r]]
        # 配置を反転させる
        if args.direction == 'ltr':
            images_rows = images_rows[::-1]
        for x, image in enumerate(images_rows):
            new_image.paste(image, (x_offset, y_offset))
            x_offset += widths[x]

    # 新しい画像を保存する
    new_image.save(f"{folder_path}//{orig_file_name}-結.{args.ext}")

# ファイルを処理する
for file_path in args.files:
    folder_path, file_name = os.path.split(file_path)
    if folder_path == "":
        folder_path = os.getcwd()
    print('Processing file:', file_name)
    join_images(folder_path, file_name)

py_name = os.path.basename(__file__)
notification.notify(title = py_name, message="Done", timeout=5)
