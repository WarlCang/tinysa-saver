from PIL import Image, ExifTags
import os
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

folder = r"C:\Users\Jiahao Wang\Desktop\tinysa-saver\pics"
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

timestamps = []

def parse_timestamp(timestamp_str):
    return dt.datetime.strptime(timestamp_str, "%Y:%m:%d %H:%M:%S")

with open("timestamps.txt", "r") as file:
    timestamps = [parse_timestamp(line.strip()) for line in file]

peak_data = []
with open("peak_data.csv", "r") as file:
    for line in file:
        parts = line.strip().split(',')
        timestamp = parse_timestamp(parts[0])  # Join the first two elements for timestamp
        attribute = parts[2]  # This is the dB value
        peak_data.append((timestamp, attribute))

# Compare timestamps and store attributes if they are within one second
matched_attributes = []
for peak_timestamp, attribute in peak_data:
    for i, ts in enumerate(timestamps):
        if abs((peak_timestamp - ts).total_seconds()) < 1:
            print(attribute)
            matched_attributes.append(attribute)
            del timestamps[i]  # Remove the matched timestamp to prevent re-matching
            break  # Stop checking once a match is found to avoid multiple matches

angles_radians =[]
dB_values = matched_attributes
for i in range(36):
    angles_radians.append(np.radians(10*i))
    dB_values.append(100)

# Create the polar plot
plt.figure()
ax = plt.subplot(111, polar=True)
ax.plot(angles_radians, dB_values, marker='o')

# Set the angle where 0 degrees is at the top and angles increase clockwise
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

# Set the labels for the angles
ax.set_xticks(np.radians(range(0, 360, 10)))  # Set ticks every 10 degrees
ax.set_xticklabels(range(0, 360, 10))  # Set labels to be in degrees

# Add title and dB level gridlines
ax.set_title('50m_10MHz', va='bottom')
ax.grid(True)

# Show the plot
plt.show()