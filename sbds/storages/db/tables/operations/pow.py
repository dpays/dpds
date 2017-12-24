# coding=utf-8

import os.path


from sqlalchemy import Column, Unicode, Enum

from ...field_handlers import amount_field
from ...enums import operation_types_enum
from .. import Base
from .base import BaseOperation



class PowOperation(Base, BaseOperation):
    """Raw Format
    ==========

    op_type=='pow'
    ==============
    {
        "ref_block_prefix": 2181793527,
        "expiration": "2016-03-24T18:00:21",
        "operations": [
            [
                "pow",
                {
                    "props": {
                        "account_creation_fee": "100.000 STEEM",
                        "sbd_interest_rate": 1000,
                        "maximum_block_size": 131072
                    },
                    "work": {
                        "signature": "202f30b355f4bfe501292d3c3d650de105a1d7053fcefe875a286e79d3e886e7b005e97255b81f4c35e0ca1ad8e9acc4a57d694828231e57ae7e408e8a2f858a99",
                        "work": "0031b16c3007c425f72c1c32359511fb89ede9980ac807b81f5ab8e5edcce345",
                        "input": "8a023b6abb7e241ad41594fb0a22afb6832e4c4d68bae99707e20bfc8679b8e6",
                        "worker": "STM5gzvDurFRmVUUs38TDtTtGVAEz8TcWMt4xLVbxwP2PP8b9q7P4"
                    },
                    "nonce": 326,
                    "block_id": "00000449f7860b82b4fbe2f317c670e9f01d6d9a",
                    "worker_account": "nxt6"
                }
            ]
        ],
        "signatures": [],
        "ref_block_num": 1097,
        "extensions": []
    }


    Args:

    Returns:

    """

    __tablename__ = 'sbds_op_pows'
    __operation_type__ = os.path.splitext(os.path.basename(__file__))[0]

    worker_account = Column(Unicode(50), nullable=False, index=True)
    block_id = Column(Unicode(40), nullable=False)

    _fields = dict(
        worker_account=lambda x: x.get('worker_account'),
        block_id=lambda x: x.get('block_id')
    )

    operation_type = Column(operation_types_enum, nullable=False, index=True, default=__operation_type__)

