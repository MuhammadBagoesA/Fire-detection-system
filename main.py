import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import os
import tempfile
import time

# MODEL

MODEL_WEIGHTS = "weight/best.pt"
model = YOLO(MODEL_WEIGHTS)

SAMPLE_IMAGE_DIR = "sample images"
SAMPLE_VIDEO_DIR = "sample videos"

class_names = ["smoke", "fire"]

# SIDEBAR

st.sidebar.header("Pengaturan Deteksi")

conf_threshold = st.sidebar.slider(
    "Confidence Threshold",
    0.0,
    1.0,
    0.1,
    0.01
)

# TITLE

st.title("Fire & Smoke Detection")
st.write("by : Muhammad Bagoes Anargiansyah")

st.write(
"""
Upload **gambar atau video** untuk mendeteksi api dan asap.\n
Model dapat diimplementasikan pada foto dan video.\n
Implementasi lebih lanjut dapat dilakukan pada streaming video secara real-time menggunakan webcam atau CCTV serta penambahan fitur alarm.
"""
)

st.divider()

# DISPLAY AREA

col1, col2 = st.columns([3,1])

with col1:
    image_placeholder = st.empty()

with col2:
    alert_placeholder = st.empty()

image_placeholder.info("Belum ada media yang dianalisis")

# FUNCTION DETECTION

def detect_classes(results):

    fire_detected = False
    smoke_detected = False

    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0:

        classes = boxes.cls.cpu().numpy().astype(int)

        for cls in classes:

            if cls < len(class_names):

                if class_names[cls] == "fire":
                    fire_detected = True

                if class_names[cls] == "smoke":
                    smoke_detected = True

    return fire_detected, smoke_detected


def show_alert(fire_detected, smoke_detected):

    if fire_detected and smoke_detected:
        alert_placeholder.error("🔥🔥 FIRE AND SMOKE DETECTED!")

    elif fire_detected:
        alert_placeholder.error("🔥 FIRE DETECTED!")

    elif smoke_detected:
        alert_placeholder.warning("💨 SMOKE DETECTED!")

    else:
        alert_placeholder.success("✅ No Fire / Smoke detected")


# IMAGE DETECTION

def run_image(img):

    results = model(img, conf=conf_threshold)

    annotated = results[0].plot()
    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    fire_detected, smoke_detected = detect_classes(results)

    image_placeholder.image(
        annotated,
        caption="Detection Result",
        width="stretch"
    )

    show_alert(fire_detected, smoke_detected)


# VIDEO DETECTION

def run_video(video_path):

    cap = cv2.VideoCapture(video_path)

    image_placeholder.empty()

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame, conf=conf_threshold)

        annotated = results[0].plot()
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        image_placeholder.image(
            annotated,
            caption="Video Detection",
            width="stretch"
        )

        fire_detected, smoke_detected = detect_classes(results)

        show_alert(fire_detected, smoke_detected)

        time.sleep(0.03)

    cap.release()


# UPLOAD MEDIA

st.subheader("Upload Media")

uploaded_file = st.file_uploader(
    "Upload gambar atau video...",
    type=["jpg","jpeg","png","mp4","mov","avi"]
)

if uploaded_file is not None:

    file_type = uploaded_file.type

    if "image" in file_type:

        image = Image.open(uploaded_file).convert("RGB")

        img = np.array(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        run_image(img)

    elif "video" in file_type:

        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        run_video(tfile.name)


# SAMPLE IMAGES

st.subheader("Contoh Gambar")
st.write("atau gunakan gambar serta video contoh:")

sample_images = []

if os.path.exists(SAMPLE_IMAGE_DIR):
    for file in os.listdir(SAMPLE_IMAGE_DIR):
        if file.endswith(("jpg","jpeg","png")):
            sample_images.append(os.path.join(SAMPLE_IMAGE_DIR, file))

cols = st.columns(3)

for i, img_path in enumerate(sample_images):

    with cols[i % 3]:

        image = Image.open(img_path)

        st.image(
            image,
            caption=os.path.basename(img_path),
            width="stretch"
        )

        if st.button("Gunakan gambar ini", key=img_path):

            img = np.array(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            run_image(img)


# SAMPLE VIDEOS

st.subheader("Contoh Video")

sample_videos = []

if os.path.exists(SAMPLE_VIDEO_DIR):
    for file in os.listdir(SAMPLE_VIDEO_DIR):
        if file.endswith(("mp4","mov","avi")):
            sample_videos.append(os.path.join(SAMPLE_VIDEO_DIR, file))

cols = st.columns(2)

for i, vid_path in enumerate(sample_videos):

    with cols[i % 2]:

        st.video(vid_path)

        if st.button("Gunakan video ini", key=vid_path):

            run_video(vid_path)