from lib import allow_cors, auth
from db import GeoDb
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("app")

db = GeoDb("db.geojson", "../data")

ADMINS = ["saswata.12@gmail.com", "m.imagination.m@gmail.com"]


@allow_cors
def app(request):

    if request.method == "POST":
        return upload(request)
    elif request.method == "GET":
        return list_images(request)
    else:
        return ("Not allowed", 405)


@auth(allowed_users=ADMINS)
def upload(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response>`.
    """

    try:
        image = Image.open(request.files["image"])
        metdata = get_image_metadata(image)
        logger.info(f"got metadata: {metdata}")
        metdata["description"] = request.form["description"]
        id = db.insert(image=image, **metdata)
        return id
    except Exception as e:
        logger.exception("exception while uploading.")
        return str(e), 500


def get_image_metadata(image):
    info = image.getexif()
    exif_table = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exif_table[decoded] = value
    if "GPSInfo" not in exif_table:
        raise ValueError("missing gps info in image.")
    gps_info = {}
    for key in exif_table['GPSInfo'].keys():
        decode = GPSTAGS.get(key, key)
        gps_info[decode] = exif_table['GPSInfo'][key]

    latitude = gps_info["GPSLatitude"]
    latitude = latitude[0] + latitude[1]/60.0 + latitude[2]/(60.0*60.0)
    if gps_info["GPSLatitudeRef"].lower() == "s":
        latitude *= -1
    longitude = gps_info["GPSLongitude"]
    longitude = longitude[0] + longitude[1] / 60.0 + longitude[2] / (60.0 * 60.0)
    if gps_info["GPSLongitudeRef"].lower() == "w":
        longitude *= -1
    return {
        "latlng": [latitude, longitude],
        "date": gps_info.get("GPSDateStamp")
    }


def list_images(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response>`.
    """
    logging.info(request.args["ne"])
    logging.info(request.args["sw"])
    ne = [float(x) for x in request.args["ne"].split(",")]
    sw = [float(x) for x in request.args["sw"].split(",")]
    return {"images": db.query(bound=[ne, sw])}
