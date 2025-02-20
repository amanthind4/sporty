
# Pytest-Selenium Framework





![test-sporty](https://github.com/user-attachments/assets/2af1f7ba-4cc0-423f-8779-6fa43013a484)

This project is built using the **Pytest** framework integrated with **Selenium WebDriver** for browser-based test automation. 


## Key Features
1. **Pytest Framework**: 
   - Simplified and scalable testing with fixtures, parameterization, and plugin support.
2. **Selenium WebDriver**:
   - Automates browser interactions for functional and end-to-end testing.
3. **WebDriver Manager**:
   - Automatically manages compatible WebDriver versions for seamless execution.
4. **Chrome Browser Requirement**:
   - Tests require the **Chrome browser** to be installed.

---

## Testcase: Verify Car Details
- Navigate to **Twitch.com**.
- click in the search icon
- input StarCraft II
- scroll down 2 times
-Select one streamer.
-on the streamer page wait until all is load and take a screenshot
- screenshot is saved under screenshot folder with test name and timestamp




## Folder Structure

###  **config**
   - Configuration files (`config.ini`) for application settings and browser preferences.


###  **logs**
   - Execution logs for debugging.

###  **Pages**
   - **pages**: Reusable Page Object Model (POM) implementations.



###  **testcases**
   - Pytest test cases for functional testing.

###  **utilities**
   - Helper modules for logging, configuration, and CSV handling.


###  **reports**
   - Stores test execution reports, using html reports.
   - To see the latest report go to the folder , go to file , right click and choose the browser of your choice to view.


---

## Reusability and Scalability
### Reusability
- Modular design with POM for reusing page interaction logic.
- Centralized helper functions in the `utilities` folder.

### Scalability
- Easily extendable for multiple browsers or configurations.


---

## Prerequisites
- **Chrome** browser installed.
- **Python 3.7+** installed.
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```

---

## Execution
- Run Pytest tests:
  ```
  pytest
  ```


This framework is designed for modular, scalable, and 
maintainable test automation with support for modern practices.



