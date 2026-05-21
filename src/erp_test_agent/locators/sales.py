"""Sales module locators."""


class SalesLocators:
    # Navigation
    MENU_SALES = '[data-testid="menu-sales"]'
    MENU_CUSTOMERS = '[data-testid="menu-sales-customer"]'
    MENU_ORDERS = '[data-testid="menu-sales-order"]'
    MENU_INVOICES = '[data-testid="menu-sales-invoice"]'

    # Customer form
    BTN_NEW_CUSTOMER = '[data-testid="btn-new-customer"]'
    CUSTOMER_NAME = '[data-testid="customer-name"]'
    CUSTOMER_VAT = '[data-testid="customer-vat"]'
    CUSTOMER_COUNTRY = '[data-testid="customer-country"]'
    CUSTOMER_CITY = '[data-testid="customer-city"]'
    CUSTOMER_CREDIT_LIMIT = '[data-testid="customer-credit-limit"]'
    CUSTOMER_PAYMENT_TERMS = '[data-testid="customer-payment-terms"]'

    # Sales order form
    BTN_NEW_ORDER = '[data-testid="btn-new-sales-order"]'
    SO_CUSTOMER = '[data-testid="so-customer"]'
    SO_ORDER_DATE = '[data-testid="so-order-date"]'
    SO_DELIVERY_DATE = '[data-testid="so-delivery-date"]'

    # Invoice form
    BTN_NEW_INVOICE = '[data-testid="btn-new-invoice"]'
    INV_SO_REF = '[data-testid="invoice-so-ref"]'
    INV_DATE = '[data-testid="invoice-date"]'
    INV_DUE_DATE = '[data-testid="invoice-due-date"]'
    BTN_POST_INVOICE = '[data-testid="btn-post-invoice"]'

    # Common
    BTN_SAVE = '[data-testid="btn-save"]'
    RECORD_STATUS = '[data-testid="record-status"]'
