Feature: eBay regression

  Scenario: User should be able to add item to the cart
    Given Open Chrome
    Then  Go to "ebay.com"
    Then  Enter "dress" to the searchbar
    Then  Click on "Search" button
    Then  Click on the first dress
    Then  Click "Add to cart button"
    Then  Click "Go to cart"
    And   Verify the item was added to the cart


  Scenario: All header elements/links are working & directing to corresponding pages
    Given Open Chrome
    Then  Go to "ebay.com"
    Then  Click on "Sign in"
    And   Verify "Sign in" page has opened. Expected url: "https://signin.ebay.com"
    Then  Go to "ebay.com"
    And   Click on "register"
    And   Verify "Registration" page has opened. Expected url: "https://signup.ebay.com"
    Then  Go to "ebay.com"
    Then  Click on "Daily Deals"
    And   Verify "Daily Deals" page has opened. Expected url: "https://www.ebay.com/deals"
    Then  Go to "ebay.com"
    Then  Click on "Brand Outlet"
    And   Verify "Brand Outlet" page has opened. Expected url: "https://www.ebay.com/b/Brand-Outlet"
    Then  Go to "ebay.com"
    Then  Click on "Gift Cards"
    And   Verify "Gift Cards" page has opened. Expected url: "https://www.ebay.com/giftcards"
    Then  Navigate to eBay.com
    Then  Click on "Help & Contact"
    And   Verify "Help & Contact" page has opened. Expected url: "https://www.ebay.com/help/home"
    Then  Navigate to eBay.com
    Then  Click on "Sell"
    And   Verify "Sell" page has opened. Expected url: "https://www.ebay.com/sl/sell"
    Then  Navigate to eBay.com
    Then  Click on "Watchlist"
    And   Verify Watchlist dropdown
    Then  Navigate to eBay.com
    Then  Hover over My eBay element
    And   Verify My eBay dropdown
    Then  Navigate to eBay.com
    Then  Hover over Notification element
    And   Verify Notification dropdown
    Then  Navigate to eBay.com
    Then  Hover over Cart element
    And   Verify Cart dropdown
    Then  Click on "Cart"
    And   Verify "Cart" page has opened. Expected url: "https://cart.ebay.com"