import argparse
import tempfile
import zipfile
from pathlib import Path

import img2pdf
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description="画像zipをpdfに変換する。")
    parser.add_argument('-s', '--source', type=str, required=True, help='読み込むzipファイルのパス')
    parser.add_argument('-d', '--destination', type=str, required=True, help='出力するpdfファイルのパス')
    args = parser.parse_args()

    path_zip = Path(args.source)
    path_pdf = Path(args.destination)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # zipファイルを一時フォルダに展開する
        with zipfile.ZipFile(path_zip, "r") as zip_f:
            print(f"extract: {path_zip=}")
            zip_f.extractall(tmp_dir)

        # pngファイルをjpgファイルに変換する
        path_dir = Path(tmp_dir)
        path_images = sorted(list(path_dir.glob("*.png")))

        for path_image in path_images:
            print(f"convert: {path_image=}")
            img = Image.open(path_image)
            path_image_jpg = path_image.with_suffix(".jpg")
            img.convert("RGB").save(path_image_jpg, "JPEG")

        # pdfファイルを作成する
        path_images = sorted(list(path_dir.glob("*.jpg")))

        with open(path_pdf, "wb") as f:
            print(f"save pdf: {path_pdf=}")
            f.write(img2pdf.convert(path_images))


if __name__ == "__main__":
    main()
