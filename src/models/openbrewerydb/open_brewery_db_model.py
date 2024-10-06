from typing import List, Optional

from pydantic import BaseModel, Field, RootModel


class SingleBreweryResponse(BaseModel):
    id: str = Field(strict=True)
    name: str = Field(strict=True)
    brewery_type: str = Field(strict=True)
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    city: str = Field(strict=True)
    state_province: str = Field(strict=True)
    postal_code: str = Field(strict=True)
    country: str = Field(strict=True)
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None
    state: str = Field(strict=True)
    street: Optional[str] = None


class SingleBreweryErrorResponse(BaseModel):
    message: str = Field(strict=True)


class MetaBreweryResponse(BaseModel):
    total: str = Field(strict=True)
    page: str = Field(strict=True)
    per_page: str = Field(strict=True)


class ListBreweriesResponse(RootModel[List[SingleBreweryResponse]]):
    pass
