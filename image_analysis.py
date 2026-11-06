
import cv2
import numpy as np


def analyze_images(before, after):

    # Read uploaded images
    img1 = cv2.imdecode(
        np.frombuffer(before.getvalue(), np.uint8),
        cv2.IMREAD_COLOR
    )

    img2 = cv2.imdecode(
        np.frombuffer(after.getvalue(), np.uint8),
        cv2.IMREAD_COLOR
    )

    # Validate images
    if img1 is None or img2 is None:
        raise ValueError("Unable to read uploaded images.")

    # Resize after image to match before image
    img2 = cv2.resize(
        img2,
        (img1.shape[1], img1.shape[0])
    )

    # Convert images to grayscale
    gray1 = cv2.cvtColor(
        img1,
        cv2.COLOR_BGR2GRAY
    )

    gray2 = cv2.cvtColor(
        img2,
        cv2.COLOR_BGR2GRAY
    )

    # Apply Gaussian blur
    gray1 = cv2.GaussianBlur(
        gray1, (5, 5), 0
    )

    gray2 = cv2.GaussianBlur(
        gray2, (5, 5), 0
    )

    # Calculate image difference
    difference = cv2.absdiff(
        gray1,
        gray2
    )

    # Apply threshold
    _, mask = cv2.threshold(
        difference,
        30,
        255,
        cv2.THRESH_BINARY
    )

    # Remove small noise
    kernel = np.ones((3, 3), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    # Calculate visual change percentage
    changed_pixels = np.count_nonzero(mask)

    total_pixels = mask.size

    change_percentage = (
        changed_pixels / total_pixels
    ) * 100

    # Highlight changed regions
    highlighted = img2.copy()

    highlighted[mask > 0] = [0, 0, 255]

    # Blend original and highlighted image
    overlay = cv2.addWeighted(
        img2,
        0.65,
        highlighted,
        0.35,
        0
    )

    # Convert BGR to RGB for Streamlit
    overlay = cv2.cvtColor(
        overlay,
        cv2.COLOR_BGR2RGB
    )

    original = cv2.cvtColor(
        img2,
        cv2.COLOR_BGR2RGB
    )

    return change_percentage, original, overlay, mask
