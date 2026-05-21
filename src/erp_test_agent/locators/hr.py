"""HR module locators."""


class HRLocators:
    # Navigation
    MENU_HR = '[data-testid="menu-hr"]'
    MENU_EMPLOYEES = '[data-testid="menu-hr-employee"]'
    MENU_ATTENDANCE = '[data-testid="menu-hr-attendance"]'
    MENU_LEAVE = '[data-testid="menu-hr-leave"]'

    # Employee form
    BTN_NEW_EMPLOYEE = '[data-testid="btn-new-employee"]'
    EMPLOYEE_FIRST_NAME = '[data-testid="employee-first-name"]'
    EMPLOYEE_LAST_NAME = '[data-testid="employee-last-name"]'
    EMPLOYEE_NATIONAL_ID = '[data-testid="employee-national-id"]'
    EMPLOYEE_DEPARTMENT = '[data-testid="employee-department"]'
    EMPLOYEE_JOB_TITLE = '[data-testid="employee-job-title"]'
    EMPLOYEE_HIRE_DATE = '[data-testid="employee-hire-date"]'
    EMPLOYEE_CONTRACT_TYPE = '[data-testid="employee-contract-type"]'

    # Attendance report
    ATTENDANCE_EMPLOYEE_FILTER = '[data-testid="attendance-employee-filter"]'
    ATTENDANCE_MONTH = '[data-testid="attendance-month"]'
    ATTENDANCE_YEAR = '[data-testid="attendance-year"]'
    BTN_RUN_ATTENDANCE = '[data-testid="btn-run-attendance"]'

    # Common
    BTN_SAVE = '[data-testid="btn-save"]'
    RECORD_STATUS = '[data-testid="record-status"]'
