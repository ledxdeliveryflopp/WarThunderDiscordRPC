from datetime import datetime

from pydantic import BaseModel, RootModel


class ReleaseAuthorSchemas(BaseModel):

    login: str
    avatar_url: str
    html_url: str


class ReleaseAssetSchemas(BaseModel):

    url: str
    id: int
    name: str
    content_type: str
    size: int | float
    digest: str
    download_count: int
    browser_download_url: str


class ReleaseSchemas(BaseModel):
    url: str
    assets_url: str
    upload_url: str
    html_url: str
    id: int
    author: ReleaseAuthorSchemas
    tag_name: str
    name: str
    prerelease: bool
    created_at: datetime
    updated_at: datetime
    assets: list[ReleaseAssetSchemas]
    body: str
