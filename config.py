# ChronosMatch - Week 1 Configuration

BUFFER_CAPACITY = 464

# Number of orders to generate in a test run.
TOTAL_ORDERS = 500_000

# Number of orders generated in each batch.
BATCH_SIZE = 1000

# Size of the memory-mapped buffer in bytes.
HEADER_SIZE = 16

# Each order:
# Order ID: unsigned 64-bit integer
# Price: unsigned 64-bit integer (price in paise)
# Quantity: unsigned 32-bit integer
#
# Format: <QQI
ORDER_FORMAT = "<QQI"

import struct

ORDER_SIZE = struct.calcsize(ORDER_FORMAT)

BUFFER_SIZE = HEADER_SIZE + BUFFER_CAPACITY * ORDER_SIZE