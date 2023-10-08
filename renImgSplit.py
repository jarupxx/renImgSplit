import argparse
import os
import time
import multiprocessing
from PIL import Image
from plyer import notification

parser = argparse.ArgumentParser(description='Process multiple images')
parser.add_argument('files', nargs='+', help='Path to the input files')
parser.add_argument('--ext', help='Image format default: .png', default='.png')
parser.add_argument('--columns', type=int, default=2, help='Number of columns to split the image')
parser.add_argument('--rows', type=int, default=1, help='Number of rows to split the image')
parser.add_argument('--top', type=int, default=0, help='Number of pixels to crop from the top')
parser.add_argument('--bottom', type=int, default=0, help='Number of pixels to crop from the bottom')
parser.add_argument('--left', type=int, default=0, help='Number of pixels to crop from the left')
parser.add_argument('--right', type=int, default=0, help='Number of pixels to crop from the right')
parser.add_argument('-d', '--direction', help='Reading direction (ltr or rtl, default: ltr)', default='ltr')
args = parser.parse_args()

try:
    temp, args.ext = args.ext.split(".")
except ValueError:
    pass

if args.direction != 'rtl':
    args.direction = 'ltr'

def split_images(orig_folder_path, orig_file_name):
    folder_path = orig_folder_path
    file_name = orig_file_name
    file_name, file_ext = os.path.splitext(file_name)
    file_name = file_name.split("_")[0]
    os.chdir(folder_path)

    # 画像の読み込み
    image = Image.open(f"{folder_path}//{file_name}{file_ext}")

    # 画像をクロップする
    width, height = image.size
    crop_left = args.left
    crop_upper = args.top
    crop_right = width - args.right
    crop_lower = height - args.bottom
    cropped_image = image.crop((crop_left, crop_upper, crop_right, crop_lower))

    # 端数をクロップする
    width, height = cropped_image.size
    crop_width = width - (width % args.columns)
    crop_height = height - (height % args.rows)
    cropped_image = cropped_image.crop((0, 0, crop_width, crop_height))

    # 画像を分割する
    width, height = cropped_image.size
    tile_width = width // args.columns
    tile_height = height // args.rows
    for row in range(args.rows):
        for column in range(args.columns):
            left = column * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height
            tile = cropped_image.crop((left, upper, right, lower))

            # 分割した画像を保存する
            if (args.direction == 'rtl'):
                column_name = column
            else:
                column_name = args.columns - column - 1
            file_name, file_ext = os.path.splitext(orig_file_name)
            tile_file_name = f"{orig_folder_path}//{file_name}_{row+1}^{column_name+1}.{args.ext}"
            tile.save(tile_file_name)
    os.rename(f"{orig_folder_path}//{orig_file_name}", f"{orig_folder_path}//済-{orig_file_name}")

def process_file(file_paths):
    orig_folder_path, orig_file_name = os.path.split(file_paths)
    if orig_folder_path == "":
        orig_folder_path = os.getcwd()
    if orig_file_name.count("_") != 0 or orig_file_name.count("^") != 0:
        print('Skip: not allowed reserved words "_" "^".', orig_file_name)
    else:
        print('Processing file:', orig_file_name)
        split_images(orig_folder_path, orig_file_name)

if __name__ == "__main__":
    start_time = time.time()
    num_processes = multiprocessing.cpu_count()

    file_paths = args.files

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_file, file_paths)

    py_name = os.path.basename(__file__)
    print('Done.')
    # 処理が3秒超えたら通知をする
    end_time = time.time()
    processing_time = end_time - start_time
    if processing_time > 3:
        notification.notify(title=py_name, message="Done.", timeout=5)
