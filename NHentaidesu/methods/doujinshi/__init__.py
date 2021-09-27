from .info import DoujinInfo
from .related import GetRelated
from .comments import GetComments

class Doujinshi(
    DoujinInfo,
    GetRelated,
    GetComments
):
    pass