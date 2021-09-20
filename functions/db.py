import json
import uuid
from pathlib import Path
from google.cloud import storage

import geopandas
from shapely.geometry import box
from threading import Thread
import time
from io import BytesIO


class GeoDb:

    def __init__(self, db_filename, image_directory, refresh_interval=60):
        self.db_filename = db_filename
        scheme, _ = split_scheme(db_filename)
        if scheme == "gs":
            self.storage = GoogleCloudStorage()
        elif scheme in (None, "file"):
            self.storage = LocalFileStorage()
        else:
            raise ValueError(f"uri scheme {scheme} not supported.")

        if not self.storage.exists(db_filename):
            empty_db = {
                "type": "FeatureCollection",
                "features": []
            }
            self.storage.save(json.dumps(empty_db, indent=4), self.db_filename)

        scheme, _ = split_scheme(db_filename)
        if scheme == "gs":
            self.image_store = GoogleCloudImageStore(image_directory)
        elif scheme in (None, "file"):
            self.image_store = LocalImageStore(image_directory)
        else:
            raise ValueError(f"uri scheme {scheme} not supported.")

        db_str = self.storage.load(self.db_filename)
        self.df = geopandas.read_file(db_str)

        self.refresh_thread = None
        self.refresh_interval = refresh_interval

    def insert(self, image, latlng, **kwargs):
        image_id = str(uuid.uuid4())
        image_url = self.image_store.save(image, f"{image_id}.jpg")
        kwargs["id"] = image_id
        kwargs["src"] = image_url
        db = json.loads(self.storage.load(self.db_filename))
        features = db.get("features")
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [latlng[1], latlng[0]]  # stored as longitude, latitude
                },
                "properties": kwargs
            }
        )
        self.storage.save(json.dumps(db, indent=4), self.db_filename)
        if self.refresh_thread is None:
            self.refresh_thread = Thread(target=self.refresh)
            self.refresh_thread.setDaemon(True)
            self.refresh_thread.start()
        return image_id

    def query(self, bound):
        q_box = box(bound[0][1], bound[0][0], bound[1][1], bound[1][0])

        res_df = self.df.iloc[self.df.sindex.query(q_box)]
        res = []
        cols = [col for col in self.df.columns if col != "geometry"]
        for idx, row in res_df.iterrows():
            item = {key: row[key] for key in cols}
            item["latlng"] = (row["geometry"].y, row["geometry"].x)
            res.append(item)

        return res

    def refresh(self):
        while True:
            print("thread running ")
            self.df = geopandas.read_file(self.storage.load(self.db_filename))
            time.sleep(self.refresh_interval)


def split_scheme(uri):

    res = uri.split("://")
    if len(res) == 2:
        return res
    elif len(res) == 1:
        return None, uri
    else:
        raise ValueError(f"Invalid uri {uri}")


class LocalFileStorage:

    def load(self, path, mode='r'):

        if Path(path).exists():
            with open(path, mode) as f:
                return f.read()
        else:
            raise ValueError(f"{path} does not exists.")

    def save(self, data, path, mode='w'):

        with open(path, mode) as f:
            f.write(data)

    def exists(self, path):

        return Path(path).exists()


class GoogleCloudStorage:

    def __init__(self):
        self.client = storage.Client()

    def load(self, path, mode='r'):

        blob = self._get_blob(path)
        if blob.exists():
            return blob.download_as_text()
        else:
            raise ValueError(f"{path} does not exists.")

    def save(self, data, path, mode='w'):

        blob = self._get_blob(path)
        blob.upload_from_string(data)

    def exists(self, path):

        blob = self._get_blob(path)
        return blob.exists()

    def _get_blob(self, path):

        scheme, p = split_scheme(path)
        assert scheme == "gs"
        bucket_name = p.split("/", 1)[0]
        bucket = self.client.bucket(bucket_name)
        try:
            p = p.split("/", 1)[1]
        except IndexError:
            raise ValueError(f"Invalid storage path: {path}")
        # Then do other things...
        blob = bucket.blob(p)
        return blob


class LocalImageStore:

    def __init__(self, directory):
        self.directory = directory

    def save(self, image, filename):
        path = Path(self.directory).joinpath(filename)
        image.save(path)
        return f"http://localhost:8000/{filename}"


class GoogleCloudImageStore:

    def __init__(self, directory):

        scheme, p = split_scheme(directory)
        assert scheme == "gs"
        self.bucket_name = p.split("/", 1)[0]
        client = storage.Client()
        self.bucket = client.bucket(self.bucket_name)
        try:
            self.prefix = p.split("/", 1)[1]
        except IndexError:
            self.prefix = ''

    def save(self, image, filename):
        path = Path(self.prefix).joinpath(filename)
        bio = BytesIO()
        image.save(bio, format="jpeg")
        bio.seek(0)
        blob = self.bucket.blob(str(path))
        blob.upload_from_file(bio)
        return f"https://storage.googleapis.com/{self.bucket_name}/{str(path)}"
