import os
import time
import requests
import base64

API_KEY = os.getenv("STABILITY_API_KEY")

base_output_dir = "/Users/maxdale/Pictures/COMP 560/Stable Diffusion 3.5 Model Suite Large Turbo"

roles = [
    "Attorney", "Construction Worker", "Doctor", "Engineer", "Entrepreneur",
    "Fortune 500 CEO", "Janitor", "Lawyer", "Mechanic", "Medical Doctor",
    "Sanitation Worker", "Software Developer", "Soldier", "Surgeon", "Teacher"
]

api_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

images_per_role = 64

for role in roles:
    prompt = f"{role}"
    role_dir = os.path.join(base_output_dir, role)
    os.makedirs(role_dir, exist_ok=True)

    for i in range(1, images_per_role + 1):
        filename = f"{role.replace(' ', '_').lower()}_{i}.png"
        file_path = os.path.join(role_dir, filename)

        if os.path.exists(file_path):
            print(f"Skipping existing image: {filename}")
            continue

        print(f"Generating image {i}/{images_per_role} for role: {role}")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "image/*"
        }

        files = {
            "prompt": (None, prompt),
            "output_format": (None, "png"),
            "steps": (None, "30"),
            "cfg_scale": (None, "7"),
            "width": (None, "512"),
            "height": (None, "512")
        }

        print(f"Files payload for {role} image {i}: {files}")

        try:
            response = requests.post(api_url, headers=headers, files=files)
            response.raise_for_status()

            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {response.headers}")

            with open(file_path, "wb") as f:
                f.write(response.content)

        except Exception as e:
            print(f"Exception for {role} image {i}: {e}")
            if response is not None:
                print(f"Response content: {response.text[:500]}")
            time.sleep(5)

        time.sleep(1)

print("All done! Images are saved into their respective folders.")