import cv2
import os
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

caps = []

if not os.path.exists(os.path.join(current_directory, "configurations.txt")):
    
    for video_path in video_files:

        video_cap = (cv2.VideoCapture(video_path))
        file_name = file_names[video_files.index(video_path)]

        if not video_cap.isOpened():
            raise RuntimeError(f"could not open video file {file_name}")
    
        ret, frame = video_cap.read()
        
        if ret:
            cv2.namedWindow(file_name, cv2.WINDOW_NORMAL)
            cv2.imshow(file_name, frame)
        
        video_cap.release()

    print("\npress esc to leave or s to save configuration")

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == 27: # esc
            break

        if key == ord("s"):
            
            with open(os.path.join(current_directory, "configurations.txt"), "w") as file:
                for window_name in file_names:
                    file.write(f"{window_name} - {cv2.getWindowImageRect(window_name)}\n")

            print("configuration saved. restart the program to use configuration.")
            break
else:
    
    config_info = {}

    with open(os.path.join(current_directory, "configurations.txt"), "r") as file:
        for line in file:
            temp_line = line
            window_name, numbers = temp_line.split("-")
            window_name = window_name[:-1]
            numbers = numbers.replace(" ", "").replace("(", "").replace(")", "").replace("\n", "")
            config_info[window_name] = numbers.split(",")

    print("configurations loaded - in order to reset them delete configurations.txt")
    print("close the program using esc")

    for x in video_files:
        video_cap = (cv2.VideoCapture(x))

        if not video_cap.isOpened():
            raise RuntimeError(f"video could not open video file {file_names[x]}")
        
        caps.append(video_cap)

    for i, f in enumerate(video_files):
        name = file_names[i]
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
        cv2.moveWindow(name, int(config_info[name][0]), int(config_info[name][1]))
        cv2.resizeWindow(name, int(config_info[name][2]), int(config_info[name][3]))

    while True:
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                resized_frame = cv2.resize(frame, (int(config_info[name][2]), int(config_info[name][3])))
                cv2.imshow(file_names[i], resized_frame)
            elif not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        if cv2.waitKey(27) & 0xFF == 27: # esc
            break

cv2.destroyAllWindows()