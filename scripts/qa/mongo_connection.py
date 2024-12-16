import os
import traceback
import pymongo
from dotenv import load_dotenv
import logging

logger = logging.getLogger("mongoConnection")
logging.basicConfig(level=logging.ERROR)

class MongoConnection:
    def __init__(self):
        logger.debug(
            "Start: mongoConnection().__init__(), trying to load environment variables in docker"
        )
        self.host = None
        self.port = None
        self.database = None

        try:
            self.host = os.environ["mongo_host"]
            self.port = os.environ["mongo_port"]
            self.database = os.environ["mongo_db"]
        except:
            logger.warning(
                f"Can't load environment variables from docker... trying local .env file instead..."
            )
        try:
            logger.debug(
                "Start: mongoConnection().__init__(), trying to load environment variables with local .env file"
            )
            load_dotenv(".env")
            self.host = os.environ.get("mongo_host")
            self.port = os.environ("mongo_port")
            self.database = os.environ.get("mongo_db")
        except:
            logger.warning(f"Can't load environment variables from local .env file")

    def get_mongo_connection(self):
        try:
            mongo_client = pymongo.MongoClient(
                f"mongodb://{self.host}:{self.port}/", serverSelectionTimeoutMS=1200000
            )
            database = mongo_client[self.database]
            return database
        except Exception:
            logger.error(
                f"Can't connect to Mongo\nMake sure you have filled out the correct environment variables in the .env file"
            )
            logger.error(traceback.format_exc())
            logger.error(self.host)
            os.sys.exit()

    def get_mongo_session(self):
        session = pymongo.MongoClient(
            f"mongodb://{self.host}:{self.port}/").start_session()


if __name__ == "__main__":
    database = MongoConnection().get_mongo_connection()
    logger.info("Mongo connection successful, listing available collections")
    print(database.list_collection_names())