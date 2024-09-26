class Console:
    """Handle output message of console"""
    def __init__(self, message, variant = 'success', location='') -> None:
       print(f"{variant}: {message} {'->' if len(location) > 0 else ''}  {location}") 