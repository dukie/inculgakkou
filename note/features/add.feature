# -*- coding: utf-8 -*-

Feature: Levels

   Scenario: Add new Sensei
    Given I am a visitor
    When I visit url "http://localhost:8081/incul/"
    When I click link contents "Settings"
    When I click link contents "Senseis"
    Then I should see "List of senseis" somewhere in page
    When I input "Test Sensei" in "FullName" field
    When I input "First'" in "FirstName" field
    When I input "LastName" in "LastName" field
    When I input "FullName" in "FullNameFurigana" field
    When I input "FirstName" in "FirstNameFurigana" field
    When I input "LastName" in "LastNameFurigana" field
    When I select "Male" in "Sex" dropdown
    When I input "04/19/1955" in "Birthday" field
    When I input "PlaceFrom" in "PlaceFrom" field
    When I click "Submit Sensei" button
    Then I should see "Test Sensei" somewhere in page

   Scenario: Add new Level
    Given I am a visitor
    When I visit url "http://localhost:8081/incul/"
    When I click link contents "Settings"
    When I click link contents "Levels"
    Then I should see "Lessons List" somewhere in page
    When I input "Test Level" in "Name" field
    When I input "04/19/2014" in "StartPeriod" field
    When I input "04/19/2015" in "EndPeriod" field
    When I click "Submit Level" button
    Then I should see "Test Level" somewhere in page


