
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

def font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def regular_font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/generate")
def generate():
    name = (request.form.get("name") or "DEMO USER")[:40]
    school = (request.form.get("school") or "DEMO UNIVERSITY")[:50]
    student_id = (request.form.get("student_id") or "DEMO-000001")[:30]

    W, H = 1000, 620
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # Header and border
    d.rounded_rectangle((20, 20, W-20, H-20), radius=35, outline="black", width=4)
    d.rectangle((20, 20, W-20, 150), fill=(235, 235, 235))
    d.text((55, 55), "DEMO STUDENT CARD", font=font(46), fill="black")
    d.text((55, 115), "SAMPLE ONLY — NOT VALID FOR VERIFICATION", font=font(22), fill="black")

    # Portrait placeholder / upload
    px, py, pw, ph = 60, 205, 270, 330
    portrait = request.files.get("photo")
    if portrait and portrait.filename:
        try:
            pimg = Image.open(portrait.stream).convert("RGB")
            pimg.thumbnail((pw, ph))
            canvas = Image.new("RGB", (pw, ph), (225, 225, 225))
            ox = (pw - pimg.width) // 2
            oy = (ph - pimg.height) // 2
            canvas.paste(pimg, (ox, oy))
            img.paste(canvas, (px, py))
        except Exception:
            d.rectangle((px, py, px+pw, py+ph), fill=(225, 225, 225), outline="black", width=2)
            d.text((px+45, py+145), "PHOTO", font=font(32), fill="black")
    else:
        d.rectangle((px, py, px+pw, py+ph), fill=(225, 225, 225), outline="black", width=2)
        d.text((px+45, py+145), "PHOTO", font=font(32), fill="black")

    # Text fields
    x = 380
    d.text((x, 210), "NAME", font=font(22), fill="black")
    d.text((x, 245), name, font=regular_font(36), fill="black")

    d.text((x, 330), "SCHOOL", font=font(22), fill="black")
    d.text((x, 365), school, font=regular_font(34), fill="black")

    d.text((x, 450), "DEMO ID", font=font(22), fill="black")
    d.text((x, 485), student_id, font=regular_font(34), fill="black")

    # Strong diagonal watermark baked into image
    overlay = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    od = ImageDraw.Draw(overlay)
    wm_font = font(100)
    wm = "SAMPLE • NOT VALID"
    bbox = od.textbbox((0,0), wm, font=wm_font)
    tw = bbox[2]-bbox[0]
    th = bbox[3]-bbox[1]
    od.text(((W-tw)//2, (H-th)//2), wm, font=wm_font, fill=(0,0,0,80))
    overlay = overlay.rotate(18, expand=False, center=(W//2,H//2))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    buf = BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png", as_attachment=True, download_name="demo_student_card.png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
