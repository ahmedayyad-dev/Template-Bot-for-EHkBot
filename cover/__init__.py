import textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont, ImageEnhance
import random


class ProfessionalBackgroundGenerator:

    def __init__(self, image_path, size=(1280, 720)):
        self.image_path = image_path
        self.width, self.height = size
        self.size = size

    def create_gradient_overlay(self):
        gradient = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)

        for y in range(self.height):
            alpha = int(255 * (y / self.height) * 0.5)
            draw.rectangle([(0, y), (self.width, y + 1)], fill=(0, 0, 0, alpha))

        center_x, center_y = self.width // 2, self.height // 2
        max_radius = max(self.width, self.height)

        for r in range(0, max_radius, 5):
            alpha = int(120 * (1 - (r / max_radius)))
            if alpha > 0:
                draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
                             outline=(0, 0, 0, alpha), width=5)

        return gradient

    def apply_professional_effects(self, image):
        image = image.convert("L")
        image = ImageOps.autocontrast(image, cutoff=2)
        # هنا المشكلة - لازم نضمن أن الـ alpha = 255
        image = image.convert("RGB")  # تحويل لـ RGB بدلاً من RGBA
        image = image.filter(ImageFilter.GaussianBlur(2))
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=3))
        # تحويل لـ RGBA مع alpha كامل
        image = image.convert("RGBA")

        return image

    def create_vignette(self, strength=0.7):
        vignette = Image.new('L', self.size, 255)
        draw = ImageDraw.Draw(vignette)

        center_x, center_y = self.width // 2, self.height // 2

        for i in range(255, 0, -2):
            width = int(self.width * (i / 255))
            height = int(self.height * (i / 255))

            draw.ellipse([center_x - width // 2, center_y - height // 2,
                          center_x + width // 2, center_y + height // 2],
                         fill=i)

        return vignette.filter(ImageFilter.GaussianBlur(30))

    def add_noise_texture(self, image, intensity=0.05):
        pixels = image.load()

        num_pixels = int(self.width * self.height * intensity)

        for _ in range(num_pixels):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            current_pixel = pixels[x, y]
            noise_value = random.randint(-20, 20)

            new_r = max(0, min(255, current_pixel[0] + noise_value))
            new_g = max(0, min(255, current_pixel[1] + noise_value))
            new_b = max(0, min(255, current_pixel[2] + noise_value))

            pixels[x, y] = (new_r, new_g, new_b, 255)

        return image

    def generate(self):
        # خلفية سوداء أساسية
        final_bg = Image.new("RGB", self.size, (20, 20, 20))

        try:
            # فتح الصورة
            img = Image.open(self.image_path)

            # تحويل للأبيض والأسود
            img = img.convert('L')

            # تكبير الصورة
            img = img.resize((self.width, self.height), Image.LANCZOS)

            # تطبيق blur
            img = img.filter(ImageFilter.GaussianBlur(radius=20))

            # تحويل لـ RGB
            img = img.convert('RGB')

            # تقليل السطوع
            img = ImageEnhance.Brightness(img).enhance(0.4)

            # دمج الصورة مع الخلفية السوداء
            final_bg.paste(img, (0, 0))

        except Exception as e:
            print(f"Error loading image: {e}")
            # الخلفية السوداء تبقى كما هي

        # تحويل نهائي لـ RGBA
        final_bg = final_bg.convert('RGBA')
        return final_bg


def apply_circle_mask(image):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image.size, fill=255)

    mask = mask.filter(ImageFilter.GaussianBlur(1))

    result = Image.new('RGBA', image.size, (255, 255, 255, 0))
    result.paste(image, mask=mask)
    return result


def convert_num_to_words(number):
    if number is None:
        number = 0
    if isinstance(number, str):
        if number.isdigit():
            number = int(number)
        else:
            return number
    if number < 1000:
        return str(number)
    elif number < 1000000:
        return f"{number / 1000:.1f}k"
    elif number < 1000000000:
        return f"{number / 1000000:.1f}m"
    elif number < 1000000000000:
        return f"{number / 1000000000:.1f}b"
    else:
        return f"{number / 1000000000000:.1f}t"


async def generate_cover(duration, thumbnail_path, views, state):
    bg_generator = ProfessionalBackgroundGenerator(thumbnail_path)
    background = bg_generator.generate()

    draw = ImageDraw.Draw(background)
    views = convert_num_to_words(views)

    thumb_pos = (180, 160)
    thumb_size = (380, 380)
    texts = {
        "state": (state, 60, (630, 210), 40),
        "duration_views": (f"Duration: {duration}" + (f" | Views: {views}" if views else ''), 34, (630, 300), 0)
    }

    try:
        thumbnail = Image.open(thumbnail_path).resize(thumb_size, Image.LANCZOS)
        thumbnail = apply_circle_mask(thumbnail)
    except:
        thumbnail = apply_circle_mask(Image.new('RGBA', thumb_size, (50, 50, 50, 255)))

    circle_center = (thumb_pos[0] + thumb_size[0] // 2, thumb_pos[1] + thumb_size[1] // 2)
    circle_radius = thumb_size[0] // 2

    for i in range(3, 0, -1):
        glow_radius = circle_radius + (i * 3)
        alpha = 80 // i
        draw.ellipse([circle_center[0] - glow_radius, circle_center[1] - glow_radius,
                      circle_center[0] + glow_radius, circle_center[1] + glow_radius],
                     outline=(255, 255, 255, alpha), width=2)

    draw.ellipse([circle_center[0] - circle_radius - 5, circle_center[1] - circle_radius - 5,
                  circle_center[0] + circle_radius + 5, circle_center[1] + circle_radius + 5],
                 outline=(255, 255, 255, 255), width=3)

    if thumbnail.mode == 'RGBA':
        background.paste(thumbnail, thumb_pos, thumbnail)
    else:
        background.paste(thumbnail, thumb_pos)

    font_path = "cover/DejaVuSerifCondensed-Italic.ttf"

    for key, (text, size, pos, wrap_width) in texts.items():
        if wrap_width:
            text = textwrap.fill(text, width=wrap_width)

        font = ImageFont.truetype(font_path, size)
        lines = text.split('\n')

        for i, line in enumerate(lines):
            x, y = pos[0], pos[1] + i * 60
            draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))

    background.save(thumbnail_path, format="PNG", optimize=True, quality=95)
    return thumbnail_path