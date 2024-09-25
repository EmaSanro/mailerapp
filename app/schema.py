instructions = [
    'DROP TABLE IF EXISTS email;',
    """
        CREATE TABLE email (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """
]