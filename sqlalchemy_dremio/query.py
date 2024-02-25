from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from sqlalchemy import types

import pyarrow as pa
from pyarrow import flight

# We're converting Arrow to a Pandas dataframe below, so we need to cover all supported pandas data types here. 
# See: https://arrow.apache.org/docs/python/pandas.html#arrow-pandas-conversion
# TODO (LJ): If we remove the conversion to pandas df we can switch to using native arrow types.
_type_map = {
    'bool': types.Boolean(),
    'int8': types.SmallInteger(),
    'byte': types.SmallInteger(),
    'int16': types.Integer(),
    'int32': types.Integer(),
    'int64': types.BigInteger(),
    'float32': types.Float(precision=32),
    'float64': types.Float(precision=64),
    'string': types.String(),
    'object': types.String(),
    'datetime64[ns]': types.DATETIME,

    # GH-33321: https://github.com/apache/arrow/pull/35656 - Support converting to non-nano datetime64 for pandas >= 2.0 
    'datetime64[ms]': types.DATETIME,
    'datetime64[s]': types.DATETIME,
    'datetime64[us]': types.DATETIME,

    #TODO (LJ): Handle unsigned integers?
    #TODO (LJ): Handle timestamp with timezone?
}

def run_query(query, flightclient=None, options=None):
    info = flightclient.get_flight_info(flight.FlightDescriptor.for_command(query), options)
    reader = flightclient.do_get(info.endpoints[0].ticket, options)

    batches = []
    while True:
        try:
            batch, metadata = reader.read_chunk()
            batches.append(batch)
        except StopIteration:
            break

    data = pa.Table.from_batches(batches)
    
    # TODO (LJ): Remove conversion to pandas dataframe?
    df = data.to_pandas(date_as_object=False)

    return df


def execute(query, flightclient=None, options=None):
    df = run_query(query, flightclient, options)

    result = []

    for x, y in df.dtypes.to_dict().items():
        o = (x, _type_map[str(y.name)], None, None, True)
        result.append(o)

    return df.values.tolist(), result
