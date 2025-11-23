"""Geffe generator ID value object."""

from typing import NewType
from uuid import UUID

GeffeGeneratorID = NewType("GeffeGeneratorID", UUID)

