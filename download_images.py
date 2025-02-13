 
from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

# ✅ Download 1000 Embryo Images
embryo_args = {
    "keywords": "human embryo under microscope",
    "limit": 1000,
    "print_urls": True,
    "output_directory": "dataset",
    "image_directory": "embryo",
    "format": "jpg"
}
response.download(embryo_args)

# ✅ Download 1000 Non-Embryo Images (Random Objects, Animals, etc.)
non_embryo_args = {
    "keywords": "random objects, landscapes, cars, animals",
    "limit": 1000,
    "print_urls": True,
    "output_directory": "dataset",
    "image_directory": "non_embryo",
    "format": "jpg"
}
response.download(non_embryo_args)

print("✅ Images downloaded successfully!")
