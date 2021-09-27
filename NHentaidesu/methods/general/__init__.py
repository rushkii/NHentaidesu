from .new import NewDoujin
from .user import GetUser
from .tags import GetTagInfo
from .search import DoujinSearch

class General(
    NewDoujin,
    GetUser,
    GetTagInfo,
    DoujinSearch
):
    pass