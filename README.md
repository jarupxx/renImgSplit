# renImgSplit
Install dependencies with ```pip install PIL plyer```
## 概要
ファイルをまとめて分割します.

上下左右のサイズを指定してトリミングできます.

引数で渡したファイルを全てトリミングしてから分割して保存します.

同名のファイルは上書きされます.
## 使用方法

```renImgSplit.py "C:\path\001.jpg"```

'--ext' 保存形式 初期値 = .bmp

'--columns' 列、横方向の分割数 初期値 = 2

'--rows' 行、縦方向の分割数 初期値 = 1

'--top' 上部のクロップサイズ 初期値 = 0

'--bottom' 下部のクロップサイズ 初期値 = 0

'--left' 左側のクロップサイズ 初期値 = 0

'--right' 右側のクロップサイズ 初期値 = 0

'-d', '--direction' 画像の配置、右開きの本なら ltr を指定します 初期値 = ltr

左右100pxクロップ、3分割してpngで保存するなら

```renImgSplit.py --ext .png --columns 3 --left 100 --right 100 "C:\path\001.jpg"```

## 注意事項

同じ解像度で分割できない場合は端が削られます.

ファイル名に"_" "^"は使用できません.
## Summary

This program split images.

Trim images specifying the top, bottom, left, and right.

This program trims, split, and saves them.

Output file is replaced with the new one.
## Usage

```renImgSplit.py "C:\path\001.jpg"```

'--ext' 'Image format default: .bmp'

'--columns' 'Number of columns to split the image'

'--rows' 'Number of rows to split the image'

'--top' 'Number of pixels to crop from the top'

'--bottom' 'Number of pixels to crop from the bottom'

'--left' 'Number of pixels to crop from the left'

'--right' 'Number of pixels to crop from the right'

'-d', '--direction' Reading direction (ltr or rtl)

If you want to crop 100px left and right, split it into 3 parts and save format as a png.

```renImgSplit.py --ext .png --columns 3 --left 100 --right 100 "C:\path\001.jpg"```

## Notes
This program cannot be splitted with the same resolution, the edges will be clipped.

Do not use "_" "^" by filename.
# renImgMerge
renImgSplit で分割した画像をまとめて結合します.

全て同じ解像度でファイル名が揃っていることを想定しています.

## 使用方法

```renImgMerge.py "C:\path\001_1^2.bmp"```

'--ext' 保存形式 初期値 = .bmp

'-d', '--direction' 画像の配置、右開きの本なら ltr を指定します 初期値 = ltr

## 注意事項

renImgMergeは十分なテストをされておりません.

## Summary

This program Merge the images split by renImgSplit.

It is assumed that all the images are of the same resolution.
## Usage

```renImgMerge.py "C:\path\001_1^2.bmp"```

'--ext' 'Image format default: .bmp'

'-d', '--direction' Reading direction (ltr or rtl)

## Notes
renImgMerge has not been thoroughly tested.
