class CryptoScanner:
    def scan_path(self, path: str):
        # Mock scanner implementation for testing paths
        return [
            {"primitive": "RSA-2048", "file_path": f"{path}/sample.py", "line_number": 5}
        ]
