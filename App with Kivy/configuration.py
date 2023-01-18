"""
    configuration
    Holds configuration for the app.
    :copyright: (c) 2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""

# ROOT requirements
MINIMUM_HEIGHT, MINIMUM_WIDTH = 500, 400

# User and passwords related.
# Password and User_Id constrains.
MIN_LEN_USERNAME = 5
MAX_LEN_USERNAME = 12
MIN_LEN_PASSWORD = 10
# Status for labels:
STATUS_LABELS = [
    'Check',  # Default point [0]
    'Empty',  # Password/username empty [1]
    'Ok',  # Field ok [2]
    'User not available',  # User taken [3]
    'Too short',  # Password/username too short [4]
    'Too long',  # Password/username too long [5]
    'Password not matching'  # Passwords does not match [6]
]
