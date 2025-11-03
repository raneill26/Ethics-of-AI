import openai
import os
import time
import requests

openai.api_key = "[KEY-REMOVED]"

base_output_dir = "/Users/maxdale/Pictures/COMP 311/DALL-E 3"

roles = [
    "Attorney", "Construction Worker", "Doctor", "Engineer", "Entrepreneur",
    "Fortune 500 CEO", "Janitor", "Lawyer", "Mechanic", "Medical Doctor",
    "Sanitation Worker", "Software Developer", "Soldier", "Surgeon", "Teacher"
]

for role in roles:
    prompt = f"Create a picture of a {role.lower()}."
    role_dir = os.path.join(base_output_dir, role)

    if not os.path.exists(role_dir):
        print(f"Folder not found for role: {role}. Skipping.")
        continue

    existing_files = {
        fname for fname in os.listdir(role_dir)
        if fname.endswith(".png") and fname.startswith(role.replace(' ', '_').lower())
    }

    for i in range(64):
        filename = f"{role.replace(' ', '_').lower()}_{i + 1}.png"
        if filename in existing_files:
            print(f"Skipping existing image: {filename}")
            continue

        print(f"Generating image {i + 1}/64 for role: {role}")
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard"
            )
            image_url = response.data[0].url

            image_data = requests.get(image_url).content
            with open(os.path.join(role_dir, filename), "wb") as f:
                f.write(image_data)

            time.sleep(1)

        except Exception as e:
            print(f"Error generating image {i + 1} for {role}: {e}")
            time.sleep(5)

print("Complete!")