from dataclasses import dataclass


@dataclass
class PageObject:
    """Defines the data a Page needs to contain, before rendering."""
    content: str
    title: str
    metadata: dict
    slug: str


@dataclass
class PostObject(PageObject):
    """Extends the PageObject with certain aspects only necessary for post rendering."""
    date: str
