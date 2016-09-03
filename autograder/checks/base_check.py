class BaseCheck(object):
    def __init__(self, context):
        self.context = context
        self.error_count = 0
        self.warning_count = 0

    def error(self, message):
        self.error_count += 1
        self.context.logger.error(message)

    def warn(self, message):
        self.warning_count += 1
        self.context.logger.warn(message)

    def info(self, message):
        self.context.logger.info(message)
