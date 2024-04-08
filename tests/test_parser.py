import os
from datetime import datetime
from unittest import TestCase, mock

import pytest
from pytz import utc

from sr_invoice_parser.exceptions import ParserParseException, ParserRequestException
from sr_invoice_parser.parser import InvoiceParser

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def read_example_response():
    with open(os.path.join(__location__, "example_response.html"), "rb") as file:
        content = file.read()
    return content


class TestParser(TestCase):
    def setUp(self):
        super().setUp()
        self.example_response = read_example_response()

    def create_success_mock_response(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = self.example_response
        return mock_response

    def create_wrong_mock_response(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = "Bad mock response"
        return mock_response

    def test_init_no_url_and_html(self):
        """Test that an exception is raised when no URL or HTML content is provided"""

        with pytest.raises(
            ParserParseException, match="URL or HTML content is required"
        ):
            InvoiceParser()

    def test_validate_url(self) -> None:
        """Test that the validate_url method works as expected"""

        with pytest.raises(ParserRequestException, match="Invalid domain"):
            InvoiceParser(url="https://example.com").validate_url()

        InvoiceParser(url="https://suf.purs.gov.rs/v/vl?").validate_url()

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_fetch_failed_with_400(self, mock_get):
        # Create a mock response
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.text = "Mock response"
        mock_get.return_value = mock_response

        with pytest.raises(
            ParserRequestException, match="Request failed with status code 400"
        ):
            parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
            parser.fetch()

        mock_get.assert_called_once_with("https://suf.purs.gov.rs/v/vl?")

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_fetch_response(self, mock_get):
        # Create a mock response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = "Mock response"
        mock_get.return_value = mock_response

        parser = InvoiceParser(html_text="Example HTML content")
        parser.url = "https://suf.purs.gov.rs/v/vl?"
        result = parser.fetch()

        assert result == "Mock response"
        mock_get.assert_called_once_with("https://suf.purs.gov.rs/v/vl?")

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_company_name_failed(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_wrong_mock_response()
        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")

        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_company_name': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_company_name()

        # test with HTML content
        parser = InvoiceParser(html_text="Bad HTML content")
        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_company_name': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_company_name()

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_company_name(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_success_mock_response()
        value = "Primer naziva firme"

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
        assert parser.get_company_name() == value

        # test with HTML content
        parser = InvoiceParser(html_text=self.example_response)
        assert parser.get_company_name() == value

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_company_tin_failed(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_wrong_mock_response()

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")

        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_company_tin': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_company_tin()

        # test with HTML content
        parser = InvoiceParser(html_text="Bad HTML content")
        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_company_tin': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_company_tin()

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_company_tin(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_success_mock_response()
        value = "123456789"

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
        assert parser.get_company_tin() == value

        # test with HTML content
        parser = InvoiceParser(html_text=self.example_response)
        assert parser.get_company_tin() == value

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_total_amount_failed(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_wrong_mock_response()

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")

        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_total_amount': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_total_amount()

        # test with HTML content
        parser = InvoiceParser(html_text="Bad HTML content")
        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_total_amount': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_total_amount()

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_total_amount(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_success_mock_response()
        value = float(8960.0)

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
        assert parser.get_total_amount() == value

        # test with HTML content
        parser = InvoiceParser(html_text=self.example_response)
        assert parser.get_total_amount() == value

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_dt_failed(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_wrong_mock_response()

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")

        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_dt': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_dt()

        # test with HTML content
        parser = InvoiceParser(html_text="Bad HTML content")
        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_dt': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_dt()

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_dt(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_success_mock_response()
        value = datetime(2024, 4, 7, 15, 0, 30).replace(tzinfo=utc)

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
        assert parser.get_dt() == value

        # test with HTML content
        parser = InvoiceParser(html_text=self.example_response)
        assert parser.get_dt() == value

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_invoice_number_failed(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_wrong_mock_response()

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")

        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_invoice_number': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_invoice_number()

        # test with HTML content
        parser = InvoiceParser(html_text="Bad HTML content")
        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_invoice_number': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_invoice_number()

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_invoice_number(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_success_mock_response()
        value = "QWERTYU1-QWERTYU1-12345"

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
        assert parser.get_invoice_number() == value

        # test with HTML content
        parser = InvoiceParser(html_text=self.example_response)
        assert parser.get_invoice_number() == value

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_invoice_text_failed(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_wrong_mock_response()

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")

        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_invoice_text': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_invoice_text()

        # test with HTML content
        parser = InvoiceParser(html_text="Bad HTML content")
        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_invoice_text': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_invoice_text()

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_invoice_text(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_success_mock_response()
        value = """<pre style="font-family:monospace">============ ФИСКАЛНИ РАЧУН ============
123456789
OKOV INTERNATIONAL
Primer naziva firme
Кнеза Михаила
Београд-Београд
Касир:                         prodavac1
ИД купца:                   10:987654321
ЕСИР број:                      644/20.1
-------------ПРОМЕТ ПРОДАЈА-------------
Артикли
========================================
Назив   Цена         Кол.         Укупно
Veoma dugačak naziv artikla za testiranj
e test 1 (Ђ)
    4.000,00          1       4.000,00
Veoma dugačak naziv artikla za testiranj
 test 2 (Ђ)
    1.000,00          1       1.000,00
Kratak naziv artikla 1 (Е)
    1.960,00          1       1.960,00
Kratak naziv artikla 2 (G)
    1.000,00          1       1.000,00
Kratak naziv artikla 3 (A)
    1.000,00          1       1.000,00
----------------------------------------
Укупан износ:                   8.960,00
Платна картица:                 8.960,00
========================================
Ознака       Име      Стопа        Порез
Ђ           О-ПДВ   20,00%        500,00
Е           О-ПДВ   10,00%        196,00
A           О-ПДВ    0,00%          0,00
G           О-ПДВ    0,00%          0,00
----------------------------------------
Укупан износ пореза:              696,00
========================================
ПФР време:          07.04.2024. 17:00:30
ПФР број рачуна: QWERTY1U-QWERTY1U-18855
3
Бројач рачуна:           175097/188553ПП
========================================<br><img src="data:image/gif;base64" width="250" height="250">
======== КРАЈ ФИСКАЛНОГ РАЧУНА =========</pre>"""

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
        assert parser.get_invoice_text() == value

        # test with HTML content
        parser = InvoiceParser(html_text=self.example_response)
        assert parser.get_invoice_text() == value

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_items_failed(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_wrong_mock_response()

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")

        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_items': Failed to parse the HTML content in 'get_invoice_text': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_items()

        # test with HTML content
        parser = InvoiceParser(html_text="Bad HTML content")
        with pytest.raises(
            ParserParseException,
            match="Failed to parse the HTML content in 'get_items': Failed to parse the HTML content in 'get_invoice_text': 'NoneType' object has no attribute 'strip'",
        ):
            parser.get_items()

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_items(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_success_mock_response()
        value = [
            {
                "name": "Veoma dugačak naziv artikla za testiranje test 1",
                "vat": 20,
                "price": 4000.0,
                "quantity": 1,
                "total_price": 4000.0,
            },
            {
                "name": "Veoma dugačak naziv artikla za testiranj test 2",
                "vat": 20,
                "price": 1000.0,
                "quantity": 1,
                "total_price": 1000.0,
            },
            {
                "name": "Kratak naziv artikla 1",
                "vat": 10,
                "price": 1960.0,
                "quantity": 1,
                "total_price": 1960.0,
            },
            {
                "name": "Kratak naziv artikla 2",
                "vat": 0,
                "price": 1000.0,
                "quantity": 1,
                "total_price": 1000.0,
            },
            {
                "name": "Kratak naziv artikla 3",
                "vat": 0,
                "price": 1000.0,
                "quantity": 1,
                "total_price": 1000.0,
            },
        ]

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
        assert parser.get_items() == value

        # test with HTML content
        parser = InvoiceParser(html_text=self.example_response)
        assert parser.get_items() == value

    @mock.patch("sr_invoice_parser.parser.requests.get")
    def test_get_data(self, mock_get):
        # Create a mock response
        mock_get.return_value = self.create_success_mock_response()
        value = {
            "company_name": "Primer naziva firme",
            "company_tin": "123456789",
            "invoice_number": "QWERTYU1-QWERTYU1-12345",
            "invoice_datetime": datetime(2024, 4, 7, 15, 0, 30).replace(tzinfo=utc),
            "invoice_total_amount": 8960.0,
            "invoice_items": [
                {
                    "name": "Veoma dugačak naziv artikla za testiranje test 1",
                    "vat": 20,
                    "price": 4000.0,
                    "quantity": 1,
                    "total_price": 4000.0,
                },
                {
                    "name": "Veoma dugačak naziv artikla za testiranj test 2",
                    "vat": 20,
                    "price": 1000.0,
                    "quantity": 1,
                    "total_price": 1000.0,
                },
                {
                    "name": "Kratak naziv artikla 1",
                    "vat": 10,
                    "price": 1960.0,
                    "quantity": 1,
                    "total_price": 1960.0,
                },
                {
                    "name": "Kratak naziv artikla 2",
                    "vat": 0,
                    "price": 1000.0,
                    "quantity": 1,
                    "total_price": 1000.0,
                },
                {
                    "name": "Kratak naziv artikla 3",
                    "vat": 0,
                    "price": 1000.0,
                    "quantity": 1,
                    "total_price": 1000.0,
                },
            ],
            "invoice_text": """<pre style="font-family:monospace">============ ФИСКАЛНИ РАЧУН ============
123456789
OKOV INTERNATIONAL
Primer naziva firme
Кнеза Михаила
Београд-Београд
Касир:                         prodavac1
ИД купца:                   10:987654321
ЕСИР број:                      644/20.1
-------------ПРОМЕТ ПРОДАЈА-------------
Артикли
========================================
Назив   Цена         Кол.         Укупно
Veoma dugačak naziv artikla za testiranj
e test 1 (Ђ)
    4.000,00          1       4.000,00
Veoma dugačak naziv artikla za testiranj
 test 2 (Ђ)
    1.000,00          1       1.000,00
Kratak naziv artikla 1 (Е)
    1.960,00          1       1.960,00
Kratak naziv artikla 2 (G)
    1.000,00          1       1.000,00
Kratak naziv artikla 3 (A)
    1.000,00          1       1.000,00
----------------------------------------
Укупан износ:                   8.960,00
Платна картица:                 8.960,00
========================================
Ознака       Име      Стопа        Порез
Ђ           О-ПДВ   20,00%        500,00
Е           О-ПДВ   10,00%        196,00
A           О-ПДВ    0,00%          0,00
G           О-ПДВ    0,00%          0,00
----------------------------------------
Укупан износ пореза:              696,00
========================================
ПФР време:          07.04.2024. 17:00:30
ПФР број рачуна: QWERTY1U-QWERTY1U-18855
3
Бројач рачуна:           175097/188553ПП
========================================<br><img src="data:image/gif;base64" width="250" height="250">
======== КРАЈ ФИСКАЛНОГ РАЧУНА =========</pre>""",
        }

        # test with URL
        parser = InvoiceParser(url="https://suf.purs.gov.rs/v/vl?")
        assert parser.data() == value

        # test with HTML content
        parser = InvoiceParser(html_text=self.example_response)
        assert parser.data() == value
