import streamlit as st
import item_genV2
import random
import string


def app():
    # Global Variables
    rarities = ["Common", "Uncommon", "Rare", "Epic", "Legendary",
                "Special", "Supreme", "Divine", "Mythic", "Custom"]
    rarity_values = ["&l&fCOMMON", "&l&aUNCOMMON", "&l&9RARE", "&l&5EPIC",
                     "&l&6LEGENDARY", "&l&cSPECIAL", "&l&4SUPREME", "&l&bDIVINE", "&l&dMYTHIC"]
    custom_rarity = ""
    LINE_LIMIT = 150
    LINE_SIZE_LIMIT = 100
    letters = string.ascii_letters

    # Initial Setup
    st.title("🎨  Item Generation Test")
    st.write(
        "This app can generate a Hypixel Skyblock Item in just a few steps!"
    )
    error_location = st.empty()
    left, right = st.columns(2)
    right.write("Item Generated:")
    imageLocation = right.empty()
    imageLocation.image("default.png")

    # Item Generation Form
    left.write("Fill Item Details:")

    name = left.text_input("Item Name")
    rarity = left.selectbox(
        "Item Rarity",
        rarities,
        index=0
    )
    custom_rarity_location = left.empty()

    lore_lines = left.text_area(
        "Lore Lines (Max " + str(LINE_LIMIT) + " Lines)")

    if rarity or name or lore_lines:
        split_lines = lore_lines.splitlines()
        if rarity == "Custom":
            custom_rarity = custom_rarity_location.text_input(
                "Custom Item Rarity")
            rarity = custom_rarity
        else:
            rarity = rarity_values[rarities.index(rarity)]
        if len(split_lines) > LINE_LIMIT:
            error_location.error("You have too many lore lines. Max: "
                                 + str(LINE_LIMIT) + "/Current: " + str(len(split_lines)))
        elif any([line_length for line_length in split_lines if len(line_length) > LINE_SIZE_LIMIT]):
            error_location.error(
                "You have a line that is too long! Max: " + str(LINE_SIZE_LIMIT))
        elif len(name) > LINE_SIZE_LIMIT:
            error_location.error(
                "You have a title that is too long! Max: " + str(LINE_SIZE_LIMIT))
        elif len(rarity) > LINE_SIZE_LIMIT:
            error_location.error(
                "You have a custom rarity that is too long! Max: " + str(LINE_SIZE_LIMIT))
        else:
            file = item_genV2.render([name] + split_lines + [rarity])

            if name == "":
                imageLocation.image("default.png")
            else:
                imageLocation.image(file)
            right.download_button(
                "⬇ Download Image",
                data=file,
                file_name=''.join(random.choice(letters)
                                  for i in range(10)) + ".png",
                mime="application/octet-stream",
            )
