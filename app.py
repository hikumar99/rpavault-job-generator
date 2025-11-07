# 🤖 RPAVault Smart Job Poster Generator (Keyword Detection + Dynamic Themes)
## 🎯 Answer
This is your **final, smart version** of the RPAVault Job Post Generator.  
It now **automatically detects keywords** like “Remote”, “Internship”, “Hiring”, etc.,  
adds relevant **icons + titles**, and uses **random color themes + gradients + logo branding**.  

Perfect for **daily automation-ready visuals** across Instagram, YouTube Shorts & LinkedIn.

---

# 💻 Full Streamlit Code  
**File:** `app.py`
```python
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random, io, textwrap, os, re

# --- CONFIG ---
st.set_page_config(page_title="RPAVault Smart Job Poster Generator", layout="centered")

# --- HEADER ---
st.markdown("""
# 🚀 RPAVault Smart Job Poster Generator  
Automatically generate **branded, theme-based job posters**  
with keyword detection for 🎓 Internship, 🌍 Remote, and 💼 Hiring roles.
""")

# --- SIDEBAR SETUP ---
st.sidebar.header("⚙️ Setup Area")

bg_folder = "backgrounds"
os.makedirs(bg_folder, exist_ok=True)

uploaded_logo = st.sidebar.file_uploader("Upload RPAVault Logo (PNG, transparent bg)", type=["png"])
uploaded_bg = st.sidebar.file_uploader("Upload Background Image", type=["jpg", "jpeg", "png"])

if uploaded_bg:
    bg_path = os.path.join(bg_folder, uploaded_bg.name)
    with open(bg_path, "wb") as f:
        f.write(uploaded_bg.read())
    st.sidebar.success(f"✅ Added {uploaded_bg.name} to backgrounds")

# --- TEXT INPUT ---
job_text = st.text_area("📋 Paste Job Description", height=250, placeholder="Paste job content here...")

# --- COLOR THEMES ---
themes = [
    {"name": "Sunset Red", "header": (255, 69, 0, 255), "text": "white"},
    {"name": "Ocean Blue", "header": (30, 144, 255, 255), "text": "white"},
    {"name": "Tech Purple", "header": (138, 43, 226, 255), "text": "white"},
    {"name": "Forest Green", "header": (0, 128, 0, 255), "text": "white"},
    {"name": "Golden Glow", "header": (255, 191, 0, 255), "text": "black"},
    {"name": "Crimson Bold", "header": (220, 20, 60, 255), "text": "white"},
]

# --- KEYWORD MAPPING ---
keyword_styles = [
    {"pattern": r"\bremote\b", "icon": "🌍", "label": "Remote Role"},
    {"pattern": r"\bintern(ship)?\b", "icon": "🎓", "label": "Internship Opportunity"},
    {"pattern": r"\bhiring\b", "icon": "💼", "label": "We’re Hiring"},
    {"pattern": r"\bcontract\b", "icon": "📄", "label": "Contract Position"},
    {"pattern": r"\bpart[- ]?time\b", "icon": "🕒", "label": "Part-Time Role"},
    {"pattern": r"\bfull[- ]?time\b", "icon": "⏰", "label": "Full-Time Role"},
]

def detect_keywords(text):
    tags = []
    for kw in keyword_styles:
        if re.search(kw["pattern"], text, re.IGNORECASE):
            tags.append(f"{kw['icon']} {kw['label']}")
    return tags

# --- GENERATE BUTTON ---
if st.button("🎨 Generate Smart Poster"):
    if not os.listdir(bg_folder):
        st.error("❌ Please upload at least one background image.")
    elif not uploaded_logo:
        st.error("❌ Please upload RPAVault logo.")
    elif not job_text.strip():
        st.warning("⚠️ Paste job content before generating.")
    else:
        # --- PICK RANDOM THEME ---
        theme = random.choice(themes)

        # --- LOAD BACKGROUND ---
        bg_file = random.choice(os.listdir(bg_folder))
        bg = Image.open(os.path.join(bg_folder, bg_file)).convert("RGBA")
        bg = bg.resize((1080, 1920))

        # --- ADD GRADIENT ---
        gradient = Image.new("RGBA", bg.size, (0, 0, 0, 0))
        for y in range(bg.height):
            alpha = int(255 * (y / bg.height) * 0.65)
            gradient.putpixel((0, y), (0, 0, 0, alpha))
        gradient = gradient.resize(bg.size)
        bg = Image.alpha_composite(bg, gradient)

        # --- DRAW OBJECTS ---
        draw = ImageDraw.Draw(bg)
        title_font = ImageFont.truetype("arialbd.ttf", 80)
        body_font = ImageFont.truetype("arial.ttf", 44)
        tag_font = ImageFont.truetype("arialbd.ttf", 50)

        # --- HEADER BAR ---
        draw.rectangle([(0, 0), (1080, 200)], fill=theme["header"])
        draw.text((60, 60), "🚨 JOB ALERT", font=title_font, fill=theme["text"])

        # --- DETECT KEYWORDS ---
        tags = detect_keywords(job_text)
        y_offset = 220
        for tag in tags:
            draw.text((60, y_offset), tag, font=tag_font, fill=theme["text"])
            y_offset += 60

        # --- JOB DESCRIPTION ---
        wrapped_text = textwrap.fill(job_text, width=38)
        draw.multiline_text((80, y_offset + 40), wrapped_text, fill="white", font=body_font, spacing=10)

        # --- ADD LOGO ---
        logo = Image.open(uploaded_logo).convert("RGBA")
        logo_width = 280
        logo.thumbnail((logo_width, logo_width))
        bg.paste(logo, (bg.width - logo.width - 50, bg.height - logo.height - 50), logo)

        # --- SAVE OUTPUT ---
        output_buffer = io.BytesIO()
        final_img = bg.convert("RGB")
        final_img.save(output_buffer, format="JPEG")

        st.image(final_img, caption=f"RPAVault Smart Poster ({theme['name']})", use_container_width=True)
        st.download_button("⬇️ Download Image", output_buffer.getvalue(),
                           file_name=f"rpavault_smart_job_alert_{theme['name'].replace(' ', '_').lower()}.jpg",
                           mime="image/jpeg")
