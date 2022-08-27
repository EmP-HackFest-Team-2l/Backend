from datetime import datetime
from bson.objectid import ObjectId

class Message:
    def __init__(self, message_dict):
        self.title: str = message_dict.get("title")
        self.content: str = message_dict.get("content")
        self.read: bool = message_dict.get("read")
        self.favorite: bool = message_dict.get("favorite")
        self.tags: list[str] = message_dict.get("tags")
        self.recipient: str  = message_dict.get("recipient")
        self.sender: str | None = message_dict.get("sender")
        self.send_time: datetime = message_dict.get("send_time") 
    
    def validate(self, validate_send_time=False) -> str:
        if not self.title:
            return "`title` is not set."
        elif not isinstance(self.title, str):
            return "`title` is not a string."

        elif self.content is not None and not isinstance(self.content, str):
            return "`content` is not a string."

        elif self.read is None:
            return "`read` is not set."
        elif not isinstance(self.read, bool):
            return "`read` is not a boolean."

        elif self.favorite is None:
            return "`favorite` is not set."
        elif not isinstance(self.favorite, bool):
            return "`favorite` is not a boolean."

        elif self.tags is None:
            return "`tags` is not set."
        elif not isinstance(self.tags, list) \
            or not all([isinstance(item, str) for item in self.tags]):
            return "`tags` is not an array of strings."

        elif not self.recipient:
            return "`recipient` is not set."
        elif not isinstance(self.recipient, ObjectId):
            try:
                ObjectId(self.recipient)
            except Exception as ex:
                print(ex)
                return "`recipient` is not an ObjectId."

        elif self.sender is not None and not isinstance(self.sender, ObjectId):
            try:
                ObjectId(self.sender)
            except:
                return "`sender` is not an ObjectId."

        elif validate_send_time and not self.send_time:
            return "`send_time` is not set."
        elif validate_send_time and not isinstance(self.send_time, datetime):
            return "`send_time` is not a datetime."