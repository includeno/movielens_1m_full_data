from scrapy import Request

class ScrollSeleniumRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(self, wait_time=30, wait_until=None,wait_until_list=None, screenshot=False, script=None,wait_element=None,wait_count=None,wait_script=None,extra_info={}, *args, **kwargs):
        """Initialize a new selenium request

        Parameters
        ----------
        wait_time: int
            The number of seconds to wait.
        wait_until: method
            One of the "selenium.webdriver.support.expected_conditions". The response
            will be returned until the given condition is fulfilled.
        screenshot: bool
            If True, a screenshot of the page will be taken and the data of the screenshot
            will be returned in the response "meta" attribute.
        script: str
            JavaScript code to execute.

        """

        self.wait_time = wait_time
        self.wait_until = wait_until
        self.wait_until_list=wait_until_list
        self.screenshot = screenshot
        self.script = script

        self.wait_element = wait_element
        self.wait_count = wait_count
        self.wait_script = wait_script
        self.extra_info = extra_info
        
        super().__init__(*args, **kwargs)