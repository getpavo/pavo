from dataclasses import dataclass


@dataclass
class Page:
    """Defines the data a Page needs to contain, before rendering."""

    content: str
    title: str
    metadata: dict
    slug: str


@dataclass
class Post(Page):
    """Extends the PageObject with certain aspects only necessary for post rendering."""

    date: str
