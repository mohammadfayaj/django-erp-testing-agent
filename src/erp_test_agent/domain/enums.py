"""Domain enumerations shared across the ERP Test Agent."""

from enum import Enum


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


class AssertionType(str, Enum):
    UI_CONTAINS = "ui_contains"
    FIELD_EQUALS = "field_equals"
    FIELD_NOT_EMPTY = "field_not_empty"
    RECORD_EXISTS = "record_exists"
    BUSINESS_RULE = "business_rule"
    API_CHECK = "api_check"
    DB_CHECK = "db_check"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Browser(str, Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"
