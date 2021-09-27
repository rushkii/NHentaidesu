from NHentaidesu import types
from NHentaidesu.scaffold import Scaffold

from datetime import datetime
from typing import List

class GetComments(Scaffold):
    async def get_comments(self, book_id: int) -> List["types.DoujinComments"]:
        result = await self.request_api(f"/gallery/{book_id}/comments")

        comments = types.List()
        
        for res in result:
            comment = types.DoujinComments._parse(
                self,
                id=res['id'],
                gallery_id=res['gallery_id'],
                user=types.GetUser._parse(
                    self,
                    id=res['poster']['id'],
                    username=res['poster']['username'],
                    slug=res['poster']['slug'],
                    avatar=res['poster']['avatar_url'],
                    is_superuser=res['poster']['is_superuser'],
                    is_staff=res['poster']['is_staff'],
                ),
                post_date=datetime.fromtimestamp(res['post_date']),
                text=res['body']
            )
            comments.append(comment)

        return comments

    async def flag_comment(self, comment_id: int, reason: str) -> bool:
        await self.request_api(
            f"/comments/{comment_id}/flag",
            method="POST",
            json={'reason': reason}
        )
        return True

    async def delete_comment(self, comment_id: int) -> bool:
        await self.request_api(
            f"/comments/{comment_id}/delete",
            method="POST"
        )
        return True

    # DEPRECATED, NHENTAI USING RECAPTCHA
    # async def submit_comment(self, book_id: int, text: str):
    #     result = await self.request_api(
    #         f"/comments/{book_id}/delete",
    #         method="POST",
    #         data=text
    #     )
    #     return result
