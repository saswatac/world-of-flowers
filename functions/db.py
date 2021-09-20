import json
import uuid
from pathlib import Path

import geopandas
from shapely.geometry import box
from threading import Thread
import time


class GeoDb:

    def __init__(self, db_filename, image_directory, refresh_interval=1):
        self.db_filename = db_filename
        self.storage = LocalFileStorage()
        if not Path(self.db_filename).exists():
            empty_db = {
                "type": "FeatureCollection",
                "features": []
            }
            self.storage.save(json.dumps(empty_db, indent=4), self.db_filename)

        self.image_store = LocalImageStore(image_directory)
        self.df = geopandas.read_file(self.storage.load(self.db_filename))

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

        if self.refresh_thread is None:
            self.refresh_thread = Thread(target=self.refresh)
            self.refresh_thread.setDaemon(True)
            self.refresh_thread.start()

        return res

    def refresh(self):
        while True:
            print("thread running ")
            self.df = geopandas.read_file(self.storage.load(self.db_filename))
            time.sleep(self.refresh_interval)


class LocalFileStorage:

    def load(self, filename, mode='r'):

        if Path(filename).exists():
            with open(filename, mode) as f:
                return f.read()
        else:
            raise ValueError(f"{filename} does not exists.")

    def save(self, data, filename, mode='w'):

        with open(filename, mode) as f:
            f.write(data)


class LocalImageStore:

    def __init__(self, directory):
        self.directory = directory

    def save(self, image, filename):
        path = Path(self.directory).joinpath(filename)
        image.save(path)
        return f"http://localhost:8000/{filename}"
