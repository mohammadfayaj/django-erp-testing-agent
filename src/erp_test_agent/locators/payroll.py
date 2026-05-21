"""Payroll module locators."""


class PayrollLocators:
    # Navigation
    MENU_PAYROLL = '[data-testid="menu-payroll"]'
    MENU_PAYROLL_RUNS = '[data-testid="menu-payroll-runs"]'
    MENU_PAYSLIPS = '[data-testid="menu-payroll-payslips"]'
    MENU_SALARY_STRUCTURES = '[data-testid="menu-payroll-salary-structures"]'

    # Payroll run form
    BTN_NEW_PAYROLL_RUN = '[data-testid="btn-new-payroll-run"]'
    PAYROLL_MONTH = '[data-testid="payroll-month"]'
    PAYROLL_YEAR = '[data-testid="payroll-year"]'
    PAYROLL_DEPARTMENT = '[data-testid="payroll-department"]'
    BTN_GENERATE_PAYSLIPS = '[data-testid="btn-generate-payslips"]'
    BTN_POST_PAYROLL = '[data-testid="btn-post-payroll"]'

    # Payslip
    PAYSLIP_EMPLOYEE = '[data-testid="payslip-employee"]'
    PAYSLIP_BASIC = '[data-testid="payslip-basic-salary"]'
    PAYSLIP_NET = '[data-testid="payslip-net-salary"]'

    # Common
    BTN_SAVE = '[data-testid="btn-save"]'
    RECORD_STATUS = '[data-testid="record-status"]'
