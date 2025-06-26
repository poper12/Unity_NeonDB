from typing import Type, List, TypeVar, Optional, Any, Dict
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field as PydanticField
from tools import LanguageSingleton
import os

T = TypeVar("T")

# MongoDB Models using Pydantic
class ChapterFile(BaseModel):
    url: str
    file_id: Optional[str] = None
    file_unique_id: Optional[str] = None
    cbz_id: Optional[str] = None
    cbz_unique_id: Optional[str] = None
    telegraph_url: Optional[str] = None

class MangaOutput(BaseModel):
    user_id: str
    output: int

class Subscription(BaseModel):
    url: str
    user_id: str

class LastChapter(BaseModel):
    url: str
    chapter_url: str

class MangaName(BaseModel):
    url: str
    name: str

class DB(metaclass=LanguageSingleton):
    def __init__(self, dbname: str = None):
        db_url = dbname or os.environ.get('MONGODB_URI', 'mongodb+srv://userbot:userbot@cluster0.iweqz.mongodb.net/test?retryWrites=true&w=majority')
        if not (db_url.startswith('mongodb://') or db_url.startswith('mongodb+srv://')):
            db_url = 'mongodb+srv://userbot:userbot@cluster0.iweqz.mongodb.net/test?retryWrites=true&w=majority'
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client['campus']

    async def add(self, other: BaseModel):
        collection = self.db[other.__class__.__name__]
        await collection.replace_one({'url': getattr(other, 'url', None) or getattr(other, 'user_id', None)}, other.dict(), upsert=True)

    async def get(self, model: Type[T], id: Any) -> Optional[T]:
        collection = self.db[model.__name__]
        if isinstance(id, tuple):
            query = {k: v for k, v in zip(model.__fields__, id)}
        else:
            # Try url or user_id
            if hasattr(model, 'url'):
                query = {'url': id}
            else:
                query = {'user_id': id}
        doc = await collection.find_one(query)
        return model(**doc) if doc else None

    async def get_all(self, model: Type[T]) -> List[T]:
        collection = self.db[model.__name__]
        docs = collection.find()
        return [model(**doc) async for doc in docs]

    async def erase(self, other: BaseModel):
        collection = self.db[other.__class__.__name__]
        await collection.delete_one({'url': getattr(other, 'url', None) or getattr(other, 'user_id', None)})

    async def get_chapter_file_by_id(self, id: str):
        collection = self.db['ChapterFile']
        doc = await collection.find_one({
            '$or': [
                {'file_unique_id': id},
                {'cbz_unique_id': id},
                {'telegraph_url': id}
            ]
        })
        return ChapterFile(**doc) if doc else None

    async def get_subs(self, user_id: str, filters=None) -> List[MangaName]:
        # Find all subscriptions for user_id, then get MangaName for each url
        sub_collection = self.db['Subscription']
        manga_collection = self.db['MangaName']
        subs = sub_collection.find({'user_id': user_id})
        urls = [sub['url'] async for sub in subs]
        query = {'url': {'$in': urls}}
        if filters:
            query['$or'] = [
                {'name': {'$regex': f, '$options': 'i'}} for f in filters
            ] + [
                {'url': {'$regex': f, '$options': 'i'}} for f in filters
            ]
        mangas = manga_collection.find(query)
        return [MangaName(**doc) async for doc in mangas]

    async def erase_subs(self, user_id: str):
        collection = self.db['Subscription']
        await collection.delete_many({'user_id': user_id})
