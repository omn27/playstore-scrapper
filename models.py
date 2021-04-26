import db
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime


class Links(db.Base):
    __tablename__ = "Links"
    id = Column(Integer, primary_key=True)
    packet_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    email_isAvailable = Column(Boolean, nullable=True)
    account_in_AndroidDeveloper = Column(Boolean, nullable=True)
    dork = Column(String, nullable=True)

    def __init__(
        self,
        packet_name,
        email=None,
        estado_email=None,
        cuenta_en_android_developer=None,
        dork=None,
    ):
        self.packet_name = packet_name
        self.email = email
        self.estado_email = estado_email
        self.cuenta_en_android_developer = cuenta_en_android_developer
        self.dork = dork

    def __str__(self):
        return self.id + self.packet_name + self.email + self.estado_email