# ... (Keep all your Journal and Audio code the same above this line!) ...

# ==========================================
# ROOM 2: THE MARKETPLACE
# ==========================================
elif page == "The Marketplace 🛍️":
    st.title("The Marketplace")
    st.write("Curated physical items to ground your space and support your mindfulness practice.")
    st.write("---")

    # Helper function to display products safely
    def display_product(label, img_file, desc, btn_key):
        st.markdown(f"#### {label}")
        if os.path.exists(img_file):
            st.image(img_file, use_container_width=True)
        else:
            st.warning(f"📸 Image '{img_file}' missing in vault.")
        st.write(desc)
        st.button(f"View {label}", key=btn_key)

    # ROW 1
    c1, c2, c3 = st.columns(3)
    with c1:
        display_product("Natural Stones", "stones.jpg", "Unpolished, naturally sourced stones for grounding.", "s")
    with c2:
        display_product("Crafted Beads", "beads.jpg", "Tactile wooden beads for rhythmic breathing.", "b")
    with c3:
        display_product("Geometric Yantras", "yantras.jpg", "Metalwork focal points for concentration.", "y")
    
    st.write("---")

    # ROW 2
    c4, c5, c6 = st.columns(3)
    with c4:
        display_product("Joyful Sculptures", "buddha.jpg", "Traditional figures representing contentment.", "sc")
    with c5:
        display_product("Spatial Decor", "vaastu.jpg", "Pieces designed for environmental balance.", "v")
    with c6:
        display_product("Heritage Art", "art.jpg", "Iconography offering a serene focal point.", "a")
