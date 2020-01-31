import asyncio
import motor.motor_asyncio
from umongo import Instance, Document, fields

db = motor.motor_asyncio.AsyncIOMotorClient('mongodb', 27017)['db']
instance = Instance(db)


@instance.register
class SuccessPage(Document):
    """
      This class maps to the collection in MongoDB where
      we will store the pages with status 200
    """
    url = fields.StrField(attribute='url')
    title = fields.StrField(attribute='title')
    text = fields.StrField(attribute='text')


@instance.register
class ErrorPage(Document):
    """
      This class maps to the collection in MongoDB where
      we will store the pages that gave an error
    """
    url = fields.StrField(attribute='url')
    status = fields.StrField(attribute='status')


class WebpageStore:
    """
      The responsibility of this class is to store the
      responses of the URL requests in MongoDB.
    """
    async def store_success_page(self, url, title, text):
        page = SuccessPage(url=url, title=title, text=text)
        await page.commit()

    async def store_error_page(self, url, status):
        page = ErrorPage(url=url, status=str(status))
        await page.commit()
