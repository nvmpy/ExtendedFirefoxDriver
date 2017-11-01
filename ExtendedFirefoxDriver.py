import urllib2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class ExtendedFirefoxDriver(webdriver.Firefox):

    def load_jquery(self):
        """ Injects jQuery library into currently loaded page. """
        jquery_js = urllib2.urlopen('https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js')
        jquery = jquery_js.read()
        self.execute_script(jquery)

    def capture_input(self, capture_selector, trigger_selector=None):
        """
        Captures and returns the value of element "capture_selector" when
        click action is performed on "trigger_selector".

        Keyword arguments:
        capture_selector -- The CSS selector of the input field to capture (required)
        trigger_selector -- The CSS selector of an element to trigger the capture (default None)
        """

        self.load_jquery()

        # This is arbitrary but has to be unique.
        transfer_el_id = 'transfer-el'

        # Build catch script.
        catch_script = """
            var captureInput = $('%s');var createTransferElement = function(){transferDiv = $("<div></div>", {id: "%s", "style":"display:none;"});
            transferDiv.text(captureInput.val());captureInput.parent().append(transferDiv);}; captureInput.off('keydown');
            captureInput.keyup(function (ev) {if (ev.keyCode == 13) {ev.preventDefault();ev.stopPropagation();createTransferElement();}});
        """ % (capture_selector, transfer_el_id)
        remove_handlers_script = "$('%s').off('keyup');" % capture_selector

        # Add trigger parts to script if specified.
        if trigger_selector is not None:
            trigger_script = """
                var triggerButton = $('%s');triggerButton.click(function(ev){ev.preventDefault();ev.stopPropagation();createTransferElement();});
            """ % trigger_selector
            catch_script += trigger_script
            remove_handlers_script += "$('%s').off('click');" % trigger_selector

        # Execute our script.
        self.execute_script(catch_script)

        # Wait for the transfer element to be added to the DOM.
        transfer_el_exists = EC.presence_of_element_located((By.ID, transfer_el_id))
        WebDriverWait(self, 2**30).until(transfer_el_exists)

        # Retrieve transfer element text
        transfer = self.find_element(By.ID, transfer_el_id)
        inner_text = transfer.get_attribute('innerText')

        # Remove our listeners from earlier.
        self.execute_script(remove_handlers_script)

        # Fire the trigger or press enter depending on whether or not we specified a trigger element.
        if trigger_selector is not None:
            trigger_el = self.find_element_by_css_selector(trigger_selector)
            trigger_el.click()
        else:
            capture_el = self.find_element_by_css_selector(capture_selector)
            capture_el.sendKeys(Keys.RETURN)

        return inner_text