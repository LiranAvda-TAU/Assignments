

class Message:

    def __init__(self, sender_id, receiver_id, creation_date, subject, body):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.date = creation_date
        self.subject = subject
        self.body = body

    def __repr__(self):
        return 'sender id: {0}\nreceiver id: {1}\ndate: {2}\nsubject: {3}\nbody: {4}'.format(self.sender_id,
                                                                                             self.receiver_id,
                                                                                             self.date,
                                                                                             self.subject,
                                                                                             self.body)

    @staticmethod
    def from_db_to_message(db_message):
        return Message(db_message['sender_id'],
                       db_message['receiver_id'],
                       db_message['created'],
                       db_message['subject'],
                       db_message['body']).__repr__()
