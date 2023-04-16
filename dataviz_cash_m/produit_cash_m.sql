CREATE TABLE abonnes_produit (
    id SERIAL PRIMARY KEY,
    periode	DATE,
    semaine VARCHAR(500),
    racine VARCHAR(500),
    nom_client VARCHAR(500),
    contact_date DATE,
    id_gestionnaire VARCHAR(500),
    nom_gestionnaire VARCHAR(500),
    statut VARCHAR(500),
    services VARCHAR(500),
    directions VARCHAR(500),
    agence VARCHAR(500),
    secteur VARCHAR(500),
    cible_anet VARCHAR(500),
    cible_tpe VARCHAR(500),
    cible_acs VARCHAR(500),
    cible_ecnps VARCHAR(500),
    cible_ramassage VARCHAR(500),
    cible_efacture VARCHAR(500),
    anet VARCHAR(500),
    tpe VARCHAR(500),
    acs VARCHAR(500),
    ecnps VARCHAR(500),
    ramassage VARCHAR(500),
    efacture VARCHAR(500)
);