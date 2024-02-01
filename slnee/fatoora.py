"""
A module to implement ZATCA e-invoice (fatoora)
more information @ https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Pages/default.aspx
"""
import frappe
from uttlv import TLV
import base64
from hashlib import sha256
import qrcode
import json
from typing import Union, Optional
from PIL import Image
from pyzbar.pyzbar import decode
from pydantic import validate_arguments
import validators
from datetime import datetime

__all__ = ("Fatoora", "iso8601_zulu_format", "is_valid_iso8601_zulu_format")

iso8601_zulu_format = "%Y-%m-%dT%H:%M:%SZ"

def getqrcode(doctype,doc):
    if doc.doctype=="Sales Invoice":
        tax_id = frappe.get_doc("Company",doc.company).tax_id
        if not tax_id :
            tax_id =""
        company=doc.company
        date= str(doc.posting_date)+" "+str(doc.posting_time)
        total = doc.grand_total
        tax=doc.total_taxes_and_charges
    if doc.doctype=="Clearances":
        tax_id = frappe.get_doc("Company",doc.company).tax_id
        if not tax_id :
            tax_id =""
        company=doc.company
        date= str(doc.clearance_date)+" 12:00:00"
        total = doc.net_amount
        tax=doc.vat

        
    fatoora_obj = Fatoora(
    seller_name=company,
    tax_number= tax_id,
    invoice_date=date,
    total_amount=total,
    tax_amount=tax, 
)
    return(fatoora_obj.base64)


    
def is_valid_iso8601_zulu_format(string_date: str) -> bool:
    """Returns True if the string valid ISO 8601 Zulu format
    Args:
        string_date (str): The date.
    Returns:
        bool: is valid valid ISO 8601 Zulu or not.
    """
    try:
        datetime.strptime(string_date, iso8601_zulu_format)
    except Exception:
        return False
    else:
        return True


class Fatoora:
    def __init__(
        self,
        seller_name: str,
        tax_number: str,
        invoice_date: float,
        total_amount: float,
        tax_amount: str,
        qrcode_url: Optional[str] = None,
        tags: TLV = TLV(),
    ):
        self.tags = tags
        self.seller_name = seller_name
        self.tax_number = tax_number
        self.invoice_date = invoice_date
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        self.qrcode_url = qrcode_url

    @classmethod
    def base2dict(cls, base: str) -> dict:
        """Convert base64 to a dictionary
        Args:
            base (str): base64
        Returns:
            dict: dictionary of base64 contents
        """
        tags = TLV()
        decoded = base64.b64decode(base)

        tags = TLV()
        tags.parse_array(bytes(decoded))
        values = (tags[counter].decode() for counter in tags)
        keys = (
            "seller_name",
            "tax_number",
            "invoice_date",
            "total_amount",
            "tax_amount",
        )
        return dict(zip(keys, values))

    @classmethod
    def read_qrcode(
        cls, filename: str, dct: bool = False
    ) -> Optional[Union[str, dict]]:
        """read content of qr code
        Args:
            filename (str): qr code path
            dct (bool, optional): True -> return dict of content
                                False -> return base64 of content or url. Defaults to False.
        Returns:
            Optional[Union[str, dict]]: content of qr code
        """
        data = decode(Image.open(filename))[0].data.decode()

        if dct:
            return cls.base2dict(data)
        else:
            return data

    @property
    def seller_name(self) -> str:
        return self.tags[1]

    @seller_name.setter
    @validate_arguments
    def seller_name(self, new_value: str) -> None:
        self.tags[0x01] = new_value

    @property
    def tax_number(self) -> str:
        return self.tags[2]

    @tax_number.setter
    @validate_arguments
    def tax_number(self, new_value: str) -> None:
        self.tags[0x02] = str(new_value)

    @property
    def invoice_date(self) -> datetime:
        return datetime.strptime(self.tags[3], iso8601_zulu_format)

    @invoice_date.setter
    @validate_arguments
    def invoice_date(self, date: Union[datetime, float, str]) -> None:
        """The ability to enter the invoice date as timestamp or datetime object, or string ISO 8601 Zulu format
            and save it as ISO 8601 Zulu format
        Args:
            date (Union[datetime, float, str]): invoice date
        """
        if type(date) is float:
            date = datetime.fromtimestamp(date)
        elif type(date) is str:
            if is_valid_iso8601_zulu_format(date):
                date = datetime.strptime(date, iso8601_zulu_format)
            else:
                raise ValueError(
                    f"Invalid date format: {date} should be iso8601 format or timestamp or datetime object"
                )
        else:
            # is datetime object
            pass
        self.tags[0x03] = date.strftime(iso8601_zulu_format)

    @property
    def total_amount(self) -> str:
        return float(self.tags[4])

    @total_amount.setter
    @validate_arguments
    def total_amount(self, new_value: float) -> None:
        self.tags[0x04] = str(new_value)

    @property
    def tax_amount(self) -> str:
        return float(self.tags[5])

    @tax_amount.setter
    @validate_arguments
    def tax_amount(self, new_value: str) -> None:
        self.tags[0x05] = str(new_value)

    @property
    def qrcode_url(self) -> Optional[str]:
        return self._qrcode_url

    @qrcode_url.setter
    @validate_arguments
    def qrcode_url(self, new_value: Optional[str]) -> None:
        if not new_value or validators.url(new_value):
            self._qrcode_url = new_value
        else:
            raise ValueError(f"Invalid url '{new_value}'")

    @property
    def base64(self) -> str:
        """Return base64 of fatoora
        Returns:
            str: base64 of fatoora
        """
        tlv_as_byte_array = self.tags.to_byte_array()
        tlv_as_base64 = base64.b64encode(tlv_as_byte_array).decode()
        return tlv_as_base64

    @validate_arguments
    def qrcode(self, filename: str) -> None:
        """Generate qr code for fatoora
        Args:
            filename (str): The path you want to put the qr code in
        """
        qr_code = qrcode.make(self.qrcode_url or self.base64)
        qr_code.save(filename)

    @property
    def hash(self) -> str:
        """Return the hash of fatoora
        Returns:
            str: hash hexdigest
        """
        return sha256(self.base64.encode()).hexdigest()

    def dict(self) -> dict:
        """Return fatoora details as dictionary
        Returns:
            dict: fatoora details
        """
        return self.__class__.base2dict(self.base64)

    def json(self) -> str:
        """Return fatoora details as json
        Returns:
            str: fatoora details
        """
        return json.dumps(self.dict())

