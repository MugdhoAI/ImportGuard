"""Strict Pydantic models shared by routes, recipes, and model proposals."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

FieldType = Literal["string", "integer", "decimal", "boolean", "date_iso"]
Operation = Literal["identity", "trim", "collapse_whitespace", "lowercase", "uppercase"]


class TargetField(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=80)
    type: FieldType = "string"
    required: bool = True

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value or value.startswith("_"):
            raise ValueError("Field names must be non-empty and cannot start with underscore")
        return value


class MappingEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_column: str | None
    target_field: str
    operation: Operation = "identity"
    confidence: Literal["high", "medium", "low"] | None = None
    needs_review: bool = True
    note: str = Field(default="", max_length=240)


class Recipe(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    version: Literal[1] = 1
    schema_fields: list[TargetField] = Field(alias="schema")
    mappings: list[MappingEntry]


class Proposal(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mappings: list[MappingEntry]
