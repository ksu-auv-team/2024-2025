def map(x : float, in_min : float, in_max : float, out_min : float, out_max : float) -> float:
    # Map a value from one range to another
    return round((x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min, 2)
