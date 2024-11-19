import json

from app.schemas.data_country import Country


json_data = """
 {
  "valid_countries": [
    {
      "name": "Afghanistan",
      "alpha_code": "AF"
    },
    {
      "name": "Albania",
      "alpha_code": "AL"
    },
    {
      "name": "Algeria",
      "alpha_code": "DZ"
    },
    {
      "name": "Andorra",
      "alpha_code": "AD"
    },
    {
      "name": "Angola",
      "alpha_code": "AO"
    },
    {
      "name": "Antigua and Barbuda",
      "alpha_code": "AG"
    },
    {
      "name": "Argentina",
      "alpha_code": "AR"
    },
    {
      "name": "Armenia",
      "alpha_code": "AM"
    },
    {
      "name": "Australia",
      "alpha_code": "AU"
    },
    {
      "name": "Austria",
      "alpha_code": "AT"
    },
    {
      "name": "Azerbaijan",
      "alpha_code": "AZ"
    },
    {
      "name": "Bahamas",
      "alpha_code": "BS"
    },
    {
      "name": "Bahrain",
      "alpha_code": "BH"
    },
    {
      "name": "Bangladesh",
      "alpha_code": "BD"
    },
    {
      "name": "Barbados",
      "alpha_code": "BB"
    },
    {
      "name": "Belarus",
      "alpha_code": "BY"
    },
    {
      "name": "Belgium",
      "alpha_code": "BE"
    },
    {
      "name": "Belize",
      "alpha_code": "BZ"
    },
    {
      "name": "Benin",
      "alpha_code": "BJ"
    },
    {
      "name": "Bhutan",
      "alpha_code": "BT"
    },
    {
      "name": "Bolivia",
      "alpha_code": "BO"
    },
    {
      "name": "Bosnia and Herzegovina",
      "alpha_code": "BA"
    },
    {
      "name": "Botswana",
      "alpha_code": "BW"
    },
    {
      "name": "Brazil",
      "alpha_code": "BR"
    },
    {
      "name": "Brunei",
      "alpha_code": "BN"
    },
    {
      "name": "Bulgaria",
      "alpha_code": "BG"
    },
    {
      "name": "Burkina Faso",
      "alpha_code": "BF"
    },
    {
      "name": "Burundi",
      "alpha_code": "BI"
    },
    {
      "name": "Cabo Verde",
      "alpha_code": "CV"
    },
    {
      "name": "Cambodia",
      "alpha_code": "KH"
    },
    {
      "name": "Cameroon",
      "alpha_code": "CM"
    },
    {
      "name": "Canada",
      "alpha_code": "CA"
    },
    {
      "name": "Central African Republic",
      "alpha_code": "CF"
    },
    {
      "name": "Chad",
      "alpha_code": "TD"
    },
    {
      "name": "Chile",
      "alpha_code": "CL"
    },
    {
      "name": "China",
      "alpha_code": "CN"
    },
    {
      "name": "Colombia",
      "alpha_code": "CO"
    },
    {
      "name": "Comoros",
      "alpha_code": "KM"
    },
    {
      "name": "Congo, Democratic Republic of the",
      "alpha_code": "CD"
    },
    {
      "name": "Congo, Republic of the",
      "alpha_code": "CG"
    },
    {
      "name": "Costa Rica",
      "alpha_code": "CR"
    },
    {
      "name": "Croatia",
      "alpha_code": "HR"
    },
    {
      "name": "Cuba",
      "alpha_code": "CU"
    },
    {
      "name": "Cyprus",
      "alpha_code": "CY"
    },
    {
      "name": "Czech Republic",
      "alpha_code": "CZ"
    },
    {
      "name": "Denmark",
      "alpha_code": "DK"
    },
    {
      "name": "Djibouti",
      "alpha_code": "DJ"
    },
    {
      "name": "Dominica",
      "alpha_code": "DM"
    },
    {
      "name": "Dominican Republic",
      "alpha_code": "DO"
    },
    {
      "name": "East Timor (Timor-Leste)",
      "alpha_code": "TL"
    },
    {
      "name": "Ecuador",
      "alpha_code": "EC"
    },
    {
      "name": "Egypt",
      "alpha_code": "EG"
    },
    {
      "name": "El Salvador",
      "alpha_code": "SV"
    },
    {
      "name": "Equatorial Guinea",
      "alpha_code": "GQ"
    },
    {
      "name": "Eritrea",
      "alpha_code": "ER"
    },
    {
      "name": "Estonia",
      "alpha_code": "EE"
    },
    {
      "name": "Eswatini",
      "alpha_code": "SZ"
    },
    {
      "name": "Ethiopia",
      "alpha_code": "ET"
    },
    {
      "name": "Fiji",
      "alpha_code": "FJ"
    },
    {
      "name": "Finland",
      "alpha_code": "FI"
    },
    {
      "name": "France",
      "alpha_code": "FR"
    },
    {
      "name": "Gabon",
      "alpha_code": "GA"
    },
    {
      "name": "Gambia",
      "alpha_code": "GM"
    },
    {
      "name": "Georgia",
      "alpha_code": "GE"
    },
    {
      "name": "Germany",
      "alpha_code": "DE"
    },
    {
      "name": "Ghana",
      "alpha_code": "GH"
    },
    {
      "name": "Greece",
      "alpha_code": "GR"
    },
    {
      "name": "Grenada",
      "alpha_code": "GD"
    },
    {
      "name": "Guatemala",
      "alpha_code": "GT"
    },
    {
      "name": "Guinea",
      "alpha_code": "GN"
    },
    {
      "name": "Guinea-Bissau",
      "alpha_code": "GW"
    },
    {
      "name": "Guyana",
      "alpha_code": "GY"
    },
    {
      "name": "Haiti",
      "alpha_code": "HT"
    },
    {
      "name": "Honduras",
      "alpha_code": "HN"
    },
    {
      "name": "Hungary",
      "alpha_code": "HU"
    },
    {
      "name": "Iceland",
      "alpha_code": "IS"
    },
    {
      "name": "India",
      "alpha_code": "IN"
    },
    {
      "name": "Indonesia",
      "alpha_code": "ID"
    },
    {
      "name": "Iran",
      "alpha_code": "IR"
    },
    {
      "name": "Iraq",
      "alpha_code": "IQ"
    },
    {
      "name": "Ireland",
      "alpha_code": "IE"
    },
    {
      "name": "Israel",
      "alpha_code": "IL"
    },
    {
      "name": "Italy",
      "alpha_code": "IT"
    },
    {
      "name": "Ivory Coast",
      "alpha_code": "CI"
    },
    {
      "name": "Jamaica",
      "alpha_code": "JM"
    },
    {
      "name": "Japan",
      "alpha_code": "JP"
    },
    {
      "name": "Jordan",
      "alpha_code": "JO"
    },
    {
      "name": "Kazakhstan",
      "alpha_code": "KZ"
    },
    {
      "name": "Kenya",
      "alpha_code": "KE"
    },
    {
      "name": "Kiribati",
      "alpha_code": "KI"
    },
    {
      "name": "Korea, North",
      "alpha_code": "KP"
    },
    {
      "name": "Korea, South",
      "alpha_code": "KR"
    },
    {
      "name": "Kosovo",
      "alpha_code": "XK"
    },
    {
      "name": "Kuwait",
      "alpha_code": "KW"
    },
    {
      "name": "Kyrgyzstan",
      "alpha_code": "KG"
    },
    {
      "name": "Laos",
      "alpha_code": "LA"
    },
    {
      "name": "Latvia",
      "alpha_code": "LV"
    },
    {
      "name": "Lebanon",
      "alpha_code": "LB"
    },
    {
      "name": "Lesotho",
      "alpha_code": "LS"
    },
    {
      "name": "Liberia",
      "alpha_code": "LR"
    },
    {
      "name": "Libya",
      "alpha_code": "LY"
    },
    {
      "name": "Liechtenstein",
      "alpha_code": "LI"
    },
    {
      "name": "Lithuania",
      "alpha_code": "LT"
    },
    {
      "name": "Luxembourg",
      "alpha_code": "LU"
    },
    {
      "name": "Madagascar",
      "alpha_code": "MG"
    },
    {
      "name": "Malawi",
      "alpha_code": "MW"
    },
    {
      "name": "Malaysia",
      "alpha_code": "MY"
    },
    {
      "name": "Maldives",
      "alpha_code": "MV"
    },
    {
      "name": "Mali",
      "alpha_code": "ML"
    },
    {
      "name": "Malta",
      "alpha_code": "MT"
    },
    {
      "name": "Marshall Islands",
      "alpha_code": "MH"
    },
    {
      "name": "Mauritania",
      "alpha_code": "MR"
    },
    {
      "name": "Mauritius",
      "alpha_code": "MU"
    },
    {
      "name": "Mexico",
      "alpha_code": "MX"
    },
    {
      "name": "Micronesia",
      "alpha_code": "FM"
    },
    {
      "name": "Moldova",
      "alpha_code": "MD"
    },
    {
      "name": "Monaco",
      "alpha_code": "MC"
    },
    {
      "name": "Mongolia",
      "alpha_code": "MN"
    },
    {
      "name": "Montenegro",
      "alpha_code": "ME"
    },
    {
      "name": "Morocco",
      "alpha_code": "MA"
    },
    {
      "name": "Mozambique",
      "alpha_code": "MZ"
    },
    {
      "name": "Myanmar (Burma)",
      "alpha_code": "MM"
    },
    {
      "name": "Namibia",
      "alpha_code": "NA"
    },
    {
      "name": "Nauru",
      "alpha_code": "NR"
    },
    {
      "name": "Nepal",
      "alpha_code": "NP"
    },
    {
      "name": "Netherlands",
      "alpha_code": "NL"
    },
    {
      "name": "New Zealand",
      "alpha_code": "NZ"
    },
    {
      "name": "Nicaragua",
      "alpha_code": "NI"
    },
    {
      "name": "Niger",
      "alpha_code": "NE"
    },
    {
      "name": "Nigeria",
      "alpha_code": "NG"
    },
    {
      "name": "North Macedonia",
      "alpha_code": "MK"
    },
    {
      "name": "Norway",
      "alpha_code": "NO"
    },
    {
      "name": "Oman",
      "alpha_code": "OM"
    },
    {
      "name": "Pakistan",
      "alpha_code": "PK"
    },
    {
      "name": "Palau",
      "alpha_code": "PW"
    },
    {
      "name": "Panama",
      "alpha_code": "PA"
    },
    {
      "name": "Papua New Guinea",
      "alpha_code": "PG"
    },
    {
      "name": "Paraguay",
      "alpha_code": "PY"
    },
    {
      "name": "Peru",
      "alpha_code": "PE"
    },
    {
      "name": "Philippines",
      "alpha_code": "PH"
    },
    {
      "name": "Poland",
      "alpha_code": "PL"
    },
    {
      "name": "Portugal",
      "alpha_code": "PT"
    },
    {
      "name": "Qatar",
      "alpha_code": "QA"
    },
    {
      "name": "Romania",
      "alpha_code": "RO"
    },
    {
      "name": "Russia",
      "alpha_code": "RU"
    },
    {
      "name": "Rwanda",
      "alpha_code": "RW"
    },
    {
      "name": "Saint Kitts and Nevis",
      "alpha_code": "KN"
    },
    {
      "name": "Saint Lucia",
      "alpha_code": "LC"
    },
    {
      "name": "Saint Vincent and the Grenadines",
      "alpha_code": "VC"
    },
    {
      "name": "Samoa",
      "alpha_code": "WS"
    },
    {
      "name": "San Marino",
      "alpha_code": "SM"
    },
    {
      "name": "Sao Tome and Principe",
      "alpha_code": "ST"
    },
    {
      "name": "Saudi Arabia",
      "alpha_code": "SA"
    },
    {
      "name": "Senegal",
      "alpha_code": "SN"
    },
    {
      "name": "Serbia",
      "alpha_code": "RS"
    },
    {
      "name": "Seychelles",
      "alpha_code": "SC"
    },
    {
      "name": "Sierra Leone",
      "alpha_code": "SL"
    },
    {
      "name": "Singapore",
      "alpha_code": "SG"
    },
    {
      "name": "Slovakia",
      "alpha_code": "SK"
    },
    {
      "name": "Slovenia",
      "alpha_code": "SI"
    },
    {
      "name": "Solomon Islands",
      "alpha_code": "SB"
    },
    {
      "name": "Somalia",
      "alpha_code": "SO"
    },
    {
      "name": "South Africa",
      "alpha_code": "ZA"
    },
    {
      "name": "South Sudan",
      "alpha_code": "SS"
    },
    {
      "name": "Spain",
      "alpha_code": "ES"
    },
    {
      "name": "Sri Lanka",
      "alpha_code": "LK"
    },
    {
      "name": "Sudan",
      "alpha_code": "SD"
    },
    {
      "name": "Suriname",
      "alpha_code": "SR"
    },
    {
      "name": "Sweden",
      "alpha_code": "SE"
    },
    {
      "name": "Switzerland",
      "alpha_code": "CH"
    },
    {
      "name": "Syria",
      "alpha_code": "SY"
    },
    {
      "name": "Taiwan",
      "alpha_code": "TW"
    },
    {
      "name": "Tajikistan",
      "alpha_code": "TJ"
    },
    {
      "name": "Tanzania",
      "alpha_code": "TZ"
    },
    {
      "name": "Thailand",
      "alpha_code": "TH"
    },
    {
      "name": "Togo",
      "alpha_code": "TG"
    },
    {
      "name": "Tonga",
      "alpha_code": "TO"
    },
    {
      "name": "Trinidad and Tobago",
      "alpha_code": "TT"
    },
    {
      "name": "Tunisia",
      "alpha_code": "TN"
    },
    {
      "name": "Turkey",
      "alpha_code": "TR"
    },
    {
      "name": "Turkmenistan",
      "alpha_code": "TM"
    },
    {
      "name": "Tuvalu",
      "alpha_code": "TV"
    },
    {
      "name": "Uganda",
      "alpha_code": "UG"
    },
    {
      "name": "Ukraine",
      "alpha_code": "UA"
    },
    {
      "name": "United Arab Emirates",
      "alpha_code": "AE"
    },
    {
      "name": "United Kingdom",
      "alpha_code": "GB"
    },
    {
      "name": "England",
      "alpha_code": "ENG"
    },
    {
      "name": "Northern Ireland",
      "alpha_code": "NIR"
    },
    {
      "name": "Scotland",
      "alpha_code": "SCT"
    },
    {
      "name": "Wales",
      "alpha_code": "WLS"
    },
    {
      "name": "United States",
      "alpha_code": "US"
    },
     {
      "name": "America",
      "alpha_code": "US"
    },
    {
      "name": "Uruguay",
      "alpha_code": "UY"
    },
    {
      "name": "Uzbekistan",
      "alpha_code": "UZ"
    },
    {
      "name": "Vanuatu",
      "alpha_code": "VU"
    },
    {
      "name": "Vatican City",
      "alpha_code": "VA"
    },
    {
      "name": "Venezuela",
      "alpha_code": "VE"
    },
    {
      "name": "Vietnam",
      "alpha_code": "VN"
    },
    {
      "name": "Yemen",
      "alpha_code": "YE"
    },
    {
      "name": "Zambia",
      "alpha_code": "ZM"
    },
    {
      "name": "Zimbabwe",
      "alpha_code": "ZW"
    }
  ]
}
"""

data = Country(**json.loads(json_data))


def get_countries() -> Country:
    return data
