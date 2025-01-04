import datetime
import time
from zoneinfo import ZoneInfo


def epoch_to_iso(epoch_time: datetime | int | None) -> str | None:
    if epoch_time is None:
        return None
    # end if

    if not isinstance(epoch_time, (datetime.datetime, int)):
        raise TypeError("Input must be of type datetime.datetime, int (epoch) or None")
    # end if

    if isinstance(epoch_time, int):
        # Convert epoch time to a naive datetime object
        naive_datetime = datetime.datetime.fromtimestamp(epoch_time)
    else:
        # Ensure the input is a naive datetime object
        if epoch_time.tzinfo is not None:
            raise ValueError("Input datetime must be naive (without timezone info).")
        # end if

        naive_datetime = epoch_time
    # end def

    # Get the local timezone
    local_tz = ZoneInfo(time.tzname[0])  # Get the local timezone name

    # Localize the naive datetime to the local timezone
    local_datetime = naive_datetime.replace(tzinfo=local_tz)

    # Convert to ISO 8601 format
    iso_format = local_datetime.isoformat()

    return iso_format
# end def


if __name__ == '__main__':
    # Example usage
    unix_time = 1633072800  # Example epoch time
    iso_datetime = epoch_to_iso(unix_time)
    print(f"for epoch {unix_time!r}, the ISO 8601 is {iso_datetime!r}.")
# end if
