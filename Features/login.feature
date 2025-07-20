@smoke @login
@Submit
Feature: Submit Ajax Form

  Scenario: Submit Ajax Form and verify success
    Given the user navigates to Url
    When the user clicks on "Ajax Form Submit"
    And the user submits the form with name "John Doe" and comment "Testing Ajax form"
    Then the user should see the message "Form submitted Successfully!"