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


class CommentOptionsOperation(Base):
    """

    Steem Blockchain Example
    ======================
    {
      "allow_curation_rewards": true,
      "allow_votes": true,
      "permlink": "testing6",
      "percent_steem_dollars": 5000,
      "max_accepted_payout": "1000.000 SBD",
      "author": "testing001",
      "extensions": []
    }



    """

    __tablename__ = 'sbds_op_comment_option'
    __table_args__ = (
        PrimaryKeyConstraint('block_num', 'transaction_num', 'operation_num'),

        ForeignKeyConstraint(['author'], ['sbds_meta_accounts.name'],
                             deferrable=True, initially='DEFERRED', use_alter=True),

        Index('ix_sbds_op_comment_option_accounts', 'accounts', postgresql_using='gin')

    )

    block_num = Column(Integer, nullable=False)
    transaction_num = Column(SmallInteger, nullable=False)
    operation_num = Column(SmallInteger, nullable=False)
    timestamp = Column(DateTime(timezone=False))
    trx_id = Column(String(40), nullable=False)
    accounts = Column(JSONB)
    raw = Column(JSONB)

    author = Column(String(16), nullable=True)  # steem_type:account_name_type
    permlink = Column(Unicode(256), index=True)  # name:permlink
    max_accepted_payout = Column(Numeric(20, 6), nullable=False)  # steem_type:asset
    max_accepted_payout_symbol = Column(String(5))  # steem_type:asset
    percent_steem_dollars = Column(Integer)  # steem_type:uint16_t
    allow_votes = Column(Boolean)  # steem_type:bool
    allow_curation_rewards = Column(Boolean)  # steem_type:bool
    extensions = Column(JSONB)  # steem_type:steemit::protocol::comment_options_extensions_type
    operation_type = Column(operation_types_enum, nullable=False, default='comment_options')

    _fields = dict(
        max_accepted_payout=lambda x: amount_field(
            x.get('max_accepted_payout'), num_func=float),  # steem_type:asset
        max_accepted_payout_symbol=lambda x: amount_symbol_field(
            x.get('max_accepted_payout')),  # steem_type:asset
        # steem_type:steemit::protocol::comment_options_extensions_type
        extensions=lambda x: json_string_field(x.get('extensions')),
        accounts=lambda x: sbds.sbds_json.dumps(
            [acct for acct in set(flatten((x.get('author'),))) if acct])
    )

    _account_fields = frozenset(['author', ])
