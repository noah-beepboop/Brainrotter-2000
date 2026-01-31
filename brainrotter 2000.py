import cv2
import os
import math
from screeninfo import get_monitors

current_directory = os.getcwd()
video_extensions = (".mp4", ".avi", ".mov", "mkv")
video_files = []
file_names = []

for path, nothin, files in os.walk(current_directory):
    for file in files:
        if file.lower().endswith(video_extensions):
            video_files.append(os.path.join(path, file))
            file_names.append(os.path.basename(video_files[video_files.index(os.path.join(path, file))]))

if not video_files:
    raise RuntimeError("no video files found")

for m in get_monitors():
    if m.is_primary:
        screen_width = m.width
        screen_height = m.height

percent_screen = 0.5

# X is the border thickness, W is the width, H is the height
# (W - 2x)(H - 2x) = percent_screen * W * H
# -4x^2 - 2xW - 2xH + WH

left_side = percent_screen * screen_width * screen_height

a = -4
b = -2 * screen_width + -2 * screen_height
c = (screen_width * screen_height) - left_side

solution = round((-b - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)) # Gives positive solution

perimeter = 2 * (screen_width - solution) + 2 * (screen_height - solution)

image_pixel_length = perimeter / len(video_files)

caps = []
heights = []
widths = []

for x in video_files:
    video_cap = (cv2.VideoCapture(x))

    widths.append(int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    heights.append(int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    if not video_cap.isOpened():
        raise RuntimeError(f"video could not open video file {file_names[x]}")
    
    caps.append(video_cap)

new_heights = []
new_widths = []

for x, height in enumerate(heights):
    if heights[x] > widths[x]:
        ratio = image_pixel_length / heights[x]
        new_heights.append(round(heights[x] * ratio))
        new_widths.append(round(widths[x] * ratio))
    else:
        ratio = image_pixel_length / widths[x]
        new_heights.append(round(heights[x] * ratio))
        new_widths.append(round(widths[x] * ratio))

for i, f in enumerate(video_files):
    cv2.namedWindow(file_names[i], cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
    cv2.resizeWindow(file_names[i], new_widths[i], new_heights[i])

while True:
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if ret:
            cv2.imshow(file_names[i], frame)
    
    if cv2.waitKey(27) & 0xFF == 27:
        break