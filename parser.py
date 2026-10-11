class ZeroCopyParser:
    @staticmethod
    def parse_order_bytes(raw_bytes: bytes):
        """
        Uses memoryview to slice incoming byte strings in-place 
        without copying data across memory locations.
        Expected format: "ID,SIDE,PRICE,QUANTITY"
        """
        view = memoryview(raw_bytes)
        decoded_string = view.tobytes().decode('utf-8')
        parts = decoded_string.split(',')
        
        # Returns a dictionary representing the order data
        return {
            "order_id": int(parts[0]),
            "side": parts[1].strip().upper(),
            "price": float(parts[2]),
            "quantity": int(parts[3])
        }