import smtplib
from email.message import EmailMessage


class EmailHandler(object):

    def __init__(self, destination_addresses, smtp_server, port, login_address, password, logger):
        assert isinstance(destination_addresses, (str, list))
        assert isinstance(smtp_server, str)
        self._destination_addresses = destination_addresses
        self.server = smtplib.SMTP(smtp_server, port)
        self.server.starttls()
        self.sender_address = login_address
        self.server.login(login_address, password)
        self.messages_sent = list()
        self.sender = login_address
        self.logger = logger
        self.logger.info("Instantiating Email Handler for Addresses: %s" % destination_addresses)

    def get_destination_addresses(self):
        """
        getter for destination addresses to receive alerts
        :return: self._destination
        """
        return self._destination_addresses

    def get_sender(self):
        """
        getter for sender address of alerts
        :return: self.sender_address
        """
        return self.sender_address

    def send_message(self, contents, subject):
        new_message = EmailMessage()
        new_message.set_content(contents)
        new_message['From'] = self.sender
        new_message['Subject'] = subject
        new_message['To'] = self._destination_addresses
        self.server.send_message(new_message)
        self.messages_sent.append(new_message)

    def get_sent_messages(self):
        """
        getter for sent messages
        :return: self.messages_sent (list)
        """
        return self.messages_sent
