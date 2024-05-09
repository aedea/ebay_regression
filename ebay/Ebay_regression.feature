Feature: eBay regression

  Scenario: User should be able to add item to the cart
    Given Open Chrome
    Then  Navigate to eBay.com
    Then  Enter "dress" to the searchbar
    Then  Click on "Search" button
    Then  Click on the first dress
    Then  Click "Add to cart button"
    Then  Click "Go to cart"
    And   Verify the item was added to the cart


  Scenario: All header elements/links are working & directing to corresponding pages
    Given Open Chrome
    Then  Navigate to eBay.com
    Then  Click "Sign in" and and verify sign in page is opened
    Then  Navigate to eBay.com
    And   Click "register" and verify registration page has opened
    Then  Navigate to eBay.com
    Then  Click "Daily Deals" and verify daily deals page has opened
    Then  Navigate to eBay.com
    Then  Click "Brand Outlet" and verify Brand Outlet page has opened
    Then  Navigate to eBay.com
    Then  Click "Gift Cards" and verify gift cards page has opened
    Then  Navigate to eBay.com
    Then  Click "Help & Contact" and verify help and contact page has opened
    Then  Navigate to eBay.com
    Then  Click "Sell" and verify sell page has opened
    Then  Navigate to eBay.com
    Then  Click "Watchlist" and verify watchlist dropped down
    Then  Navigate to eBay.com
    Then  Hover over "My eBay" and verify my ebay dropdown menu has opened
    Then  Navigate to eBay.com
    Then  Hover over notification icon and verify notifications have opened
    Then  Navigate to eBay.com
    Then  Click on cart icon and verify cart page has opened
