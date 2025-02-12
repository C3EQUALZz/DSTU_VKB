from pydantic import BaseModel, Field


class MathExpressionRequestSchema(BaseModel):
    expression: str = Field(
        pattern=r'^[\(\)0-9+\-*/^]+$',
        description="Math expression."
                    "Examples:\n"
                    "1. 9+2*3/7-8 (mod 11)\n"
                    "2. 1/5+2*13-1/14 (mod 17)\n"
                    "3. 5^3+2*13-1/14 (mod 17)"
    )
    mod: int = Field(gt=0)
