from mongo_connection import MongoConnection
from bson.codec_options import CodecOptions

class DPRMongo:
    def __init__(self, mongo_connection: MongoConnection):
        self.patients_collection = mongo_connection.patients.with_options(codec_options=CodecOptions(tz_aware=True))
        
    def find_patient_with_kpmp_id(self, kpmp_id: str):
        return self.patients_collection.find_one({"kpmp_id": kpmp_id})
    
    def find_all_patients(self): 
        return self.patients_collection.find({}, no_cursor_timeout=True, batch_size=1)
    
    