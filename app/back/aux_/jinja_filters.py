# -*- coding: utf-8 -*-

from datetime import datetime
from markupsafe import escape
from app import app


@app.template_filter()
def formato_fecha(timestamp, format="%d/%m/%Y", max_char=None):
    try:
        fecha_texto = datetime.fromtimestamp(timestamp).strftime(format)
        if max_char:
            return fecha_texto[max_char:]
        return fecha_texto
    except:
        return ""


@app.template_filter()
def formato_decimal(number, decimals=None):
    if type(number) is str:
        try:
            number = float(number)
        except Exception as e:
            return number
    if type(number) is float or type(number) is int:
        if decimals:
            number = str(f"{number:,.{decimals}f}")
        else:
            num_decimals = str(number)[::-1].find('.')
            if int(number) - number == 0.0:
                number = str(f"{number:,.0f}")
            elif num_decimals >= 2:
                number = str(f"{number:,.2f}")
            else:
                number = str(f"{number:,.{num_decimals}f}")
    else:
        return number
    number = escape(
        str(number).replace(".", "|").replace(",", ".").replace("|", ",")
        )
    return number
