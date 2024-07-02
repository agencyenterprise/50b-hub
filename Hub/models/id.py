from pydantic import Field
from bson import ObjectId
from typing import Annotated

Id = Annotated[ObjectId | None, Field(is_required=False)]