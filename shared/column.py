
from sqlalchemy import DateTime
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator

import datetime
from typing import Optional


class DateTimeUTC(TypeDecorator[datetime.datetime]):
    '''
    A custom column type for storage that treats all datetime instances as UTC timestamps
    This will treat any "naive" datetime objects as implicitly UTC and convert any "aware"
    objects into UTC.

    Almost a carbon-copy of this implementation:
    https://github.com/litestar-org/advanced-alchemy/blob/main/advanced_alchemy/types/datetime.py

    For further info, see:
    https://github.com/fastapi/sqlmodel/issues/539
    https://stackoverflow.com/questions/78767971/why-does-timezone-not-work-in-sqlmodel
    https://www.reddit.com/r/flask/comments/1im57ij/sqlalchemy_is_driving_me_nuts/
    '''

    # Class level property: specifies the underlying implementation
    impl = DateTime(timezone=True)

    # Class level property: allow this value to tbe cached
    cache_ok = True


    @property
    def python_type(self) -> type[datetime.datetime]:
        return datetime.datetime


    def process_bind_param(
        self,
        value: Optional[datetime.datetime],
        dialect: Dialect
    ) -> Optional[datetime.datetime]:
        if value is None:
            return value
        else:
            return value.astimezone(datetime.timezone.utc)


    def process_result_value(
        self,
        value: Optional[datetime.datetime],
        dialect: Dialect
    ) -> Optional[datetime.datetime]:
        if value is None:
            return value
        elif value.tzinfo is None:
            return value.replace(tzinfo=datetime.timezone.utc)
        else:
            return value

