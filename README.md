README
======

A simple web application that helps keep track of expenses. Helping users to better budget and progress to financial independence.

You can use this application online when it is released or pull down the code yourself on GitHub or deploy your own local version.

Proposed Release
================

There is no sense of when the expense was logged. We add a date to our expenses
so users can track a trend in their expenses over time.

### Feature Pipeline
1. Users can see date for each expense.
2. Users can delete existing expenses.
3. Users can change the date of when the expenses occured. (other edits)
4. Each user has their own list of expenses.
5. Users can log in to their account and have the expenses persist
6. Users can choose the currency of the expense and a local currency to see the expenses in.
7. Users can allocate an account to each account.

### Book of Work
1. Find out why form hidden date input generates two input fields
2. Consider inconsistent date bug - user loads website, leaves it
for more than a day...will the expense be logged as the day the
website loaded or the day the expense is submitted???
3. Design how users will be able to delete expenses.
4. Write functional tests on deleting existing expenses.
5. Write unit tests for deleting existing expenses.

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
