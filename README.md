README
======

A simple web application that helps keep track of expenses. Helping users to better budget and progress to financial independence.

You can use this application online when it is released or pull down the code yourself on GitHub or deploy your own local version.

Proposed Release
================

Currently invalid input triggers a hard crash - since there is no data validation. Next release will include prodive data validation.

### Feature Pipeline
1. Users are warned of invalid expense input.
2. Users can see timestamp for each expense.
3. Users can delete existing expenses.
4. Users can change the date of when the expenses occured.
5. Each user has their own list of expenses.
6. Users can log in to their account and have the expenses persist
7. Users can choose the currency of the expense and a local currency to see the expenses in.
8. Users can allocate an account to each account.

### Book of Work
1. Write expense form unit tests - consider whether to add all edge cases.
2. Refactor expense input into a form object
3. Write automated deployment script using Fabric
4. Another FT! - Add timestamps when user logs (careful of timezones!)

Release Notes
=============

### 0.0.1 (24 July 2018)

* Conception

### 0.1.0 (30 July 2018)

* First release!
* Global list that everyone can access and log expenses that never disappear!
