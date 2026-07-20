# -*- coding=utf-8 -*-
""" 
==================================================================================================================
CONFIGURATIONS DES SITES DE MESURE HYDROMÉTRIQUE POUR L'ENTRAÎNEMENT DU MODÈLE DE PRÉVISION DE RISQUE D'INONDATION
==================================================================================================================
"""

# URL base API HubEau hydrométrie
API_BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"

# mesures hydrométriques disponibles pour l'entraînement du modèle de prévision de risque d'inondation
AVAILABLE_MEASURES = ["QmnJ", "QmM", "HIXM", "HIXnJ", "QINM", "QINnJ", "QixM", "QIXnJ"]

# Sites de mesures hydrométries pour l'entraînement du modèle de prévision de risque d'inondation
SITES = {
    "Kogenheim":  {
        "code" : "A2360030",
        "site": "main",
        "river": "ill",
        "region": "grand-est",
		"stations": [
			{"code": "A236003001", "municipality" :"Kogenheim"}
		],
        "map": [
            {"latitude": "48.3370", "longitude": "7.5466"},
        ]
	},
    "Colmar-1":     {
        "code" : "A1580201", 
        "site": "main",
        "river": "launch",
        "region": "grand-est",
		"stations": [
            {"code": "A158020101", "municipality" :"Colmar"}, 
        ],
        "map": [
            {"latitude": "48.1025", "longitude": "7.3850"},
        ]
	},
    "Colmar-2":     {
        "code" : "A1610030", 
        "site": "main",
        "river": "ill",
        "region": "grand-est",
		"stations": [
            {"code": "A161003001", "municipality" :"Colmar"}, 
        ],
        "map": [
            {"latitude": "48.0887", "longitude": "7.4438"},
        ]
	},
    "Colmar-3":     {
        "code" : "A2220001", 
        "site": "main",
        "river": "fetch",
        "region": "grand-est",
		"stations": [
            {"code": "A222000101", "municipality" :"Colmar"}, 
        ],
        "map": [
            {"latitude": "48.1617", "longitude": "7.4485"},
        ]
	},
    "Selestat":   {
        "code" : "A2350200",
        "site": "main",
        "river": "giessen",
        "region": "grand-est",
		"stations": [
			{"code": "A235020001", "municipality" :"Selestat"},
			{"code": "A235020002", "municipality" :"Selestat"},
			{"code": "A235020003", "municipality" :"Selestat"}
		], 
        "map": [
            {"latitude": "48.2718", "longitude": "7.4598"},
            {"latitude": "48.2728", "longitude": "7.4566"},
            {"latitude": "48.2381", "longitude": "7.3915"}
        ]
	},
    "Ostheim":    {
        "code" : "A2140100",
        "site": "main",
        "river": "fetch",
        "region": "grand-est",
		"stations": [
			{"code": "A214010001", "municipality" :"Ostheim"}
		], 
        "map": [
            {"latitude": "48.2085", "longitude": "7.3976"},
        ]
	},
    "Waltenheim": {
        "code" : "A3480200",
        "site": "secondary",
        "river": "zorn",
        "region": "grand-est",
		"stations": [
			{"code": "A348020001", "municipality" :"Waltenheim-sur-Zorm"}
		], 
        "map": [
            {"latitude": "48.7496", "longitude": "7.6337"},
        ]
	},
    "Oberhof":    {
        "code" : "A3430210",
        "site": "secondary",
        "river": "zinsel-sud",
        "region": "grand-est",
		"stations": [
			{"code": "A343021001", "municipality" :"Eckartswiller"}
		], 
        "map": [
            {"latitude": "48.7996", "longitude": "7.3105"},
        ]
	},
    "Saverne":    { 
        "code" : "A3410200",
        "site": "secondary",
        "river": "zorn",
        "region": "grand-est",
		"stations": [
			{"code": "A341020001", "municipality" :"Saverne"}
		],
        "map": [
            {"latitude": "48.7380", "longitude": "7.3747"},
        ]
	},
}


if __name__ == "__main__":
    pass