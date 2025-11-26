# Image-To-WebP-Converter-Python-Script

Python script to convert images to WebP format with best quality and compressed size.

## Supported Formats

- **JPG/JPEG** → WebP
- **PNG** → WebP
- **WEBP** → WebP (re-compresses)
- **HEIC** → WebP (iPhone photos)

Creates one clean `webp_output` folder inside your target folder.

---

## 1. Install Requirements

Open your terminal inside the project folder:

```bash
python3 -m venv venv
source venv/bin/activate
pip install pillow pillow-heif
```

This installs:
- **Pillow** – image processing library
- **pillow-heif** – HEIC/HEIF support for iPhone photos

---

## 2. Project Structure

```
image-tools/
   convert_webp.py
```

---

## 3. Run the Converter

```bash
python convert_webp.py /path/to/your/image-folder
```

Example:
```bash
python convert_webp.py ~/LillysSecret/Latest-Collection-November-2025/New-collection
```

---

## 4. What Happens When You Run It

- **Does NOT modify your original images** – originals remain untouched
- **Creates exactly ONE folder:**

```
your-folder/
   webp_output/
       image1.webp
       image2.webp
       ...
```

No recursion. No nested folders. No duplication.

- **Prints a log:**

```
🔄 Converting images inside: /Users/admin/.../New-collection
📁 Output folder: /Users/admin/.../New-collection/webp_output
✅ Converted: IMG_3358.HEIC → IMG_3358.webp
```

---

## 5. Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| HEIC failing / "cannot identify image file" | Install `pillow-heif` and use `register_heif_opener()` |
| Output folder created inside itself | Script uses absolute paths to create exactly one `webp_output` folder |
| "python: command not found" | Use `python3` on macOS |

---

## The Script

Copy & paste into `convert_webp.py`:

```python
import os
from PIL import Image
from pillow_heif import register_heif_opener

# Enable HEIC support
register_heif_opener()

# Allowed input formats
SUPPORTED_EXT = (".jpg", ".jpeg", ".png", ".heic", ".webp")

def convert_images(folder_path):
    folder_path = os.path.abspath(folder_path)

    # Create a single output folder inside the given folder
    output_folder = os.path.join(folder_path, "webp_output")
    os.makedirs(output_folder, exist_ok=True)

    print(f"🔄 Converting images inside: {folder_path}")
    print(f"📁 Output folder: {output_folder}")

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Skip unsupported formats
        if not filename.lower().endswith(SUPPORTED_EXT):
            continue

        # Output name
        output_name = os.path.splitext(filename)[0] + ".webp"
        output_path = os.path.join(output_folder, output_name)

        try:
            with Image.open(file_path) as img:
                img = img.convert("RGB")  # WebP needs RGB

                img.save(output_path, "WEBP", quality=90)

                print(f"✅ Converted: {filename} → {output_name}")

        except Exception as e:
            print(f"❌ Failed to convert {file_path}: {e}")

    print("\n🎉 Done! All possible images converted.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python convert_webp.py /path/to/folder")
    else:
        convert_images(sys.argv[1])
```
