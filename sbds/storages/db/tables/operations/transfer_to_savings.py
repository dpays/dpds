# -*- coding: utf-8 -*-
import dateutil.parser

from funcy import flatten
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Numeric
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import Boolean
from sqlalchemy import SmallInteger
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB

import sbds.sbds_json

from ..import Base
from ...enums import operation_types_enum
from ...field_handlers import json_string_field
from ...field_handlers import amount_field
from ...field_handlers import amount_symbol_field
from ...field_handlers import comment_body_field


class TransferToSavingsOperation(Base):
    """

    Steem Blockchain Example
    ======================
    {
      "from": "abit",
      "to": "abit",
      "amount": "1.000 SBD",
      "memo": ""
    }



    """

    __tablename__ = 'sbds_op_transfer_to_saving'
    __table_args__ = (
        PrimaryKeyConstraint('block_num', 'transaction_num', 'operation_num'),

        ForeignKeyConstraint(['from'], ['sbds_meta_accounts.name'],
                             deferrable=True, initially='DEFERRED', use_alter=True),



        ForeignKeyConstraint(['to'], ['sbds_meta_accounts.name'],
                             deferrable=True, initially='DEFERRED', use_alter=True),

        Index('ix_sbds_op_transfer_to_saving_accounts', 'accounts', postgresql_using='gin')

    )

    block_num = Column(Integer, nullable=False)
    transaction_num = Column(SmallInteger, nullable=False)
    operation_num = Column(SmallInteger, nullable=False)
    timestamp = Column(DateTime(timezone=False))
    trx_id = Column(String(40), nullable=False)
    accounts = Column(JSONB)
    raw = Column(JSONB)

    _from = Column('from', String(16))  # name:from
    to = Column(String(16), nullable=True)  # steem_type:account_name_type
    amount = Column(Numeric(20, 6), nullable=False)  # steem_type:asset
    amount_symbol = Column(String(5))  # steem_type:asset
    memo = Column(UnicodeText)  # name:memo
    operation_type = Column(operation_types_enum, nullable=False, default='transfer_to_savings')

    _fields = dict(
        amount=lambda x: amount_field(x.get('amount'), num_func=float),  # steem_type:asset
        amount_symbol=lambda x: amount_symbol_field(x.get('amount')),  # steem_type:asset
        accounts=lambda x: sbds.sbds_json.dumps(
            [acct for acct in set(flatten((x.get('from'), x.get('to'),))) if acct])
    )

    _account_fields = frozenset(['from', 'to', ])
