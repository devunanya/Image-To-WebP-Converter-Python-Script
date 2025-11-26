#!/usr/bin/env python3
import os
import sys
import subprocess
from PIL import Image

# Open images, HEIC will be converted via sips
def open_image(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".heic":
        # Create temporary PNG file
        temp_png = file_path + ".png"
        subprocess.run(["sips", "-s", "format", "png", file_path, "--out", temp_png], check=True)
        img = Image.open(temp_png)
        return img, temp_png  # return temp path to delete later
    else:
        img = Image.open(file_path)
        return img, None

def convert_to_webp(input_path, quality=85):
    if not os.path.exists(input_path):
        print(f"Error: '{input_path}' not found.")
        return

    for root, dirs, files in os.walk(input_path):
        # Skip any webp_output folders to avoid nested output
        if "webp_output" in dirs:
            dirs.remove("webp_output")

        output_folder = os.path.join(root, "webp_output")
        os.makedirs(output_folder, exist_ok=True)

        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.heic')):
                input_file = os.path.join(root, filename)
                output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.webp')

                if os.path.exists(output_file):
                    print(f"⏭ Skipping (already converted): {filename}")
                    continue

                try:
                    img, temp_png = open_image(input_file)
                    with img.convert("RGB") as img_rgb:
                        img_rgb.save(output_file, 'webp', quality=quality)
                    print(f"✅ Converted: {input_file} → {output_file}")
                    img.close()

                    # Remove original file after successful conversion
                    os.remove(input_file)

                    # Remove temporary PNG if it was created
                    if temp_png:
                        os.remove(temp_png)
                except Exception as e:
                    print(f"❌ Failed to convert {input_file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_webp.py <input_path> [quality]")
        sys.exit(1)

    input_path = sys.argv[1]
    quality = int(sys.argv[2]) if len(sys.argv) > 2 else 85

    convert_to_webp(input_path, quality)
