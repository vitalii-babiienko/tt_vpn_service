def convert_bytes_to_megabytes(bytes_value: int = 0) -> float:
    return round(bytes_value / (1024 * 1024), 4)
