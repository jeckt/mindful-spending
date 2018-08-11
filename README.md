README
======

A simple web application that helps keep track of expenses. Helping users to better budget and progress to financial independence.

You can use this application online when it is released or pull down the code yourself on GitHub or deploy your own local version.

Proposed Release
================

There is no sense of when the expense was logged. We add a date to our expenses
so users can track a trend in their expenses over time.

### Feature Pipeline
1. Users can change the date of when the expenses occured. (other edits)
2. Each user has their own list of expenses.
3. Users can log in to their account and have the expenses persist
4. Users can choose the currency of the expense and a local currency to see the expenses in.
5. Users can allocate an account to each account.

### Book of Work
1. TDD workflow cycle to get edit functionality online
2. Deploy
3. Allow users to update the expense date on expense entry

### Back Log
* (do it when we look at each users has their own list) Consider whether we can refactor our views render doesn't need to pass Exenses/Total expenses.
* Find out why form hidden date input generates two input fields - this seems to happen with the Django Forms HiddenInput attribute.

### Development Notes

The user/visitor will pass the date of the expense through a post request. This
will not be editable by the user to start with (future release feature) but
still will be visible for them to see. The reason to adopt this approach is
because if the web server was to decide the date this may differ to what the
user/visitor expects due to timezone differences!

Release Notes
=============

### 0.0.1 (24 July 2018)

* Conception

### 0.1.0 (30 July 2018)

* First release!
* Global list that everyone can access and log expenses that never disappear!

### 0.1.1 (3 August 2018)

* Deploy the live website
* Expense validation.

### 0.1.2 (5 August 2018)

* Expenses now have a date of when they were logged.

### 0.1.3 (8 August 2018)

* Expenses can now be deleted.
