import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests, random, io, textwrap, os, re

# --- CONFIG ---
st.set_page_config(page_title="RPAVault Job Poster", layout="centered")

# --- APP TITLE ---
st.markdown("""
# 🚨 Job Alert by RPAVault  
Generate beautiful, branded job alert posters — fully automated 💼
""")

# --- LOGO (from GitHub raw URL) ---
LOGO_URL = "https://raw.githubusercontent.com/<your-github-username>/rpavault-job-generator/main/rpavault_logo.png"

# --- UNSPLASH BACKGROUNDS (text-friendly categories) ---
unsplash_keywords = [
    "minimalist background",
    "plain wall texture",
    "soft gradient",
    "office desk blur",
    "corporate pattern",
    "abstract soft color"
]

# --- THEMES ---
themes = [
    {"name": "Sunset Red", "header": (255, 69, 0, 255), "text": "white"},
    {"name": "Ocean Blue", "header": (30, 144, 255, 255), "text": "white"},
    {"name": "Tech Purple", "header": (138, 43, 226, 255), "text": "white"},
    {"name": "Forest Green", "header": (0, 128, 0, 255), "text": "white"},
    {"name": "Golden Glow", "header": (255, 191, 0, 255), "text": "black"},
    {"name": "Crimson Bold", "header": (220, 20, 60, 255), "text": "white"},
]

# --- KEYWORD TAGS ---
keyword_styles = [
    {"pattern": r"\bremote\b", "icon": "🌍", "label": "Remote Role"},
    {"pattern": r"\bintern(ship)?\b", "icon": "🎓", "label": "Internship"},
    {"pattern": r"\bhiring\b", "icon": "💼", "label": "We’re Hiring"},
    {"pattern": r"\bcontract\b", "icon": "📄", "label": "Contract Role"},
    {"pattern": r"\bpart[- ]?time\b", "icon": "🕒", "label": "Part-Time"},
    {"pattern": r"\bfull[- ]?time\b", "icon": "⏰", "label": "Full-Time"},
]

# --- DETECT KEYWORDS ---
def detect_keywords(text):
    tags = []
    for kw in keyword_styles:
        if re.search(kw["pattern"], text, re.IGNORECASE):
            tags.append(f"{kw['icon']} {kw['label']}")
    return tags

# --- USER INPUT ---
job_text = st.text_area("📋 Paste Job Content", height=250, placeholder="Paste job description here...")

# --- GENERATE BUTTON ---
if st.button("🎨 Generate Poster"):
    if not job_text.strip():
        st.warning("⚠️ Please paste job content before generating.")
        st.stop()

    # --- PICK RANDOM THEME + BACKGROUND ---
        # --- PICK RANDOM THEME + BACKGROUND ---
    theme = random.choice(themes)
    keyword = random.choice(unsplash_keywords)

    # Try up to 3 times to get a valid image
    bg = None
    for attempt in range(3):
        unsplash_url = f"https://source.unsplash.com/1080x1350/?{keyword}"
        bg_response = requests.get(unsplash_url, timeout=10)
        content_type = bg_response.headers.get("Content-Type", "")
        if "image" in content_type:
            try:
                bg = Image.open(io.BytesIO(bg_response.content)).convert("RGBA")
                break
            except Exception:
                bg = None
        # pick another keyword if failed
        keyword = random.choice(unsplash_keywords)

    # fallback if Unsplash fails completely
    if bg is None:
        st.warning("⚠️ Unable to fetch Unsplash image, using fallback background.")
        fallback_url = "https://raw.githubusercontent.com/<your-github-username>/rpavault-job-generator/main/default_bg.jpg"
        fallback = requests.get(fallback_url)
        bg = Image.open(io.BytesIO(fallback.content)).convert("RGBA")

    # --- ADD GRADIENT OVERLAY ---
    gradient = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    for y in range(bg.height):
        alpha = int(200 * (y / bg.height))
        gradient.putpixel((0, y), (0, 0, 0, alpha))
    gradient = gradient.resize(bg.size)
    bg = Image.alpha_composite(bg, gradient)

    # --- DRAW TEXT ---
    draw = ImageDraw.Draw(bg)
    title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    body_font = ImageFont.truetype("DejaVuSans.ttf", 46)
    tag_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 50)

    # --- HEADER ---
    draw.rectangle([(0, 0), (1080, 180)], fill=theme["header"])
    draw.text((60, 50), "🚨 Job Alert by RPAVault", font=title_font, fill=theme["text"])

    # --- KEYWORD TAGS ---
    tags = detect_keywords(job_text)
    y_offset = 200
    for tag in tags:
        draw.text((60, y_offset), tag, font=tag_font, fill=theme["text"])
        y_offset += 60

    # --- JOB TEXT ---
    wrapped = textwrap.fill(job_text, width=38)
    draw.multiline_text((80, y_offset + 40), wrapped, fill="white", font=body_font, spacing=10)

    # --- LOGO (from GitHub raw) ---
    logo_response = requests.get(LOGO_URL)
    logo = Image.open(io.BytesIO(logo_response.content)).convert("RGBA")
    logo.thumbnail((220, 220))
    bg.paste(logo, (bg.width - logo.width - 40, bg.height - logo.height - 40), logo)

    # --- SAVE & SHOW ---
    output = io.BytesIO()
    bg.convert("RGB").save(output, format="JPEG")

    st.image(bg, caption=f"RPAVault Poster ({theme['name']})", use_container_width=True)
    st.download_button("⬇️ Download Poster",
                       output.getvalue(),
                       file_name="rpavault_job_poster.jpg",
                       mime="image/jpeg")
