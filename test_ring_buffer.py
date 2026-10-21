
from ring_buffer import RingBuffer


def test_invalid_orders():
    buffer = RingBuffer()

    try:
        invalid_orders = [
            (0, 100000, 1),
            (1, 0, 1),
            (1, 100000, 0),
            (True, 100000, 1),
        ]

        for order in invalid_orders:
            try:
                buffer.write_order(*order)
            except ValueError:
                print(f"PASS: Rejected invalid order {order}")
            else:
                print(f"FAIL: Accepted invalid order {order}")

    finally:
        buffer.close()


if __name__ == "__main__":
    test_invalid_orders()
