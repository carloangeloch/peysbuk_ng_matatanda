from sqlmodel import create_engine, SQLModel
from supabase import Client, create_client
import os
from dotenv import load_dotenv
load_dotenv()

spurl = os.getenv('SUPABASE_USERNAME')
spkey = os.getenv('SUPABASE_APIKEY')
supabase: Client = create_client(spurl, spkey)

DB_NAME=f'postgresql://postgres:{os.getenv('SUPABASE_PASSWORD')}@db.kqelyleapykawcugiwri.supabase.co:5432/postgres'
engine = create_engine(DB_NAME, echo=True)
print('Server Running . . .')

def create_table():
    SQLModel.metadata.create_all(bind=engine)
    print('Creating all model tables')


