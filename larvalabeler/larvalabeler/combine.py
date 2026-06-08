import os
import random
import shutil

import yaml


def create_directory_structure(base_path):
    """
    Create the directory structure for the combined dataset.
    """
    dirs = [
        os.path.join(base_path, "images", "train"),
        os.path.join(base_path, "images", "val"),
        os.path.join(base_path, "images", "test"),
        os.path.join(base_path, "labels", "train"),
        os.path.join(base_path, "labels", "val"),
        os.path.join(base_path, "labels", "test"),
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


def copy_and_rename_files(src_dir, dst_img_dir, dst_label_dir, img_counter):
    """
    Copy and rename images and labels from the source directory to the destination directory.
    """
    for file_name in os.listdir(src_dir):
        src_path = os.path.join(src_dir, file_name)
        if file_name.endswith((".jpg", ".png")):
            new_file_name = f"frame_{img_counter:06}.jpg"
            dst_path = os.path.join(dst_img_dir, new_file_name)
            shutil.copy(src_path, dst_path)
            label_src = os.path.splitext(src_path)[0] + ".txt"
            if os.path.exists(label_src):
                new_label_name = f"frame_{img_counter:06}.txt"
                dst_label_path = os.path.join(dst_label_dir, new_label_name)
                shutil.copy(label_src, dst_label_path)
            img_counter += 1
    return img_counter


def split_dataset(img_dir, label_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """
    Split the dataset into train, validation, and test sets.
    """
    images = [f for f in os.listdir(img_dir) if f.endswith((".jpg", ".png"))]
    random.shuffle(images)

    total_images = len(images)
    train_end = int(total_images * train_ratio)
    val_end = train_end + int(total_images * val_ratio)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    return train_images, val_images, test_images


def move_files(images, src_img_dir, src_label_dir, dst_img_dir, dst_label_dir):
    """
    Move image and label files to their respective directories (train/val/test).
    """
    for img_name in images:
        img_src_path = os.path.join(src_img_dir, img_name)
        label_src_path = os.path.join(
            src_label_dir, os.path.splitext(img_name)[0] + ".txt"
        )

        img_dst_path = os.path.join(dst_img_dir, img_name)
        label_dst_path = os.path.join(
            dst_label_dir, os.path.splitext(img_name)[0] + ".txt"
        )

        shutil.move(img_src_path, img_dst_path)
        if os.path.exists(label_src_path):
            shutil.move(label_src_path, label_dst_path)


def create_data_yaml(base_path, num_train, num_val, num_test):
    """
    Create the data.yaml file for the combined dataset.
    """
    data = {
        "path": base_path,
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": {0: "zebrafish"},
    }

    data_yaml_path = os.path.join(base_path, "data.yaml")
    with open(data_yaml_path, "w") as yaml_file:
        yaml.dump(data, yaml_file)

    # Add number of images in each subset as comments
    with open(data_yaml_path, "r+") as yaml_file:
        content = yaml_file.read()
        yaml_file.seek(0, 0)
        yaml_file.write(
            f"# Number of images in each subset\n# test: {num_test}\n# train: {num_train}\n# val: {num_val}\n\n{content}"
        )

    print(f"Created data.yaml at {data_yaml_path}")


def combine_projects(projects_dir, combined_dir):
    """
    Combine the save directories from multiple projects into one dataset.
    """
    create_directory_structure(combined_dir)

    img_counter = 0
    save_img_dir = os.path.join(combined_dir, "images")
    save_label_dir = os.path.join(combined_dir, "labels")

    for project in os.listdir(projects_dir):
        project_save_dir = os.path.join(projects_dir, project, "save")
        if os.path.exists(project_save_dir):
            img_counter = copy_and_rename_files(
                project_save_dir, save_img_dir, save_label_dir, img_counter
            )

    # Split the combined dataset into train, val, and test sets
    train_images, val_images, test_images = split_dataset(save_img_dir, save_label_dir)

    # Move files into their respective directories
    move_files(
        train_images,
        save_img_dir,
        save_label_dir,
        os.path.join(combined_dir, "images", "train"),
        os.path.join(combined_dir, "labels", "train"),
    )
    move_files(
        val_images,
        save_img_dir,
        save_label_dir,
        os.path.join(combined_dir, "images", "val"),
        os.path.join(combined_dir, "labels", "val"),
    )
    move_files(
        test_images,
        save_img_dir,
        save_label_dir,
        os.path.join(combined_dir, "images", "test"),
        os.path.join(combined_dir, "labels", "test"),
    )

    # Create the data.yaml file
    create_data_yaml(combined_dir, len(train_images), len(val_images), len(test_images))


if __name__ == "__main__":
    projects_directory = "projects"
    combined_dataset_directory = "zebrafish_larvae_auto_segmentation"

    combine_projects(projects_directory, combined_dataset_directory)
    print("Finished combining projects.")
