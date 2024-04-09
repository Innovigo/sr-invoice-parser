# SR Invoice Parser

[![build-status-image]][build-status]

SR Invoice Parser is a small library that is parsing invoices and extracting relevant information.
It is designed to work with invoices from the Tax Administration of the Republic of Serbia (Poreska uprava Republike Srbije).

- https://purs.gov.rs/
- https://suf.purs.gov.rs/

QR code gives a URL to the invoice web page, and this parser extracts the relevant information from the web page, like a crawler.

## Installation

To install SR Invoice Parser, follow these steps:

    pip install sr-invoice-parser

## Usage

The `InvoiceParser` class is the entry point for using the parser.

### Methods

- `get_data()` - Extracts all the data from the invoice and returns it as a dictionary
- `get_company_name()` - Extracts the company name.
- `get_company_tin()` - Extracts the company's tax identification number/PFR.
- `get_total_amount()` - Extracts the total amount of the invoice.
- `get_dt()` - Extracts the date and time of the invoice and converts it to UTC as a datetime object.
- `get_invoice_number()` - Extracts the invoice number.
- `get_invoice_text()` - Extracts the full text of the invoice with QR code base64.
- `get_items()` - Extracts items details from the invoice. This is array of dictionaries with keys: `name`, `quantity`, `price`, `total_price`.

Here's a basic example of how to use it:

```python
from sr_invoice_parser import InvoiceParser

parser = InvoiceParser(url="https://suf.purs.gov.rs/v/?vl=...")
# or
parser = InvoiceParser(html_text="<HTML source code of invoice web page>")

parser.data()

parser.get_company_name()
parser.get_company_tin()
parser.get_total_amount()
parser.get_dt()
parser.get_invoice_number()
parser.get_invoice_text()
parser.get_items()

```

## Example response data

```python
{
    "company_name": "Company Name",
    "company_tin": "123456789",
    "invoice_number": "QWERTYU1-QWERTYU1-12345",
    "invoice_datetime": datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
    "invoice_total_amount": 123.45,
    "invoice_text": "============ ФИСКАЛНИ РАЧУН ============.....",
    "invoice_items": [
        {
            "name": "Item 1",
            "quantity": 1,
            "price": 123.45,
            "total_price": 123.45
        }
    ]
}
```

Check the [test_parser.py](/tests/test_parser.py) file for more examples.

## Handling Exceptions

The module has custom exceptions for handling various error scenarios:

- `ParserParseException` - Raised when any error occurs during parsing the HTML content.
- `ParserRequestException` - Raised for errors related to fetching HTML content.

## Package Dependencies

Thanks to the following packages:

- [pytz](https://pypi.org/project/pytz/)
- [requests](https://pypi.org/project/requests/)
- [parsel](https://pypi.org/project/parsel/)
- [srtools](https://pypi.org/project/srtools/)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

If you have any questions, please contact us via email: [hello@innovigo.co](mailto:hello@innovigo.co?subject=[GitHub]%20sr-invoice-parser%20Question)

## License

This project is licensed under the [MIT License](/LICENSE).

[build-status-image]: https://github.com/Innovigo/sr-invoice-parser/actions/workflows/tests.yaml/badge.svg
[build-status]: https://github.com/Innovigo/sr-invoice-parser/actions/workflows/tests.yaml
