"""SR Invoice Parser is a small library(crawler) that is parsing invoices and extracting relevant information from URL. For Serbian market."""

__title__ = "sr_invoice_parser"
__author__ = "Innovigo"
__website__ = "https://wwwinnovigo.co/"
__email__ = "hello@innovigo.co"
__version__ = "1.0.0"

VERSION = __version__

from .exceptions import ParserParseException, ParserRequestException  # noqa: E402
from .parser import InvoiceParser  # noqa: E402

__all__ = ["InvoiceParser", "ParserRequestException", "ParserParseException"]
