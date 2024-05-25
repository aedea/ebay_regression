Feature: eBay regression

  Background:
    Given Go to "ebay.com"

# 4TH TEST - CATEGORIES VALIDATION
  Scenario: Categories validation
    Then  Hover over Shop by category element
    And   Verify Shop by category dropdown
    Then  The categories and subcategories should be:
    | Category              | Subcategories                                                                                                            |
    | Motors                | Parts & accessories; Cars & trucks; Motorcycles; Other vehicles                                                          |
    | Electronics           | Computers, Tablets & Network Hardware; Cell Phones, Smart Watches & Accessories; Video Games & Consoles; Cameras & Photo |
    | Collectibles & Art    | Trading cards; Collectibles; Coins & Paper Money; Sports Memorabilia                                                     |


# 3RD TEST - FILTER VALIDATION
  Scenario: Filter validation
    Then  Enter "dress" into the searchbar
    And   Click on "Search" button
    # if there's no subsection, type "NONE"
    Then  Filter by "Color", choose subsection "NONE" and select "Red"
    Then  Verify all titles from page №5 to page №3 are related to "dress"


# 2ND TEST - HEADER VALIDATION
  Scenario Outline: All header elements/links are working & directing to corresponding pages
    Then  Click on "<Header link>"
    And   Verify "<Header link>" page has opened. Expected url: "<Expected URL>"
  Examples:
    | Header link    | Expected URL                        |
    | Sign in        | https://signin.ebay.com             |
    | register       | https://signup.ebay.com             |
    | Daily Deals    | https://www.ebay.com/deals          |
    | Brand Outlet   | https://www.ebay.com/b/Brand-Outlet |
    | Gift Cards     | https://www.ebay.com/giftcards      |
    | Help & Contact | https://www.ebay.com/help/home      |
    | Sell           | https://www.ebay.com/sl/sell        |
    | Cart           | https://cart.ebay.com               |

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
    Then  Enter "dress" into the searchbar
    Then  Click on "Search" button
    Then  Click on the first dress
    Then  Click "Add to cart button"
    Then  Click "Go to cart"
    And   Verify the item was added to the cart