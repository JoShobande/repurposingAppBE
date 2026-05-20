from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

response = supabase.auth.sign_in_with_password({
    "email": "shobande.josephin@gmail.com",
    "password": "password"
})

print(response.session.access_token)