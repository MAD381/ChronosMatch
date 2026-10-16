
import mmap
import struct

from config import (
    BUFFER_CAPACITY,
    BUFFER_SIZE,
    HEADER_SIZE,
    ORDER_FORMAT,
    ORDER_SIZE,
)


class RingBuffer:
    """Memory-mapped ring buffer for storing trading orders."""

    WRITE_POSITION_OFFSET = 0
    READ_POSITION_OFFSET = 8

    def __init__(self, filename="chronosmatch_buffer.dat"):
        if BUFFER_CAPACITY <= 0:
            raise ValueError("BUFFER_CAPACITY must be positive")

        self.filename = filename
        self.capacity = BUFFER_CAPACITY
        self.order_size = ORDER_SIZE

        self.file = open(filename, "w+b")
        self.file.truncate(BUFFER_SIZE)

        self.memory = mmap.mmap(
            self.file.fileno(),
            BUFFER_SIZE,
            access=mmap.ACCESS_WRITE,
        )

        self.write_position = 0
        self.read_position = 0
        self.count = 0

        struct.pack_into(
            "<Q", self.memory, self.WRITE_POSITION_OFFSET, 0
        )
        struct.pack_into(
            "<Q", self.memory, self.READ_POSITION_OFFSET, 0
        )

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count >= self.capacity

    def write_order(self, order_id, price_paise, quantity):
        """Write an order. Return False if the buffer is full."""

        if (
            not isinstance(order_id, int)
            or not isinstance(price_paise, int)
            or not isinstance(quantity, int)
            or order_id <= 0
            or price_paise <= 0
            or quantity <= 0
        ):
            raise ValueError(
                "Order ID, price, and quantity must be positive integers"
            )

        if self.is_full():
            return False

        index = self.write_position % self.capacity
        offset = HEADER_SIZE + index * self.order_size

        struct.pack_into(
            ORDER_FORMAT,
            self.memory,
            offset,
            order_id,
            price_paise,
            quantity,
        )

        self.write_position += 1
        self.count += 1

        struct.pack_into(
            "<Q",
            self.memory,
            self.WRITE_POSITION_OFFSET,
            self.write_position,
        )

        return True

    def read_order(self):
        """Read the next order. Return None if the buffer is empty."""

        if self.is_empty():
            return None

        index = self.read_position % self.capacity
        offset = HEADER_SIZE + index * self.order_size

        order_id, price_paise, quantity = struct.unpack_from(
            ORDER_FORMAT,
            self.memory,
            offset,
        )

        self.read_position += 1
        self.count -= 1

        struct.pack_into(
            "<Q",
            self.memory,
            self.READ_POSITION_OFFSET,
            self.read_position,
        )

        return {
            "order_id": order_id,
            "price_paise": price_paise,
            "quantity": quantity,
        }

    def close(self):
        """Close the memory map and backing file."""

        if not self.memory.closed:
            self.memory.close()

        if not self.file.closed:
            self.file.close()
