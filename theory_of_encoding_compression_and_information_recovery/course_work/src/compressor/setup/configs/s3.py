from pydantic import BaseModel, Field


class S3Config(BaseModel):
    host: str = Field(..., alias="AWS_HOST")
    port: int = Field(..., alias="AWS_PORT")
    aws_access_key_id: str = Field(..., alias="AWS_ACCESS_KEY_ID", description="User ID for AWS")
    aws_secret_access_key: str = Field(..., alias="AWS_SECRET_ACCESS_KEY", description="User password for AWS")
    signature_version: str = "s3v4"
    region_name: str = "us-east-1"

    @property
    def uri(self) -> str:
        return f"http://{self.host}:{self.port}"
