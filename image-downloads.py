import os
import requests

# Configuration
api_url = "https://fontainerents.com/wp-json/wp/v2/media"
download_directory = "fontaine_images"
per_page = 100  # Maximum items per page allowed by WordPress.

# Create the download directory if it doesn't exist
os.makedirs(download_directory, exist_ok=True)

def download_images():
    page = 1
    while True:
        # Fetch the media items from the API
        response = requests.get(api_url, params={"per_page": per_page, "page": page})
        
        if response.status_code == 200:
            media_items = response.json()
            if not media_items:  # Break if no more items
                print("All images downloaded.")
                break
            
            for item in media_items:
                if "source_url" in item:  # Ensure the item has a source URL
                    image_url = item["source_url"]
                    image_name = os.path.basename(image_url)
                    image_path = os.path.join(download_directory, image_name)

                    # Download the image
                    try:
                        print(f"Downloading {image_url}...")
                        img_data = requests.get(image_url).content
                        with open(image_path, "wb") as image_file:
                            image_file.write(img_data)
                        print(f"Saved {image_name} to {download_directory}.")
                    except Exception as e:
                        print(f"Failed to download {image_url}: {e}")

            page += 1
        elif response.status_code == 400 and "rest_post_invalid_page_number" in response.text:
            print("Reached the end of available pages.")
            break
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            break

if __name__ == "__main__":
    download_images()
