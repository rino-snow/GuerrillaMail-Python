class Message:
    __slots__ = ("mail_id",
                 "mail_from",
                 "mail_subject",
                 "mail_excerpt",
                 "mail_timestamp")
    
    def __init__(self,
                 response: dict):
        self.mail_id = response.get('mail_id')
        self.mail_from = response.get('mail_from')
        self.mail_subject = response.get('mail_subject')
        self.mail_excerpt = response.get('mail_excerpt')
        self.mail_timestamp = response.get('mail_timestamp')

    def __repr__(self):
        return (f"Message(mail_id={self.mail_id},"
                f"mail_from={self.mail_from},"
                f"mail_subject={self.mail_subject},"
                f"mail_excerpt={self.mail_excerpt},"
                f"mail_timestamp={self.mail_timestamp})")
