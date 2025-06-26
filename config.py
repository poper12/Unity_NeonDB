from dotenv import load_dotenv
import os

load_dotenv()

env_vars = {
  # Get From my.telegram.org
  "API_HASH": os.getenv("API_HASH", "7699560031"),
  # Get From my.telegram.org
  "API_ID": os.getenv("API_ID", "a184b91d39fc85265e232e7c323fac45"),
  #Get For @BotFather
  "BOT_TOKEN": os.getenv("BOT_TOKEN", ""),
  # Get For tembo.io
  "DATABASE_URL_PRIMARY": "postgresql://neondb_owner:npg_UdVNDuv71gHm@ep-icy-violet-a8q6p6us-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require",
  # Logs Channel Username Without @
  "CACHE_CHANNEL": "",
  # Force Subs Channel username without @
  "CHANNEL": "",
  # {chap_num}: Chapter Number
  # {chap_name} : Manga Name
  # Ex : Chapter {chap_num} {chap_name} @Manhwa_Arena
  "FNAME": "[CH - {chap_num}] {chap_name} @Manga_Unity"  

}
dbname = env_vars.get('DATABASE_URL_PRIMARY') or env_vars.get('DATABASE_URL') or 'sqlite:///test.db'

if dbname.startswith('postgres://'):
    dbname = dbname.replace('postgres://', 'postgresql://', 1)
    
