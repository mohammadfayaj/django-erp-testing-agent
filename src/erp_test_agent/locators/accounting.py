"""Accounting module locators."""


class AccountingLocators:
    # Navigation
    MENU_ACCOUNTING = '[data-testid="menu-accounting"]'
    MENU_JOURNAL_ENTRIES = '[data-testid="menu-accounting-journal-entry"]'
    MENU_COA = '[data-testid="menu-accounting-chart-of-accounts"]'
    MENU_REPORTS = '[data-testid="menu-accounting-reports"]'

    # Journal entry form
    BTN_NEW_JE = '[data-testid="btn-new-journal-entry"]'
    JE_DATE = '[data-testid="je-date"]'
    JE_REFERENCE = '[data-testid="je-reference"]'
    JE_LINE_ACCOUNT = '[data-testid="je-line-account"]'
    JE_LINE_DEBIT = '[data-testid="je-line-debit"]'
    JE_LINE_CREDIT = '[data-testid="je-line-credit"]'
    BTN_POST_JE = '[data-testid="btn-post-journal-entry"]'

    # Financial reports
    BTN_BALANCE_SHEET = '[data-testid="btn-balance-sheet"]'
    BTN_PROFIT_LOSS = '[data-testid="btn-profit-loss"]'
    REPORT_AS_OF_DATE = '[data-testid="report-as-of-date"]'
    REPORT_FROM_DATE = '[data-testid="report-from-date"]'
    REPORT_TO_DATE = '[data-testid="report-to-date"]'
    BTN_GENERATE_REPORT = '[data-testid="btn-generate-report"]'

    # Common
    BTN_SAVE = '[data-testid="btn-save"]'
    RECORD_STATUS = '[data-testid="record-status"]'
