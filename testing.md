# 5.0 Testing

## 5.1 Known bugs

| Known bugs  | Issue |
| --------------- | ------------------------------------------------------------------------- |
| Removing all records of a token | The token will still show in portfolio but all values will be 0 |

## 5.2 Code validator

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| HTML W3C validator | All files pass the validator | Pass |
| CSS W3C validator | All files pass the validator | Pass |
| JS JSHint validator | All files pass the validator | Pass | 
| PEP8 | All files pass the validator | Pass |

## 5.3 Nav-bar

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Logo Link | Links to home page | Pass |
| Title Link | Links to home page | Pass |
| Home link | Links to home page | Pass |
| My Portfolio link | Links to portfolio page | Pass |
| Add record link | Links to add record page | Pass |
| Log in link | Links to log in page | Pass |
| Sign up link | Links to sign up page | Pass |
| Log out link | Logs user out returning them to log in page | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |
| Mobile drop down menu | Menu is responsive and links work | Pass |

## 5.4 Footer

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Facebook link | Links to Facebook page in a new tab | Pass |
| YouTube link | Links to YouTube page in a new tab | Pass |
| Instagram link | Links to Instagram page in a new tab | Pass |
| Twitter link | Links to Twitter page in a new tab | Pass |
| Home link | Links to Home page | Pass |
| Portfolio link | Links to Portfolio page | Pass |
| Log in link | Links to Log in page | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |

## 5.5 Home page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Top 50 cryptocurrencies | Home page lists top 50 cryptocurrencies | Pass |
| Update crypto listings | When page is refreshed the listings are updated | Pass |
| Sign up here link | Sign up here link works and only shows when user isn't logged in | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |
| Mobile scrollbar | Mobile devices have scroll bar for crypto table | Pass |

## 5.6 Log in page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Wrong username | If the username is incorrect a message flashing informing the user | Pass |
| Wrong password | If the password is incorrect a message flashing informing the user | Pass |
| Submit button works | Submit button works and signs user in to portfolio screen | Pass |
| Sign up link | Links to sign up page | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |

## 5.7 Sign up page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Username already taken | If the username is already in use the user is notified | Pass |
| Emails don't match | If the emails don't match the user is notified via flash message | Pass |
| Passwords don't match | If the passwords don't match the user is notified via flash message | Pass |
| Submit button works | Submit button works and signs user in to portfolio screen | Pass |
| Log in link | Links to log in page | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |

## 5.8 Portfolio page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Username is displayed | The username is displayed on portfolio tab | Pass |
| Portfolio total value | The portfolio total updated value displays under the name | Pass |
| Portfolio accordion | The portfolio accordion is responsive | Pass |
| Add new link | Links to add transaction page | Pass |
| Portfolio tokens | Each token in the portfolio displays on its own row | Pass |
| Updated token value | When the page is reloaded the tokens price, value, profit loss and 24h % change | Pass |
| New transactions | New transactions change the values on the portfolio page | Pass |
| View records | View button when pressed it opens the records modal | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |
| Mobile scrollbar | Mobile devices have scroll bar for portfolio table | Pass |

## 5.9 Record page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Date order | Shows record newest to oldest | Pass |
| List of tokens | Shows all token records name, type, quantity, per coin, data, notes and total | Pass |
| Edit button | Opens the edit page | Pass |
| Delete button | deletes the record | Pass |
| Flash delete message | User is prompted that the record was successfully deleted | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |
| Mobile scrollbar | Mobile devices have scroll bar for record table | Pass |

## 5.10 Add transaction page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Transaction tab works | Users can select buy, sell and staking changing the transaction form | Pass |
| Select coin | Lists top 50 crypto's | Pass |
| Buy order | Buy order records correct information | Pass |
| Sell order | Sell order records correct information | Pass |
| Staking order | Staking order records correct information | Pass |
| Orders update portfolio | Orders update correctly to the portfolio collection | Pass |
| Go back button | Links back to portfolio page | Pass |
| Add transaction button | The record is submited | Pass |
| Flash transaction message | User is prompted that the transaction was successfully recorded | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |

## 5.11 Edit page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Correct record being edited | The record the user clicked on is the one being edited | Pass |
| Go back button | Links back to portfolio page | Pass |
| Submit works | When sumbit is clicked the record is updated | Pass |
| Flash edit message | User is prompted that the change was successful | Pass |
| Desktop breakpoints | Responsive on desktop | Pass |
| Tablet breakpoints | Responsive on tablet | Pass |
| Mobile breakpoints | Responsive on mobile | Pass |
