Feature: eBay regression

  Background:
    Given Go to "ebay.com"


  # 3RD TEST - FILTER VALIDATION
  Scenario: Filter validation
    Then  Enter "dress" to the searchbar
    And   Click on "Search" button
    # if there's no subsection, type "NONE"
    Then  Filter by "Size", choose subsection "Regular" and select "M"
    Then  Go to page #1
    # type the number of desired pages to verify if titles are related to the search
    Then  Verify all items on 3 pages are related to "dress"


  # 2ND TEST - HEADER VALIDATION
  Scenario Outline: All header elements/links are working & directing to corresponding pages
    Then  Click on "<Header link>"
    And   Verify "<Page title>" page has opened. Expected url: "<Expected URL>"
  Examples:
    | Header link    | Page title     | Expected URL                        |
    | Sign in        | Sign in        | https://signin.ebay.com             |
    | register       | Registration   | https://signup.ebay.com             |
    | Daily Deals    | Daily Deals    | https://www.ebay.com/deals          |
    | Brand Outlet   | Brand Outlet   | https://www.ebay.com/b/Brand-Outlet |
    | Gift Cards     | Gift Cards     | https://www.ebay.com/giftcards      |
    | Help & Contact | Help & Contact | https://www.ebay.com/help/home      |
    | Sell           | Sell           | https://www.ebay.com/sl/sell        |
    | Cart           | Cart           | https://cart.ebay.com               |

  Scenario Outline: Validate header dropdowns
    Then  Hover over <Header element> element
    And   Verify <Header element> dropdown
  Examples:
    | Header element |
    | Watchlist      |
    | My eBay        |
    | Notification   |
    | Cart           |


  # 1ST TEST - DRESS SEARCH
  Scenario: User should be able to add item to the cart
    Then  Enter "dress" to the searchbar
    Then  Click on "Search" button
    Then  Click on the first dress
    Then  Click "Add to cart button"
    Then  Click "Go to cart"
    And   Verify the item was added to the cart