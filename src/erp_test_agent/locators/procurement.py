"""Procurement module locators."""


class ProcurementLocators:
    # Navigation
    MENU_PROCUREMENT = '[data-testid="menu-procurement"]'
    MENU_VENDORS = '[data-testid="menu-procurement-vendor"]'
    MENU_PURCHASE_ORDERS = '[data-testid="menu-procurement-purchase-order"]'
    MENU_GRN = '[data-testid="menu-procurement-grn"]'

    # Vendor form
    BTN_NEW_VENDOR = '[data-testid="btn-new-vendor"]'
    VENDOR_NAME = '[data-testid="vendor-name"]'
    VENDOR_VAT = '[data-testid="vendor-vat"]'
    VENDOR_COUNTRY = '[data-testid="vendor-country"]'
    VENDOR_CITY = '[data-testid="vendor-city"]'
    VENDOR_PAYMENT_TERMS = '[data-testid="vendor-payment-terms"]'

    # Purchase order form
    BTN_NEW_PO = '[data-testid="btn-new-purchase-order"]'
    PO_VENDOR = '[data-testid="po-vendor"]'
    PO_ORDER_DATE = '[data-testid="po-order-date"]'
    PO_DELIVERY_DATE = '[data-testid="po-delivery-date"]'
    PO_ITEM_DESCRIPTION = '[data-testid="po-item-description"]'
    PO_ITEM_QTY = '[data-testid="po-item-quantity"]'
    PO_ITEM_PRICE = '[data-testid="po-item-unit-price"]'

    # GRN form
    BTN_NEW_GRN = '[data-testid="btn-new-grn"]'
    GRN_PO_REF = '[data-testid="grn-purchase-order-ref"]'
    GRN_RECEIVED_DATE = '[data-testid="grn-received-date"]'
    GRN_WAREHOUSE = '[data-testid="grn-warehouse"]'
    BTN_POST_GRN = '[data-testid="btn-post-grn"]'

    # Common
    BTN_SAVE = '[data-testid="btn-save"]'
    BTN_SUBMIT = '[data-testid="btn-submit"]'
    RECORD_STATUS = '[data-testid="record-status"]'
