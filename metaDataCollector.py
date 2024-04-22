from PIL import Image, ExifTags
import os

folder = ""
timestamps = []

for filename in os.listdir(folder):
    if filename.lower().endswith((".jpg")):
        path = os.path.join(folder, filename)
        try:
            image = Image.open(path)
            exif = {ExifTags.TAGS[k]: v for k, v in image._getexif().items() if k in ExifTags.TAGS}
            datetime = exif.get("DateTimeDigitized", "Unknown")
            timestamps.append(f"{datetime}")
        except (AttributeError, KeyError):
            pass

output_file = "timestamps.txt"
with open(output_file, "w") as f:
    for timestamp in timestamps:
        f.write(timestamp + "\n")