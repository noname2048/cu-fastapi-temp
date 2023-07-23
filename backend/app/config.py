import os
from datetime import datetime

import requests
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings.sources import PydanticBaseSettingsSource
from pytz import timezone


class Settings(BaseSettings):
    version: str = "invalid"
    backend_env: str = Field("local", pattern=r"^(local|dev|stage|prod)$")
    start_at: str = Field(
        default_factory=lambda: datetime.now(tz=timezone("Asia/Seoul")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    timezone: str = "Asia/Seoul"
    slack_webhook_url: str = "invalid"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,  # /run/secrets
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,  # os.environ
            dotenv_settings,  # .env
            init_settings,  # init
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def send_deployment_success_to_slack():
    event_at = datetime.now(tz=timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")
    _ = requests.post(
        url="https://hooks.slack.com/services/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",
        json={
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":white_check_mark: 새로운 서버가 시작되었습니다.",
                    },
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"*일시:* {event_at} | *버전*: {settings.version} | *환경*: {settings.backend_env}",
                        },
                    ],
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🏠 *INDEX* | https://cu.noname2048.com",
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "바로가기",
                            "emoji": True,
                        },
                        "url": "https://cu.noname2048.com",
                        "value": "go_to_index",
                        "action_id": "go_to_index",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🚀 *API 문서* | https://cu.noname2048.com/docs",
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "바로가기",
                            "emoji": True,
                        },
                        "url": "https://cu.noname2048.com/docs",
                        "value": "go_to_docs",
                        "action_id": "go_to_docs",
                    },
                },
            ],
        },
    )
