"""Задача 3: Рефакторинг почтового скрипта в PEP8-совместимый класс.

Модуль определяет класс `GmailClient` для отправки и получения писем
по SMTP и IMAP. Вся конфигурация передаётся через конструктор
или аргументы методов — никакой хардкодной конфиденциальной информации.
"""

from __future__ import annotations

import email
import imaplib
import smtplib
import os
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable, Optional, Tuple


DEFAULT_SMTP_HOST = "smtp.gmail.com"
DEFAULT_IMAP_HOST = "imap.gmail.com"
DEFAULT_SMTP_PORT = 587


@dataclass
class GmailConfig:
    """Конфигурация клиента Gmail."""

    username: str
    password: str
    smtp_host: str = DEFAULT_SMTP_HOST
    imap_host: str = DEFAULT_IMAP_HOST
    smtp_port: int = DEFAULT_SMTP_PORT


class GmailClient:
    """Простой клиент Gmail для отправки и получения писем."""

    def __init__(self, config: GmailConfig) -> None:
        self.config = config

    def send_email(self, subject: str, message: str, recipients: Iterable[str]) -> None:
        """Отправить письмо с указанной темой и текстом получателям `recipients`."""
        msg = MIMEMultipart()
        msg["From"] = self.config.username
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(message))

        with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.config.username, self.config.password)
            smtp.sendmail(self.config.username, list(recipients), msg.as_string())

    def fetch_latest_by_header(self, header_value: Optional[str] = None) -> Tuple[bytes, email.message.Message]:
        """Получить последнее письмо, опционально отфильтрованное по заголовку Subject.

        Возвращает пару `(raw_email_bytes, parsed_email_message)`.
        Бросает AssertionError, если подходящих писем нет.
        """
        with imaplib.IMAP4_SSL(self.config.imap_host) as imap:
            imap.login(self.config.username, self.config.password)
            imap.select("inbox")
            criterion = f'(HEADER Subject "{header_value}")' if header_value else 'ALL'
            result, data = imap.uid('search', None, criterion)
            if result != 'OK' or not data or not data[0]:
                raise AssertionError('Нет писем с указанным заголовком Subject')
            latest_email_uid = data[0].split()[-1]
            result, data = imap.uid('fetch', latest_email_uid, '(RFC822)')
            if result != 'OK' or not data or not data[0]:
                raise RuntimeError('Не удалось получить письмо по UID')
            raw_email: bytes = data[0][1]
            parsed_message = email.message_from_bytes(raw_email)
            return raw_email, parsed_message


if __name__ == "__main__":
    # Безопасная инициализация через переменные окружения — чтобы не хранить
    # учётные данные в коде.
    username_env = os.getenv("GMAIL_USERNAME")
    password_env = os.getenv("GMAIL_PASSWORD")
    if username_env and password_env:
        config = GmailConfig(username=username_env, password=password_env)
        client = GmailClient(config)
        print("GmailClient инициализирован из переменных окружения.")
        # Далее можно явно вызывать методы client.send_email(...) и client.fetch_latest_by_header(...)
    else:
        print(
            "Задайте переменные окружения GMAIL_USERNAME и GMAIL_PASSWORD для инициализации GmailClient."
        )


