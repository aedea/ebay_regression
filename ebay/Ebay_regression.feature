Feature: eBay regression

  Background:
    Given Go to "ebay.com"

# 5TH TEST - BANNER VALIDATION
  Scenario: Banner validation
    Then  Make sure the banner is visible
    And   Validate the banner is spinning by default
    Then  Validate 3 banner transitions
#    And   Verify pause button is working and it pauses automatic slide scrolling
#    And   Verify resume button is working and it resumes automatic slide scrolling
    And   Verify forward button is working and switching to the next slide
#    And   Verify previous button is working and switching to the previous slide
    Then   Wait 7 seconds


# 4TH TEST - CATEGORIES VALIDATION
  Scenario: Shop by category validation
    Then  Hover over Shop by category element
    And   Verify Shop by category dropdown
    Then  Validate categories and subcategories are matching the table
    | Category               | Subcategories |
    | collectibles & art     | collectibles; trading cards; sports memorabilia; coins & paper money |
    | electronics            | cameras & photo; computers, tablets & network hardware; video games & consoles; cell phones, smart watches & accessories |
    | business & industrial  | restaurant & food service; test, measurement & inspection equipment; heavy equipment, parts & attachments; modular & pre-fabricated buildings |
    | home & garden          | home improvement; yard, garden & outdoor living items; tools & workshop equipment; kitchen, dining & bar supplies |
    | clothing & accessories | handbags; women; men; collectible sneakers |
    | jewelry & watches      | fine jewelry; wristwatches; luxury watches; fashion jewelry |
    | sporting goods         | golf equipment; hunting equipment; outdoor sports; cycling equipment |
    | motors                 | other vehicles; parts & accessories; cars & trucks; motorcycles |
    | other categories       | baby essentials; toys & hobbies; books, movies & music; health & beauty |

#  Scenario: All categories dropdown validation
#    Then  Click on All Categories dropdown
#    And   Verify All Categories dropped down

# 3RD TEST - FILTER VALIDATION
  Scenario: Filter validation
    Then  Enter "dress" into the searchbar
    And   Click on "Search" button
    # if there's no subsection, type "NONE"
    Then  Filter by "Color", choose subsection "NONE" and select "Red"
    Then  Verify all titles from page №5 to page №4 are related to "dress"


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