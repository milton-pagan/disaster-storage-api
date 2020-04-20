import psycopg2
from app.config.config import get_config
from app.handlers.error_handler import ErrorHandler
from app.dao.category_info import categories


class CategoryDAO(object):
    def __init__(self):
        self.conn = psycopg2.connect(**get_config())
        self.categories = categories

    def check_category_attributes(self, category, payload):
        try:
            for attribute in self.categories[category]["attributes"]:
                if attribute not in payload:
                    return ErrorHandler().bad_request("Invalid category attributes")
        except KeyError:
            return ErrorHandler().bad_request("Invalid category")

    def insert_product_category_info(self, category_name, product_id, payload):
        try:
            category = self.categories[category_name]
        except KeyError:
            return ErrorHandler().bad_request("Invalid category")

        cursor = self.conn.cursor()
        query = (
            "insert into "
            + category_name
            + "("
            + "".join(map(lambda attribute: attribute + ", ", category["attributes"]))
            + "product_id) values ("
            + "".join(["%s, " for i in category["attributes"]])
            + "%s) returning "
            + category_name
            + "_id;"
        )

        try:
            temp = [payload[attribute] for attribute in category["attributes"]]
            temp.append(product_id)
        except KeyError:
            return ErrorHandler().bad_request("Invalid category attributes")

        cursor.execute(
            query, tuple(temp),
        )

        id = cursor.fetchone()[0]
        self.conn.commit()

        return id

    def update_product_category_info(self, category_name, product_id, payload):
        try:
            category = self.categories[category_name]
        except KeyError:
            return ErrorHandler().bad_request("Invalid category")

        cursor = self.conn.cursor()
        query = (
            "update "
            + category_name
            + " set "
            + "".join(
                map(
                    lambda attribute: attribute + " = %s, ", category["attributes"][:-1]
                )
            )
            + category["attributes"][-1]
            + "=%s where product_id = %s returning "
            + category_name
            + "_id;"
        )

        try:
            temp = [payload[attribute] for attribute in category["attributes"]]
            temp.append(product_id)
        except KeyError:
            return ErrorHandler().bad_request("Invalid category attributes")

        cursor.execute(
            query, tuple(temp),
        )

        id = cursor.fetchone()[0]
        self.conn.commit()

        return id

    def delete_category_info(self, category_name, product_id):
        try:
            self.categories[category_name]
        except KeyError:
            return ErrorHandler().bad_request("Invalid category")

        cursor = self.conn.cursor()

        query = (
            "delete from "
            + category_name
            + " where product_id= %s returning "
            + category_name
            + "_id;"
        )
        cursor.execute(query, (product_id,))
        id = cursor.fetchone()[0]
        self.conn.commit()

        return id
