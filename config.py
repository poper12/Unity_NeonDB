from dotenv import load_dotenv
import os

load_dotenv()

env_vars = {
  # Get From my.telegram.org
  "API_HASH": os.getenv("API_HASH", ""),
  # Get From my.telegram.org
  "API_ID": os.getenv("API_ID", ""),
  #Get For @BotFather
  "BOT_TOKEN": os.getenv("BOT_TOKEN", ""),
  # Get For tembo.io
  "DATABASE_URL_PRIMARY": "postgresql://neondb_owner:npg_NoDFHanE76qR@ep-twilight-fire-a80mx792-pooler.eastus2.azure.neon.tech/neondb?sslmode=require",
  # Logs Channel Username Without @
  "CACHE_CHANNEL": "Dump2075",
  # Force Subs Channel username without @
  "CHANNEL": "",
  # {chap_num}: Chapter Number
  # {chap_name} : Manga Name
  # Ex : Chapter {chap_num} {chap_name} @Manhwa_Arena
  "FNAME": "[MC] [{chap_num}] {chap_name} @Manga_Campus"  

}
dbname = env_vars.get('DATABASE_URL_PRIMARY') or env_vars.get('DATABASE_URL') or 'sqlite:///test.db'

if dbname.startswith('postgres://'):
    dbname = dbname.replace('postgres://', 'postgresql://', 1)
    
