from mongo_connection import MongoConnection
from dpr_mongo import DPRMongo
from argparse import ArgumentParser
from dotenv import load_dotenv
from collections import Counter
import os
import logging
logger = logging.getLogger("qa-dpr-pp")
logger.basicConfig(level=logging.ERROR)
load_dotenv()

class QADPR:
    def __init__(self):
        self.mongo_connection = MongoConnection().get_mongo_connection()
        self.dpr_mongo = DPRMongo(self.mongo_connection)
        self.directory = None
        
        try: 
            self.directory = os.environ.get("file_dir")
        except:
            logger.error(f"Cant load environment variables from local .env file")
    
    def get_patient(self, kpmp_id: str):
        return self.dpr_mongo.find_patient_with_kpmp_id(kpmp_id)
        
    def extract_ids_from_files(self, file:str):
        kpmp_ids = []
        with open(file, 'r') as file:
            for line in file:
                kpmp_id = line.strip()
                kpmp_ids.append(kpmp_id)
        return kpmp_ids
                
        
    def get_slides(self, kpmp_id: str):
        slideNames = []
        patient = self.get_patient(kpmp_id)
        slides = patient['slides']
        for slide in slides:
            slideNames.append(slide['slideName'])
        return slideNames
    
    def list_files_in_dir(self, patient_dir:str):
        files = []
        for file in os.listdir(patient_dir):
            if file.endswith(".dzi"):
                filename = os.path.splitext(file)
                files.append(filename[0])
        return files
        
    def compare_files_with_slides(self, slides: list, files: list, kpmp_id: str):
        mismatched_ids = []
        if Counter(slides) == Counter(files):
            print("Slides in mongo match files in filesystem")
        else:
            mismatched_ids.append(kpmp_id)
        return mismatched_ids
            
    def main(self, file_location):
        kpmp_ids = self.extract_ids_from_files(file_location)
        for kpmp_id in kpmp_ids:
            slides = self.get_slides(kpmp_id)
            files = self.list_files_in_dir(os.environ['files_dir'] + kpmp_id)
            self.compare_files_with_slides(slides=slides, files=files, kpmp_id=kpmp_id)
        
    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '-f',
        '--file',
        required=True,
        help="File that has newline separated participant ids"
    )
    args = parser.parse_args()
    
    qa_dpr = QADPR()
    qa_dpr.main(args.file)
        