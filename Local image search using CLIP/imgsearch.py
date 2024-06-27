import streamlit as st
import torch
import clip
from PIL import Image
import os

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Define image directory and paths
image_dir = "images"
image_paths = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(('.jpg', '.png'))]
images = {os.path.basename(image_path): Image.open(image_path) for image_path in image_paths}

# Function to preprocess images
def preprocess_images(images):
    return {path: preprocess(img).unsqueeze(0).to(device) for path, img in images.items()}

# Function to encode text
def encode_text(text):
    with torch.no_grad():
        text_inputs = clip.tokenize([text]).to(device)
        text_features = model.encode_text(text_inputs)
    return text_features

# Function to compute similarity scores
def compute_similarity(image_features, text_features):
    with torch.no_grad():
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = image_features @ text_features.T
    return similarity.squeeze(1)

# Streamlit UI
def main():
    st.title("Image Search from local memory")

    # Checkbox to show/hide gallery
    show_gallery = st.checkbox("Show Gallery", key="show_gallery")

    # Gallery layout to display images (hidden by default)
    if show_gallery:
        st.header("Gallery")
        col1, col2, col3 = st.columns(3)
        for idx, (path, img) in enumerate(images.items()):
            if idx % 3 == 0:
                col1.image(img, caption=path, use_column_width=True)
            elif idx % 3 == 1:
                col2.image(img, caption=path, use_column_width=True)
            else:
                col3.image(img, caption=path, use_column_width=True)

    # Input layout to get text from user
    st.header("Search Images by Text")
    text_input = st.text_input("Enter text to search images:", "")
    if st.button("Search"):
        st.subheader(f"Images matching text '{text_input}':")
        
        # Preprocess images and encode text
        preprocessed_images = preprocess_images(images)
        text_features = encode_text(text_input)
        
        # Compute similarity for each image
        similarities = {}
        for path, img_tensor in preprocessed_images.items():
            image_features = model.encode_image(img_tensor)
            similarity = compute_similarity(image_features, text_features)
            similarities[path] = similarity.item()
        
        # Sort images by similarity score (descending)
        sorted_images = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        # Display matched images
        for path, similarity_score in sorted_images:
            if similarity_score > 0.2:  # Adjust threshold as needed
                st.image(images[path], caption=f"Similarity: {similarity_score:.2f}", width=300)

# Run Streamlit app
if __name__ == "__main__":
    main()
