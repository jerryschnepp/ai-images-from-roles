import requests
import time
import os

# Access the API key from an environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Load roles from a file
def load_roles(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Save image data to a file
def save_image(image_data, role):
    directory = "generated_images"
    if not os.path.exists(directory):
        os.makedirs(directory)
    image_path = os.path.join(directory, f"{role.replace(' ', '_')}.png")
    with open(image_path, "wb") as file:
        file.write(image_data)
    return image_path

# Main function to generate and save images for each role
def generate_images_for_roles(api_key, roles):
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.openai.com/v1/images/generations"

    for role in roles:
        prompt = f"Create a photorealistic image of a perfect {role} in a professional setting, focusing on natural poses, correct anatomy, with natural facial expressions and hand shapes. The depiction should be as realistic and lifelike as possible, showcasing the individual in a manner that accurately represents their role in society."
        # prompt = f"Create an image of the perfect {role}"
        response = requests.post(url, headers=headers, json={"prompt": prompt, "n": 1, "size": "1024x1024"})
        
        if response.status_code == 200:
            image_data = response.json()['data'][0]['url']
            image_response = requests.get(image_data)
            if image_response.status_code == 200:
                image_path = save_image(image_response.content, role)
                print(f"Image saved for {role}: {image_path}")
            else:
                print(f"Failed to download image for {role}")
        else:
            print(f"Error generating image for {role}: {response.text}")
            # Simple retry logic after waiting a bit in case of rate limit errors
            if response.status_code == 429:
                print("Rate limit exceeded, waiting before retrying...")
                time.sleep(60)  # Wait for 60 seconds before retrying
                continue  # Consider adding retry logic here

        # Wait a short time between requests to respect rate limits
        time.sleep(1)

if __name__ == "__main__":
    roles = load_roles("roles.txt")
    generate_images_for_roles(api_key, roles)


