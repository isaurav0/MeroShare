# MeroShare
![](https://meroshare.cdsc.com.np/assets/img/brand-login.png)

This is an open-source library to interact with [meroshare](https://meroshare.cdsc.com.np/) website using python. It holds capability of logging in to the site, staying logged in, tracking all new updates and viewing reports of the shares you have applied, all from a simple script with few self explanatory functions.

### Table of Contents
- [Why library though?](#why-library-though-)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
    + [Getting banks](#getting-banks)
    + [Logging in](#logging-in)
    + [Listing IPO's and new issues](#listing-ipo-s-and-new-issues)
    + [List of all submitted applications](#list-of-all-submitted-applications)
    + [Details of company listed](#details-of-company-listed)
    + [Result of submitted application form](#result-of-submitted-application-form)
- [Command Line](#command-line)
- [Privacy Policy](#privacy-policy)

### Why library though?
  - The website itself relies on session storage to store authorization stuffs, so everytime you restart browser, you are logged out again (*must be for security reasons but bugs me alot*).
  - Could be used as an interface for data generation and gaining insights of the site over time.

### Installation
Download using `pip`.
```
pip install meroshare
```

### Quick Start
See how easy it is.
```python
>>> from meroshare import Meroshare
>>> share = MeroShare()
>>> # Getting new IPO's and new shares available in json format
>>> issues = share.getCurrentIssues().current_issues
>>> # pretty printing the result
>>> share.printIssues()
```
This example downloads all shares listed on the website in json format and pretty prints it for readability. 



### Usage

I have implemented [Fluent Interface](https://en.wikipedia.org/wiki/Fluent_interface) API design pattern so it can be intuitive to use. You might have already noticed that we use method chaining to collect data from website and accumulate the value in an attribute and then use the corresponding attribute.

#### Getting banks
To login to website, you need to select your bank. Bank details can be obtained as using `getBanks()` method. If you want json data, you can use `banks` attribute. If you want properly formatted results, use `printBanks()`. 
```python
>>> from meroshare import MeroShare
>>> share = MeroShare(defaultLogin=False)
>>> # Get banks data as json
>>> share.getBanks().banks
>>> # Printing banks info
>>> share.getBanks().printBanks()
```
You obtain `bank_id` and `bank_name` from the above command and any one of these in addition to your username and password, can be used to login to site.

#### Logging in
`login()` method can be used to login. It will prompt for username, password and bank details. 
```
>>> share.login()
```


#### Listing IPOs and new issues  

Use `getCurrentIssues()` to make request to site and obtain json which is stored in `issues` attribute.
```python
>>> share.getCurrentIssues()
>>> issues_json = share.issues
>>> # printing issues
>>> share.printIssues()
```


#### List of all submitted applications  

**Method:**  `getApplicationReport()` 
**Attribute:** `application_report` 
**Pretty Print:** `printApplicationReport()` 


#### Details of company listed  
**Method:** `getCompanyDetails(cid)` 
**Attribute:** `company_detail` 
**Pretty Print:** `printCompanyDetails()` 

`cid` is company_id and can be obtained from `application_report` and `issues`.


#### Result of submitted application form
**Method:** `getFormDetails(fid)` 
**Attribute:** `form_detail` 
**Pretty Print:** `printFormDetails()` 

`fid` is form_id and can be obtained from `application_report`

### Command Line
```
Usage: meroshare [option] [optional_options]

    Viewing banks
        $ meroshare banks

    Logging in
        $ meroshare login

        requires username, password and bank_id or bank_name
        bank details can be found from [banks] switch

    Viewing current issues
        $ meroshare issues

    Viewing company details
        $ meroshare company [company_id]
        [company_id] can be found from issues and reports

    Viewing submitted applications
        $ meroshare reports

    Viewing result of applied share
        $ meroshare result [form_id]
        [form_id] can be found from [reports] switch

    Logging out
        $ meroshare logout
```

### Privacy Policy
I don't collect any informations or credentials from the command line or from library. Usernames, passwords and every details are saved on your local machine. 
If you want to use this library in production or upload a project made using this library, if created, **make sure to hide** `.env` file from your repository as it contains your credentials. 

