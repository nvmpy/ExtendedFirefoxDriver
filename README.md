# ExtendedFirefoxDriver

An extention of the Selenium webdriver.Firefox class that adds a method for capturing user input.

There's a step-by-step walkthrough of the process and some usage guidance over at my blog:

[How to capture input from user in Selenium webdriver](https://benjihughes.co.uk/blog/take-capture-input-user-selenium/)

### Requirements
    
Requires the selenium library.
	
    pip install selenium
	

### Usage

Create an instance of the `ExtendedFirefoxDriver` class instead of `webdriver.Firefox` and use the `capture_input` method with the following arguments.

```
capture_selector - (required) CSS selector of input field to capture.

trigger_selector - (optional) CSS selector of element to trigger capture on click.
```


## Example


### Capture IMDB search query
```python
driver = ExtendedFirefoxDriver()
driver.get('http://www.imdb.com/')

search_value = driver.capture_input('#navbar-query', '#navbar-submit-button')

print "User searched: %s" % search_value
>>> 'User searched: shawshank redemption'
```

