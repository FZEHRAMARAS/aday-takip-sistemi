import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL ve SUPABASE_ANON_KEY .env dosyasında tanımlı olmalı.")
    return create_client(url, key)


def sign_in(email: str, password: str):
    client = get_client()
    return client.auth.sign_in_with_password({"email": email, "password": password})
