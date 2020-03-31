import psycopg2
from api.config.config import get_config


class LocationDAO(object):
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())

    def insert_location(self, latitude, longitude):
        cursor = self.conn.cursor()
        query = "insert into location(latitude, longitude) values (%s, %s) returning location_id;"
        cursor.execute(query, (latitude, longitude))
        location_id = cursor.fetchone()[0]
        self.conn.commit()

        return location_id

    def update_location(self, location_id, latitude, longitude):
        cursor = self.conn.cursor()
        query = "update location set latitude=%s, longitude=%s where location_id=%s"
        cursor.execute(query, (latitude, longitude, location_id))
        self.conn.commit()

        return location_id

    def delete_location(self, location_id):
        cursor = self.conn.cursor()
        query = "delete from location where location_id = %s;"
        cursor.execute(query, (location_id,))
        self.conn.commit()

        return location_id
