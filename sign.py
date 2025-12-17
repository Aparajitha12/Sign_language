
import os
import shutil

# Root ASL dataset folder 
SRC_DATASET = "ASL dataset/asl_alphabet_train/asl_alphabet_train"
DEST_FOLDER = "sign_letters"

SPECIAL_CLASSES = ["space", "del", "nothing"]

# Ensure destination folder exists
if not os.path.exists(DEST_FOLDER):
    os.makedirs(DEST_FOLDER)

for label in SPECIAL_CLASSES:
    label_folder = os.path.join(SRC_DATASET, label)

    if not os.path.exists(label_folder):
        print(f"Folder not found: {label_folder}")
        continue

    image_list = sorted(os.listdir(label_folder))
    if not image_list:
        print(f"No images found in {label_folder}")
        continue

    # Pick the first image from the folder
    src_img = os.path.join(label_folder, image_list[0])
    dest_img = os.path.join(DEST_FOLDER, f"{label}.jpg")

    shutil.copy(src_img, dest_img)
    print(f"Copied: {label}.jpg → {DEST_FOLDER}")
