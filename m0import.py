import os, sys
import shutil

import tqdm

drive_letter = "J"
flat = False


# with open(f"{drive_letter}:music.m3u8", mode="r", encoding="utf-8") as f:
with open(sys.argv[1], mode="r", encoding="utf-8") as f:
    m3u_mg = f.readlines()

# music.m3u8の置換 D:\My music\My music→A:を書く
replaced_text = [
    m3u_mg_line.replace("D:\\My music\My music\\", "A:\\") for m3u_mg_line in m3u_mg
]
with open(sys.argv[1], mode="w", encoding="utf-8") as f:
    f.writelines(replaced_text)
#with open(sys.argv[1], mode="r", encoding="utf-8") as f:  # ひどい
#    m3u_mg = f.readlines()

for j, i in enumerate(tqdm.tqdm(range(2, len(replaced_text), 2))):
    fn = replaced_text[i]
    if not os.path.exists("D:\\My music\My music\\" + fn[3:-1]) or len(fn) == 2:
        print(fn)
        continue

    if (
        flat
    ):  # なんかm0proでファイル一覧更新が固まるときに、ディレクトリ構造をフラットにするといいという言説があるらしいのでそういうモードを入れましたが、固まるときはどうやっても固まります
        ffn = fn.split("\\")[-1]
        fn_flat = f"{drive_letter}:\\{j}_{ffn[:-1]}"  # 問題あればディレクトリ名を全部_で繋げてfnにしてください

        if os.path.exists(fn_flat):
            # 移動済みファイルとファイル名前かぶりと区別する:jとiのdictでpickleを作る？ ちゃんとやらないと、プレイリストで途中の1曲を削除すると全部ズレてやり直しになって実にアレです
            continue
        print(fn_flat)
        shutil.copy("D:\\My music\My music\\" + fn[3:-1], fn_flat)
    else:
        dirname = os.path.dirname(f"{drive_letter}" + fn[1:-1])
        os.makedirs(dirname, exist_ok=True)
        if os.path.exists(f"{drive_letter}" + fn[1:-1]):
            continue
        shutil.copy("D:\\My music\My music\\" + fn[3:-1], f"{drive_letter}" + fn[1:-1])
