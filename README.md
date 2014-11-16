AWSCreditMonitor
================

AWSCreditMonitor allows you to easily check your AWS credit data across one or more accounts.

Installation
===============

Note: Firefox is required to use AWSCreditMonitor. 

EasySetup
---------------
EasySetup is required to enable Selenium installation. If you already
have Selenium installed, you can skip EasySetup's installation.

You can install EasySetup by doing the following:

1) Download EasySetup: https://bootstrap.pypa.io/ez_setup.py

2) Run "python ez_setup.py"

Selenium
---------------
Selenium is required by AWSCreditMonitor. It handles creating our
web driver and is used to log in to AWS and scrape the necessary data.

You can install Selenium by doing the following:

1) Download Selenium 2.44: https://pypi.python.org/packages/source/s/selenium/selenium-2.44.0.tar.gz

2) Extract Selenium

3) Go into the extracted directory and run "python setup.py install"

Configuration and Use
===============

1) Copy config.py.template to config.py. Open the file and add the accounts to check (one account per list entry)

2) Run python aws_credit_monitor.py. It'll log each account in, and print the relevant credit details.
