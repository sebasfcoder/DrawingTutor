import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv("GEMINI_API_KEY_2")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables.")
    exit(1)

client = genai.Client(api_key=api_key)

prompts = {
    "m2_l1_bad_mixed": "Manga drawing tutorial example. Two manga eyes that look messy and inconsistent. Bad example. Black ink on white paper.",
    "m2_l2_good_highlights": "Manga drawing tutorial example. A pair of manga eyes with two distinct white highlights in each iris. The highlights are clear and not colored over. Black ink on white paper.",
    "m2_l2_bad_nohighlights": "Manga drawing tutorial example. A pair of manga eyes with no highlights. They look dead and flat. Bad example. Black ink on white paper.",
    "m2_l3_good_emotions": "Manga drawing tutorial example. Two eyes showing emotion: one 'Happy' eye arched up, and one 'Sad' eye arched down. Expressive line art. Black ink on white paper.",
    "m2_l3_bad_flat": "Manga drawing tutorial example. Two eyes that look flat and emotionless. Straight lines, no arch. Bad example. Black ink on white paper.",
    
    "m3_l1_good_sweat": "Manga drawing tutorial example. A face with a giant sweat drop symbol high on the head. Nervous expression. Black ink on white paper.",
    "m3_l1_bad_small": "Manga drawing tutorial example. A face with a tiny, barely visible sweat drop. Bad example. Black ink on white paper.",
    "m3_l2_good_vein": "Manga drawing tutorial example. An angry chibi face with a clear popping vein symbol (cross shape). Black ink on white paper.",
    "m3_l2_bad_notangry": "Manga drawing tutorial example. A happy face with a popping vein symbol. Confusing and wrong. Bad example. Black ink on white paper.",
    "m3_l3_good_sparkles": "Manga drawing tutorial example. A character surrounded by 'Shojo' sparkles and flowers. Beautiful and dreamy. Black ink on white paper.",
    "m3_l3_bad_few": "Manga drawing tutorial example. A character with one sad sparkle. Boring. Bad example. Black ink on white paper.",

    "m4_l1_good_profile": "Manga drawing tutorial example. A character in profile view (side view). Correct nose and chin alignment. Black ink on white paper.",
    "m4_l1_bad_flat": "Manga drawing tutorial example. A profile view where the face looks flat and 2D. Bad example. Black ink on white paper.",
    "m4_l2_good_34": "Manga drawing tutorial example. A face in 3/4 view (selfie angle). Showing a bit of the side of the head. Correct proportions. Black ink on white paper.",
    "m4_l2_bad_front": "Manga drawing tutorial example. A front view face labeled as 3/4 view. Incorrect. Bad example. Black ink on white paper.",
    "m4_l3_good_up": "Manga drawing tutorial example. A face looking up at the sky. Chin up, ears down. Perspective. Black ink on white paper.",
    "m4_l3_bad_normal": "Manga drawing tutorial example. A face looking straight ahead, not up. Bad example. Black ink on white paper.",

    "m5_l1_good_ratio": "Manga drawing tutorial example. A stick figure that is exactly 6 heads tall. Proportional. Black ink on white paper.",
    "m5_l1_bad_short": "Manga drawing tutorial example. A stick figure that is only 3 heads tall but meant to be standard. Too short. Bad example. Black ink on white paper.",
    "m5_l2_good_chibi": "Manga drawing tutorial example. A cute Chibi character, 2 heads tall. Big head, small body. Black ink on white paper.",
    "m5_l2_bad_lanky": "Manga drawing tutorial example. A Chibi character that is too tall and lanky. Not cute. Bad example. Black ink on white paper.",
    "m5_l3_good_peace": "Manga drawing tutorial example. A hand making the V-sign (peace sign). Correct finger placement. Black ink on white paper.",
    "m5_l3_bad_sausage": "Manga drawing tutorial example. A hand making a peace sign but the fingers look like sausages. Bad example. Black ink on white paper.",

    "m6_l1_good_folds": "Manga drawing tutorial example. A t-shirt hanging on a torso with natural folds from the shoulders. Gravity. Black ink on white paper.",
    "m6_l1_bad_stiff": "Manga drawing tutorial example. A t-shirt that looks like a stiff cardboard box. No folds. Bad example. Black ink on white paper.",
    "m6_l2_good_accessories": "Manga drawing tutorial example. A character wearing a big cute bow on their head. Fits well. Black ink on white paper.",
    "m6_l2_bad_floating": "Manga drawing tutorial example. A hat floating above the character's head. Not wearing it. Bad example. Black ink on white paper.",
    "m6_l3_good_uniform": "Manga drawing tutorial example. A classic sailor-style school uniform collar. Correct details. Black ink on white paper.",
    "m6_l3_bad_wrong": "Manga drawing tutorial example. A school uniform collar that looks like a regular shirt. Wrong shape. Bad example. Black ink on white paper.",

    "m7_l1_good_shadow": "Manga drawing tutorial example. A sphere with a clear light source and cast shadow. 3D effect. Black ink on white paper.",
    "m7_l1_bad_noshadow": "Manga drawing tutorial example. A flat circle with no shadow. 2D. Bad example. Black ink on white paper.",
    "m7_l2_good_angel": "Manga drawing tutorial example. Hair with a shiny 'Angel Ring' highlight. Glossy and healthy. Black ink on white paper.",
    "m7_l2_bad_matte": "Manga drawing tutorial example. Hair that looks dull and matte. No highlights. Bad example. Black ink on white paper.",
    "m7_l3_good_backlight": "Manga drawing tutorial example. A character in silhouette with light coming from behind (backlighting). Dramatic. Black ink on white paper.",
    "m7_l3_bad_bright": "Manga drawing tutorial example. A character that is fully lit even though the light is behind them. Incorrect. Bad example. Black ink on white paper.",

    "m8_l1_good_skin": "Manga drawing tutorial example. A face colored with 3 shades of skin tone (base, shadow, blush). Soft and nice. Color.",
    "m8_l1_bad_flat": "Manga drawing tutorial example. A face colored with one flat beige color. No depth. Bad example. Color.",
    "m8_l2_good_gradient": "Manga drawing tutorial example. An eye colored with a vertical gradient from dark to light. Shiny. Color.",
    "m8_l2_bad_solid": "Manga drawing tutorial example. An eye colored with a single solid color. Flat. Bad example. Color.",
    "m8_l3_good_hair": "Manga drawing tutorial example. Hair colored with a base tone and darker shadows. Depth. Color.",
    "m8_l3_bad_one": "Manga drawing tutorial example. Hair colored with one flat color. No shadows. Bad example. Color.",

    "m9_l1_good_thirds": "Manga drawing tutorial example. A simple scene composition using the rule of thirds. Balanced. Black ink on white paper.",
    "m9_l1_bad_center": "Manga drawing tutorial example. A scene where everything is dead center. Boring composition. Bad example. Black ink on white paper.",
    "m9_l2_good_dynamic": "Manga drawing tutorial example. A diagonal panel border for an action scene. Dynamic and exciting. Black ink on white paper.",
    "m9_l2_bad_box": "Manga drawing tutorial example. A standard square box for an action scene. Boring. Bad example. Black ink on white paper.",
    "m9_l3_good_bubbles": "Manga drawing tutorial example. A spiky speech bubble for shouting and a cloud bubble for thinking. Correct shapes. Black ink on white paper.",
    "m9_l3_bad_wrong": "Manga drawing tutorial example. A spiky bubble used for whispering. Wrong context. Bad example. Black ink on white paper."
}

print("Starting generation with model: gemini-2.5-flash-image")
print("-" * 50)

output_dir = "app/static/img"
os.makedirs(output_dir, exist_ok=True)

for name, prompt in prompts.items():
    filepath = os.path.join(output_dir, f"{name}.png")
    if os.path.exists(filepath):
        print(f"Skipping {name}: Image already exists at {filepath}")
        print("-" * 50)
        continue

    print(f"Generating {name}...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt],
        )
        
        generated = False
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                filepath = os.path.join(output_dir, f"{name}.png")
                image.save(filepath)
                print(f"Saved to {filepath}")
                generated = True
                break # Only save the first image
        
        if not generated:
            print(f"No image found in response for {name}")

    except Exception as e:
        print(f"Failed to generate {name}: {e}")
    print("-" * 50)
