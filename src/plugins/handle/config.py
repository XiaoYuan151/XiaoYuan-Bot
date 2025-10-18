from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    handle_message: bool = True
