
# coding=utf-8
import os.path

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

from sqlalchemy.dialects.mysql import JSON

from toolz import get_in

from ... import Base
from ....enums import operation_types_enum
from ....field_handlers import amount_field
from ....field_handlers import amount_symbol_field
from ....field_handlers import comment_body_field
from ..base import BaseOperation

class InterestOperation(Base, BaseOperation):
    """
    
    
    Steem Blockchain Example
    ======================

    

    """
    
    __tablename__ = 'sbds_op_interests'
    __operation_type__ = 'interest_operation'
    
    owner = Column(JSON) # name:owner
    interest = Column(Numeric(15,6), nullable=False) # steem_type:asset
    interest_symbol = Column(String(5)) # steem_type:asset
    operation_type = Column(
        operation_types_enum,
        nullable=False,
        index=True,
        default='interest_operation')
    
    _fields = dict(
        owner=lambda x: x.get('owner'),
        interest=lambda x: amount_field(x.get('interest'), num_func=float),
        interest_symbol=lambda x: amount_symbol_field(x.get('interest')),
    )
