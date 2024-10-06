from typing import List, Optional, Union

from pydantic import BaseModel, RootModel


class ResourceRequestIdResponse(BaseModel):
    id: int
    project_tasks_resource_id: int
    volume: str
    cost: str
    batch_number: Optional[Union[str, int]] = None
    batch_parent_request_id: Optional[int] = None
    is_over_budget: bool
    created_at: int | str
    updated_at: int
    user_id: int
    needed_at: int
    created_by: int


class ListResourceRequestsResponse(RootModel[List[ResourceRequestIdResponse]]):
    pass


class ResourceRequestErrorResponse(BaseModel):
    name: str
    message: str
    code: int
    status: int


class ResourceRequestPostErrorResponse(BaseModel):
    field: str
    message: str


class ListResourceRequestPostErrorResponse(
    RootModel[List[ResourceRequestPostErrorResponse]]
):
    pass
