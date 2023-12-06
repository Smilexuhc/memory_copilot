class UnhandledAgentException(Exception):
    """Raised when the exception should not be handled by the agent"""
    pass


class WebCrawlError(UnhandledAgentException):
    """Raised when the web crawler encounters an error"""
    pass
