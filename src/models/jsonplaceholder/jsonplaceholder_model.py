from typing import List

from pydantic import BaseModel, Field, RootModel


class PostsRequestBody(BaseModel):
    title: str
    body: str
    userId: int


class PostsResponseBody(BaseModel):
    id: int = Field(strict=True)
    title: str = Field(strict=True)
    body: str = Field(strict=True)
    userId: int = Field(strict=True)


class ListPostsResponse(RootModel[List[PostsResponseBody]]):
    pass
