@smoke @login
Feature: Login Feature

  Scenario: Successful login with valid credentials
    Given the user launches the browser
    When the user logs in with username "admin" and password "admin123"
    Then the user should see a welcome message