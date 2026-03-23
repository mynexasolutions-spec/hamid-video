from flask import Flask, render_template
import cloudinary_config
from cloudinary.api import subfolders, resources_by_asset_folder
from cloudinary.utils import cloudinary_url

app = Flask(__name__)

GALLERY_ROOT = "Hamid_video_films"


def get_folder_images(folder_name, count, width=600, crop="fill"):
    """Fetch `count` optimized image URLs from a Hamid_video_films subfolder."""
    result = resources_by_asset_folder(
        f"{GALLERY_ROOT}/{folder_name}",
        resource_type="image",
        max_results=count
    )
    urls = []
    for img in result.get("resources", []):
        url, _ = cloudinary_url(
            img["public_id"],
            width=width,
            crop=crop,
            quality="auto",
            fetch_format="auto"
        )
        urls.append(url)
    return urls


@app.route('/')
def index():
    return render_template('pages/index.html')

def collect_folder_paths(root):
    """Recursively return all folder paths under root, sorted alphabetically."""
    try:
        resp = subfolders(root)
    except Exception:
        return []
    paths = []
    for folder in sorted(resp.get("folders", []), key=lambda f: f["path"].lower()):
        paths.append(folder["path"])
        paths.extend(collect_folder_paths(folder["path"]))
    return paths


@app.route("/gallery")
def gallery():
    all_paths = collect_folder_paths(GALLERY_ROOT)

    folders_data = []
    for folder_path in all_paths:
        result = resources_by_asset_folder(
            folder_path,
            resource_type="image",
            max_results=500
        )

        resources_sorted = sorted(
            result.get("resources", []),
            key=lambda r: r.get("created_at", "")
        )

        images = []
        for img in resources_sorted:
            optimized_url, _ = cloudinary_url(
                img["public_id"],
                width=600,
                crop="fill",
                quality="auto",
                fetch_format="auto"
            )
            images.append({"url": optimized_url})

        if images:
            folders_data.append({"name": folder_path.split("/")[-1], "images": images})

    return render_template("pages/gallery.html", folders=folders_data)

@app.route("/films")
def films():
    return render_template("pages/films.html")

@app.route("/about")
def about():
    return render_template("pages/about.html")

@app.route("/contact")
def contact():
    return render_template("pages/contact.html")

@app.route("/wedding-photography")
def wedding_photography():
    feature_images = get_folder_images("Brides", 4, width=800, crop="fit")
    gallery_images = get_folder_images("Highlight Shots", 6)
    return render_template("pages/wedding-photography.html",
                           feature_images=feature_images,
                           gallery_images=gallery_images)

@app.route("/pre-wedding")
def pre_wedding():
    feature_images = get_folder_images("Enaggemt", 4, width=800, crop="fit")
    gallery_images = get_folder_images("Enaggemt", 9)
    return render_template("pages/pre-wedding.html",
                           feature_images=feature_images,
                           gallery_images=gallery_images)

@app.route("/cinematography")
def cinematography():
    feature_images = get_folder_images("Enaggemt", 4, width=800, crop="fit")
    return render_template("pages/cinematography.html",
                           feature_images=feature_images)

@app.route("/wedding-stories")
def wedding_stories():
    feature_images = get_folder_images("soniya", 4, width=800, crop="fit")
    gallery_images = get_folder_images("rahil", 3)
    return render_template("pages/wedding-stories.html",
                           feature_images=feature_images,
                           gallery_images=gallery_images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)