from datetime import datetime

from sqlalchemy import create_engine, String, DateTime
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import DATABASE_URL

Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True)
    partner_id = Column(Integer)
    order_id = Column(Integer)
    contractor_id = Column(Integer)

    sender_id = Column(Integer)
    text = Column(String)
    created = Column(DateTime)

    def __init__(self, *args):
        super().__init__(*args)
        self.created = datetime.now()

    def __repr__(self):
        return "Message ID: {0}\nOrder ID: {1}\nPartner ID: {2}\nContractor ID: {3}".format(
            self.message_id, self.order_id, self.partner_id, self.contractor_id,
        )

    def to_json(self):
        return {
            'message_id': self.message_id,
            'sender_id': self.sender_id,
            'text': self.text,
            'created': datetime.isoformat(self.created),
        }


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
