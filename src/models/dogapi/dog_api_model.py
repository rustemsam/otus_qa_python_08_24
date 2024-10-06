from typing import Dict, List

from pydantic import BaseModel, Field, HttpUrl


class DogRandomImageApiResponse(BaseModel):
    message: str = Field(strict=True)
    status: str = Field(strict=True)


class DogBreedsApiResponse(BaseModel):
    message: Dict[str, List[str]] = Field(...)
    status: str = Field(strict=True)


class DogImagesResponse(BaseModel):
    message: List[HttpUrl] = Field(...)
    status: str = Field(strict=True)


class DogBreedListResponse(BaseModel):
    message: List[str] = Field(...)
    status: str = Field(strict=True)
