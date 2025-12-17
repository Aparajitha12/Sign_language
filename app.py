import streamlit as st
import os
import cv2
from PIL import Image
import imageio

# CONFIG
SIGN_LETTER_DIR = "sign_letters"

# Valid labels
valid_labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["DEL", "NOTHING", "SPACE"]
file_map = {ch: f"{ch.lower()}.jpg" for ch in valid_labels}

# STREAMLIT SETUP
st.set_page_config(page_title="ASL Translator", layout="wide")
st.title("ASL Sign Language Translator")
st.caption("Convert text into ASL sign images")

# INPUT
user_input = st.text_input(
    "Enter text (A-Z, del, space, nothing):",
    value="I AM BALA"
).upper()

# TOKENIZATION (SPACE SAFE)
tokens = []
for char in user_input:
    if char == " ":
        tokens.append("SPACE")
    elif char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        tokens.append(char)
    else:
        continue 

# FULL DISPLAY
if tokens:
    st.subheader("Full Display")
    cols = st.columns(len(tokens))

    for i, token in enumerate(tokens):
        with cols[i]:
            label = token
            img_path = os.path.join(SIGN_LETTER_DIR, file_map[label])

            if os.path.exists(img_path):
                img = cv2.imread(img_path)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                display_label = "␣" if label == "SPACE" else label
                st.image(
                    Image.fromarray(img_rgb),
                    caption=display_label,
                    use_container_width=True
                )
            else:
                st.error(f"Missing image: {file_map[label]}")

# GIF GENERATION
st.subheader("Animated ASL GIF")

def create_gif(tokens, output_path="asl_animation.gif", duration_ms=800):
    frames = []

    for label in tokens:
        img_path = os.path.join(SIGN_LETTER_DIR, file_map[label])
        if os.path.exists(img_path):
            img = Image.open(img_path).convert("RGB").resize((300, 300))
            frames.append(img)

    if frames:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=0
        )
        return output_path
    return None

gif_path = create_gif(tokens)

if gif_path and os.path.exists(gif_path):
    st.image(gif_path, caption="ASL Animation", use_container_width=True)
else:
    st.warning("No images available to generate GIF.")
