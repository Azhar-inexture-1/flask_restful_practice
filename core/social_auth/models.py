from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer


class OAuthMixin:
    id = Column(Integer, primary_key=True)
    provider = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    account_id = Column(String, nullable=True)
    email = Column(String, nullable=True)
