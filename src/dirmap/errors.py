"""Exception hierarchy for DIRMAP.

All errors raised on purpose by DIRMAP derive from :class:`DirmapError`, so
callers (including the CLI) can catch a single base class.
"""


class DirmapError(Exception):
    """Base class for every DIRMAP error."""


class ScanError(DirmapError):
    """Raised when a folder cannot be scanned or does not exist."""


class ExportError(DirmapError):
    """Raised when a report cannot be written to disk."""
