import os
from dotenv import load_dotenv

load_dotenv()

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
PROJECT_ID = os.getenv("PROJECT_ID")


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/mefathimtech-43/Desktop/Yossi/Visualize My Space/Visualize_My_Space_Server/mywebsite-444109-4abaee7171b1.json"
