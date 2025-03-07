from pydantic import BaseModel


class NextNode(BaseModel):
    next_node_title: str
