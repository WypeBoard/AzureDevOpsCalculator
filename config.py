from pydantic import BaseSettings, Field

class CoreSettings(BaseSettings):
    mail_domain: str = Field(default="")
    mail_send_enabled: bool = Field(default=False)
    
    class Config:
        env_file = ".env"
        env_prefix = "CORE_"
        case_sensitive = False

    
class AdoSettings(BaseSettings):
    token: str = Field(default="")
    base_url: str = Field(default="")
    organisation: str = Field(default="")
    project_name: str = Field(default="")
    repository_name: str = Field(default="")
    
    class Config:
        env_file = ".env"
        env_prefix = "ADO_"
        case_sensitive = False


class CalculationSettings(BaseSettings):
    pull_request_id: str = Field(default="id")
    pull_request_title: str = Field(default="title")
    pull_request_creator_id: str = Field(default="creator_id")
    pull_request_creator: str = Field(default="creator")
    pull_request_email: str = Field(default="email")
    pull_request_url: str = Field(default="url")
    pull_request_violation: str = Field(default="violation")

    class Config:
        env_file = ".env"
        env_prefix = "CALCULATION_"
        case_sensitive = False
        
class Settings:
    def __init__(self):
        self.CoreSettings = CoreSettings()
        self.CalculationSettings = CalculationSettings()
        self.AdoSettings = AdoSettings()