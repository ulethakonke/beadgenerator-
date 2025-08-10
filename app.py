import streamlit as st
from PIL import Image
import numpy as np
import math

# --- Configuration based on user's specifications ---
ARTWORK_WIDTH_CM = 80
ARTWORK_HEIGHT_CM = 100
BEAD_SIZE_MM = 3
BEADS_PER_PACK = 6300

# Calculate bead grid dimensions based on the 3mm bead size
BEAD_GRID_WIDTH = math.ceil((ARTWORK_WIDTH_CM * 10) / BEAD_SIZE_MM)
BEAD_GRID_HEIGHT = math.ceil((ARTWORK_HEIGHT_CM * 10) / BEAD_SIZE_MM)

# Define a simple grayscale palette for bead colors
# Each tuple is (R, G, B)
# We can adjust these to match your specific bead colors
BEAD_PALETTE = {
    "Pure White": (255, 255, 255),
    "Light Grey": (190, 190, 190),  # The target color for the background
    "Mid Grey": (120, 120, 120),
    "Dark Grey": (50, 50, 50),
    "Pure Black": (0, 0, 0),
}


def find_nearest_color(pixel, palette):
    """Finds the closest color in the palette to a given pixel."""
    pixel = np.array(pixel)
    palette_colors = np.array(list(palette.values()))
    distances = np.sqrt(np.sum((palette_colors - pixel)**2, axis=1))
    nearest_index = np.argmin(distances)
    return list(palette.keys())[nearest_index]


def process_image(image, palette):
    """
    Resizes the image and maps each pixel to the nearest bead color from the palette.
    Returns the new bead image and the count of each bead color.
    """
    # Resize the image to the bead grid dimensions
    resized_image = image.resize((BEAD_GRID_WIDTH, BEAD_GRID_HEIGHT), Image.Resampling.LANCZOS)
    
    # Convert image to grayscale for easier color mapping
    grayscale_image = resized_image.convert("L")
    
    bead_counts = {color: 0 for color in palette.keys()}
    bead_pixels = np.zeros((BEAD_GRID_HEIGHT, BEAD_GRID_WIDTH, 3), dtype=np.uint8)

    # Convert the palette from RGB tuples to a map for easy lookup based on intensity
    # Since we are using grayscale, the RGB values are all the same
    # We can sort the palette by brightness (Luminance)
    sorted_palette_keys = sorted(palette.keys(), key=lambda k: palette[k][0], reverse=True)
    sorted_palette_values = [palette[key] for key in sorted_palette_keys]
    
    # Iterate through each pixel of the resized image
    for y in range(BEAD_GRID_HEIGHT):
        for x in range(BEAD_GRID_WIDTH):
            original_pixel_value = grayscale_image.getpixel((x, y))
            
            # Find the nearest color in the sorted palette
            # This is a simple but effective way to map grayscale values
            mapped_color_key = find_nearest_color((original_pixel_value, original_pixel_value, original_pixel_value), palette)
            
            # Get the RGB value for the mapped color
            mapped_color_rgb = palette[mapped_color_key]
            
            # Update bead counts
            bead_counts[mapped_color_key] += 1
            
            # Store the mapped color for the new image
            bead_pixels[y, x] = mapped_color_rgb
    
    bead_image = Image.fromarray(bead_pixels, 'RGB')
    return bead_image, bead_counts


def calculate_packs(bead_count):
    """Calculates the number of packs needed for a given bead count."""
    return math.ceil(bead_count / BEADS_PER_PACK)


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Bead Art Generator",
        page_icon="🎨",
        layout="centered"
    )
    st.title("Pixel Bead Art Generator 🎨")
    st.write("This app will convert your image into a bead art pattern and provide a shopping list based on your specifications.")
    st.markdown("---")

    st.header("Image and Project Details")
    st.write(f"**Artwork Dimensions:** {ARTWORK_WIDTH_CM}cm x {ARTWORK_HEIGHT_CM}cm")
    st.write(f"**Bead Size:** {BEAD_SIZE_MM}mm")
    st.write(f"**Bead Grid:** {BEAD_GRID_WIDTH} beads wide x {BEAD_GRID_HEIGHT} beads tall")
    st.write(f"**Packs have:** {BEADS_PER_PACK} beads")
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            st.success("Image uploaded successfully!")
            
            st.subheader("Original Image")
            st.image(image, use_column_width=True)

            st.markdown("---")
            st.subheader("Bead Art Preview")
            
            # Process the image to create the bead art pattern
            bead_image, bead_counts = process_image(image, BEAD_PALETTE)
            
            # Display the bead art image
            st.image(bead_image, caption="Bead Art Pattern", use_column_width=True)

            st.markdown("---")
            st.subheader("Bead Shopping List")
            
            total_beads = sum(bead_counts.values())
            st.write(f"**Total Beads Needed:** {total_beads:,} beads")
            st.write(f"**Total Packs Needed:** {calculate_packs(total_beads)} packs")
            
            st.write("Here is the breakdown by color:")
            
            # Display a table with bead counts and packs for each color
            for color, count in bead_counts.items():
                packs = calculate_packs(count)
                st.write(f"- **{color}:** {count:,} beads ({packs} packs)")

            # Specifically address the user's request for light grey background beads
            light_grey_count = bead_counts.get("Light Grey", 0)
            light_grey_packs = calculate_packs(light_grey_count)
            st.info(f"**Specifically for the background (and any other light grey areas), you will need {light_grey_count:,} beads, which is {light_grey_packs} packs of light grey.**")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
