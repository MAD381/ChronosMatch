import mmap
import os
import struct

from config import (
    BUFFER_CAPACITY,
    BUFFER_SIZE,
    HEADER_SIZE,
    ORDER_FORMAT,
    ORDER_SIZE,
)


class RingBuffer:
    """
    Memory-mapped ring buffer for ChronosMatch.

    Stores orders in binary form using mmap and struct.
    The producer and consumer share the same mapped file.
    """

    WRITE_POSITION_OFFSET = 0
    READ_POSITION_OFFSET = 8

    def __init__(self, filename="chronosmatch_buffer.dat"):
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

        # Header:
        # First 8 bytes  = write position
        # Next 8 bytes   = read position
        struct.pack_into(
            "<Q",
            self.memory,
            self.WRITE_POSITION_OFFSET,
            0,
        )

        struct.pack_into(
            "<Q",
            self.memory,
            self.READ_POSITION_OFFSET,
            0,
        )

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count >= self.capacity

    def write_order(self, order_id, price_paise, quantity):
        """
        Write an order to the ring buffer.

        Returns True if the order was written.
        Returns False if the buffer is full.
        """

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
        """
        Read the next order from the ring buffer.

        Returns a dictionary or None if the buffer is empty.
        """

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
        """Close the memory map and its backing file."""

        self.memory.close()
        self.file.close()