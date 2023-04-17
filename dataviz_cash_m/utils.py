import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from math import ceil


def equipement(abonne, cible):
    try:
        return (abonne / cible) * 100
    except (ValueError, ZeroDivisionError):
        return 0
    # return 0 if cible <= 0 else (abonne / cible)*100


# engine = create_engine(
#     "postgresql+psycopg2://postgres:password@localhost:5432/produit_cash_m",
#     isolation_level="SERIALIZABLE",
# )

engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5432/bnk",
    # isolation_level="SERIALIZABLE",
)
connection = engine.connect()

DBD = 'DBPPT'


class Donnees():
    def __init__(self, date):
        self.current_date = datetime.strptime(date, "%Y-%m-%d")
        self.current_month = self.current_date.strftime('%m')
        self.current_year = self.current_date.strftime('%Y')

        self.next_date = self.current_date + timedelta(days=31)
        self.next_month = self.next_date.strftime('%m')
        self.next_year = self.next_date.strftime('%Y')

        self.data = None

    @property
    def getPeriode(self):
        return f"periode BETWEEN '{self.current_year}-{self.current_month}-01' AND '{self.next_year}-{self.next_month}-01'"

    def getData(self):
        request = f"SELECT * FROM abonne_produit WHERE {self.getPeriode}"
        data = pd.read_sql(sql=text(request), con=connection)
        data = data.drop(columns=['id'])
        data['periode'] = data['periode'].astype(str)
        data['directions'] = data['directions'].apply(lambda x: x if x is not None else DBD)
        data['services'] = data['services'].apply(lambda x: x if x is not None else DBD)
        self.data = data

    def getPortefeuille(self):
        self.getData()
        df_portefeuille = self.data['directions'].value_counts()
        dict_portefeuille = []
        for i in range(df_portefeuille.shape[0]):
            _ = {'directions': str(df_portefeuille.index[i]), 'portefeuille': int(df_portefeuille.values[i])}
            dict_portefeuille.append(_)
        for dic in dict_portefeuille:
            if dic["directions"] == DBD:
                dic["directions"] = None
                dic["portefeuille"] = 0
        return dict_portefeuille

    def evoProduit(self, produit):
        request = f"""
                SELECT *
                FROM
                    ((SELECT periode, COUNT(racine) as abonne_corpo
                    FROM abonne_produit 
                    WHERE (periode BETWEEN '{self.current_year}-01-01' AND '{self.current_year}-12-31')
                    AND directions IS NOT NULL AND {produit}='Abonné'
                    GROUP BY periode
                    ORDER BY periode ASC) as x

                LEFT JOIN
                    (SELECT periode as periode2, COUNT(racine) as cible
                    FROM abonne_produit 
                    WHERE cible_{produit}='oui' AND (periode BETWEEN '{self.current_year}-01-01' AND '{self.current_year}-12-31')
                    GROUP BY periode) as z
                ON x.periode = z.periode2) as n

                LEFT JOIN
                    (SELECT periode as periode3, COUNT(racine) as abonne
                    FROM abonne_produit
                    WHERE {produit}='Abonné' AND (periode BETWEEN '{self.current_year}-01-01' AND '{self.current_year}-12-31')
                    GROUP BY periode3) as y
                ON n.periode = y.periode3
            """

        df = pd.read_sql(sql=text(request), con=connection)
        df = df.drop(columns=['periode2', 'periode3'])
        # df['croissance'] = 0
        df['equipement'] = np.vectorize(equipement)(df['abonne_corpo'], df['cible'])

        df['periode'] = df['periode'].astype(str)
        df = df.rename(columns={'periode': 'date'})
        df = df.rename(str.capitalize, axis='columns')

        # print(df)
        dict_df = []
        for j in range(df.shape[0]):
            _ = {
                df.columns[0]: df[df.columns[0]][j],
                df.columns[1]: int(df[df.columns[1]][j]),
                df.columns[2]: int(df[df.columns[2]][j]),
                df.columns[3]: int(df[df.columns[3]][j]),
                # df.columns[4]: int(df[df.columns[4]][j]),
                df.columns[4]: float(round(df[df.columns[4]][j], 2), )
            }
            dict_df.append(_)
        return dict_df

    def abonneCorpo(self, prod):
        x = self.data.groupby(by=["directions"]).count()[[f'{prod}']]
        x = x.drop(DBD)
        x = x.rename_axis('directions').reset_index()
        return x[f'{prod}'].sum()

    def getInfoProduct(self, produit):
        abonne = self.data[produit].value_counts()[0]
        corpo_abonne = self.data[self.data[f'{produit}'] == 'Abonné']
        corpo_abonne = corpo_abonne[corpo_abonne['directions'] != DBD][produit].value_counts()[0]
        cible = self.data[f'cible_{produit}'].value_counts()[0]
        non_abonne = cible - abonne
        try:
            equipement = (corpo_abonne / cible) * 100
        except ValueError:
            equipement = 0

        return [{
            'Abonne': int(abonne),
            'corpo_abonne': int(corpo_abonne),
            'Cible': int(cible),
            'Non Abonné': int(non_abonne),
            'Equipement': round(equipement, 2)
        }]

    def getResumeGraph(self, produit):
        request = f"""
                SELECT *
                FROM
                    ((SELECT COALESCE(directions, '{DBD}') as directions, COUNT(racine) as portefeuille
                    FROM abonne_produit 
                    WHERE {self.getPeriode}
                    GROUP BY directions
                    ORDER BY directions ASC) as x

                LEFT JOIN
                    (SELECT COALESCE(directions, '{DBD}') as directions2, COUNT(racine) as cible
                    FROM abonne_produit 
                    WHERE cible_{produit}='oui' AND {self.getPeriode}
                    GROUP BY directions2) as z
                ON x.directions = z.directions2) as n

                LEFT JOIN
                    (SELECT COALESCE(directions, '{DBD}') as directions3, COUNT(racine) as abonne
                    FROM abonne_produit 
                    WHERE {produit}='Abonné' AND {self.getPeriode}
                    GROUP BY directions3) as y
                ON n.directions = y.directions3
            """

        df = pd.read_sql(sql=text(request), con=connection)
        df = df.drop(columns=['directions2', 'directions3'])
        df['non_abonne'] = df['cible'] - df['abonne']
        df['equipement'] = np.vectorize(equipement)(df['abonne'], df['cible'])
        df = df.fillna(0)

        dict_df = []
        for j in range(df.shape[0]):
            # _ = {col: df[col][j] for col in df.columns}
            # print(_)
            _ = {
                df.columns[0]: df[df.columns[0]][j],
                df.columns[1]: int(df[df.columns[1]][j]),
                df.columns[2]: int(df[df.columns[2]][j]),
                df.columns[3]: int(df[df.columns[3]][j]),
                df.columns[4]: int(df[df.columns[4]][j]),
                df.columns[5]: float(round(df[df.columns[5]][j], 2), )
            }
            dict_df.append(_)

        for dic in dict_df:
            if dic["directions"] == DBD:
                dic["equipement"] = None
                dic["non_abonne"] = None
                dic["cible"] = None
                dic["portefeuille"] = None
        return dict_df

    def directionResumed(self, produit):
        request = f"""
                SELECT *
                FROM
                    ((SELECT COALESCE(directions, '{DBD}') as directions, COALESCE(services, 'DBPPT') as services,
                    COUNT(racine) as portefeuille
                    FROM abonne_produit 
                    WHERE {self.getPeriode}
                    GROUP BY directions, services
                    ORDER BY directions ASC) as x

                LEFT JOIN
                    (SELECT COUNT(racine) as cible, COALESCE(services, '{DBD}') as services2
                    FROM abonne_produit 
                    WHERE cible_{produit}='oui' AND {self.getPeriode}
                    GROUP BY services2) as z
                ON x.services = z.services2) as n

                LEFT JOIN
                    (SELECT COALESCE(services, '{DBD}') as services3,
                    COUNT(racine) as abonnés
                    FROM abonne_produit
                    WHERE {produit}='Abonné' AND {self.getPeriode}
                    GROUP BY services3) as y
                ON n.services = y.services3
            """

        df = pd.read_sql(sql=text(request), con=connection)
        df = df.rename(str.capitalize, axis='columns')
        df = df.drop(columns=['Services2', 'Services3'])

        df['Non Abonnés'] = df['Cible'] - df['Abonnés']
        df['Equipement'] = np.vectorize(equipement)(df['Abonnés'], df['Cible'])
        # df = df.rename_axis(['Directions', 'Services']).reset_index()
        df = df.fillna(0)

        dict_df = []
        for j in range(df.shape[0]):
            _ = {
                df.columns[0]: df[df.columns[0]][j],
                df.columns[1]: df[df.columns[1]][j],
                df.columns[2]: int(df[df.columns[2]][j]),
                df.columns[3]: int(df[df.columns[3]][j]),
                df.columns[4]: int(df[df.columns[4]][j]),
                df.columns[5]: int(df[df.columns[5]][j]),
                df.columns[6]: float(round(df[df.columns[6]][j], 2)),
            }
            dict_df.append(_)

        for dic in dict_df:
            if dic["Equipement"] > 200:
                dic["Equipement"] = None
                dic["Non Abonnés"] = None
                dic["Cible"] = None
                dic["Portefeuille"] = None
                dic["Services"] = None
        return dict_df

    def getNonAbonne(self, produit):
        request = f"""
            SELECT racine, nom_client, contact_date, Secteur, Nom_gestionnaire,
           COALESCE(directions, '{DBD}') as directions, COALESCE(services, 'DBPPT') as services,
           cible_{produit}, agence
           FROM abonne_produit
           WHERE cible_{produit}='oui' and {produit} IS NULL AND {self.getPeriode}
        """
        df = pd.read_sql(sql=text(request), con=connection)
        df = df.rename(columns={f'cible_{produit}': 'Ciblé'})
        df['contact_date'] = pd.to_datetime(df['contact_date'], format='%Y%m%d', errors='ignore')
        df['contact_date'] = df['contact_date'].apply(lambda date: date.strftime('%Y-%m-%d'))
        df = df.rename(str.capitalize, axis='columns')
        df = df.fillna('')

        dict_df = []
        for j in range(df.shape[0]):
            _ = {
                df.columns[0]: df[df.columns[0]][j],
                df.columns[1]: df[df.columns[1]][j],
                df.columns[2]: df[df.columns[2]][j],
                df.columns[3]: df[df.columns[3]][j],
                df.columns[4]: df[df.columns[4]][j],
                df.columns[5]: df[df.columns[5]][j],
                df.columns[6]: df[df.columns[6]][j],
                df.columns[7]: df[df.columns[7]][j],
                df.columns[8]: df[df.columns[8]][j],
            }
            dict_df.append(_)
        return dict_df

    def getInfoGestionnaire(self, produit):
        request = f"""
                SELECT *
                FROM
                    ((SELECT nom_gestionnaire as gestionnaires, COUNT(racine) as portefeuille
                    FROM abonne_produit 
                    WHERE {self.getPeriode}
                    GROUP BY gestionnaires
                    ORDER BY gestionnaires ASC) as x

                LEFT JOIN
                    (SELECT nom_gestionnaire as gestionnaires2, COUNT(racine) as cible
                    FROM abonne_produit 
                    WHERE cible_{produit}='oui' AND {self.getPeriode}
                    GROUP BY gestionnaires2) as z
                ON x.gestionnaires = z.gestionnaires2) as n

                LEFT JOIN
                    (SELECT nom_gestionnaire as gestionnaires3, COUNT(racine) as abonnés
                    FROM abonne_produit 
                    WHERE {produit}='Abonné' AND {self.getPeriode}
                    GROUP BY gestionnaires3) as y
                ON n.gestionnaires = y.gestionnaires3
            """
        df = pd.read_sql(sql=text(request), con=connection)
        df = df.rename(str.capitalize, axis='columns')
        df = df.drop(columns=['Gestionnaires2', 'Gestionnaires3'])

        df = df.dropna(subset=['Gestionnaires'])
        df = df.fillna(0)
        df['Non Abonnés'] = df['Cible'] - df['Abonnés']
        df['Equipement'] = np.vectorize(equipement)(df['Abonnés'], df['Cible'])
        df['Non Abonnés'] = df['Non Abonnés'].apply(lambda x: max(int(x), 0))
        df['Equipement'] = df['Equipement'].fillna(0)

        dict_df = []
        for j in range(df.shape[0]):
            _ = {
                df.columns[0]: df[df.columns[0]][j],
                df.columns[1]: int(df[df.columns[1]][j]),
                df.columns[2]: int(df[df.columns[2]][j]),
                df.columns[3]: int(df[df.columns[3]][j]),
                df.columns[4]: int(df[df.columns[4]][j]),
                df.columns[5]: float(round(df[df.columns[5]][j], 2)),
            }
            dict_df.append(_)
        return dict_df


class TableProduit():
    def __init__(self, date, day=0):
        self.date = date
        self.day = day

        self.start_date = None
        self.end_date = None
        self.data = None

    def abonneCorpo(self, prod):
        x = self.data.groupby(by=["directions"]).count()[[f'{prod}']]
        x = x.drop(DBD)
        x = x.rename_axis('directions').reset_index()
        return x[f'{prod}'].sum()

    def getDate(self):
        if self.date is not None:
            current_periode = datetime.strptime(self.date, "%Y-%m-%d")
            current_periode = current_periode - timedelta(days=self.day)
        else:
            self.date = datetime.now()

        current_month = current_periode.strftime('%m')
        current_year = current_periode.strftime('%Y')

        next_periode = current_periode + timedelta(days=31)
        next_month = next_periode.strftime('%m')
        next_year = next_periode.strftime('%Y')

        start_date = f'{current_year}-{current_month}-01'
        end_date = f'{next_year}-{next_month}-01'

        return start_date, end_date

    def getData(self):
        start_date, end_date = self.getDate()
        request = f"""
            SELECT periode, semaine, COALESCE(directions, '{DBD}') as directions, cible_anet, 
            cible_tpe, cible_acs, cible_ecnps, cible_ramassage, cible_efacture, anet, tpe, acs, 
            ecnps, ramassage, efacture
            FROM abonne_produit
            WHERE (periode BETWEEN '{start_date}' AND '{end_date}')
        """
        self.data = pd.read_sql(sql=text(request), con=connection)

    def compaProd(self):
        self.getData()
        if len(self.data.index) > 0:
            produits = list(self.data.columns[-6:])
            df = pd.DataFrame({'produits': produits})
            df['cible'] = df['produits'].apply(lambda prod: self.data[f'cible_{prod}'].value_counts())
            df['abonné'] = df['produits'].apply(lambda prod: self.data[prod].value_counts())
            df['abonné corpo'] = df['produits'].apply(self.abonneCorpo)
        else:
            produits = ['anet', 'tpe', 'acs', 'ecnps', 'ramassage', 'efacture']
            df = pd.DataFrame({'produits': produits})
            df['cible'] = 0
            df['abonné'] = 0
            df['abonné corpo'] = 0
        df['produits'] = df['produits'].apply(lambda prod: prod.upper())
        return df

    def getEquipement(self):
        if self.data is None:
            self.getData()

        produits = list(self.data.columns[-6:])
        df = None

        if len(self.data.index) > 0:
            for prod in produits:
                x = pd.DataFrame()
                x['abonné'] = self.data.groupby(by=["directions"]).count()[[f'{prod}']].drop(DBD)
                x['cible'] = self.data.groupby(by=["directions"]).count()[[f'cible_{prod}']]
                x['equipement_encours'] = np.vectorize(equipement)(x['abonné'], x['cible'])
                x = x.drop(columns=['cible', 'abonné']).T
                x['produit'] = f'{prod}'

                df = x if df is None else pd.concat([df, x])
                df = df.reset_index(drop=True)
                df['produit'] = df['produit'].apply(lambda x: str(x).upper())

        else:
            df = pd.DataFrame({'produit': produits})
            df['DGEI'] = 0
            df['DMS'] = 0
            df['DPME'] = 0
            df = df[['DGEI', 'DMS', 'DPME', 'produit']]
        return df


def tc(current_ab, last_ab):
    return 0 if last_ab <= 0 else ((current_ab - last_ab) / last_ab) * 100


def prodData(date=None):
    current_date = '2022-09-30'
    if date is None:
        date = '2022-09-30'

    current = TableProduit(date=current_date)
    current_df = current.compaProd()
    current_df['equipement'] = np.vectorize(equipement)(current_df['abonné corpo'], current_df['cible'])

    encours = TableProduit(date=date)
    encours_df = encours.compaProd()
    encours_df['equipement_encours'] = np.vectorize(equipement)(encours_df['abonné corpo'], encours_df['cible'])

    m_1 = TableProduit(date=date, day=31)
    m_1df = m_1.compaProd()
    m_1df = m_1df.drop(columns=['cible', 'abonné corpo'])

    n_1 = TableProduit(date=date, day=365)
    n_1df = n_1.compaProd()
    n_1df = n_1df.drop(columns=['cible', 'abonné corpo'])

    df = pd.merge(current_df, encours_df, how='inner', on='produits', suffixes=('', '_encours'))
    df = pd.merge(df, m_1df, how='inner', on='produits', suffixes=('', '_m1'))
    df = pd.merge(df, n_1df, how='inner', on='produits', suffixes=('', '_n1'))
    df['tc_m1'] = np.vectorize(tc)(df['abonné_encours'], df['abonné_m1'])
    df['tc_n1'] = np.vectorize(tc)(df['abonné_encours'], df['abonné_n1'])

    dict_df = []
    for j in range(df.shape[0]):
        _ = {
            df.columns[0]: df[df.columns[0]][j],
            df.columns[1]: int(df[df.columns[1]][j]),
            df.columns[2]: int(df[df.columns[2]][j]),
            df.columns[3]: int(df[df.columns[3]][j]),
            df.columns[4]: int(df[df.columns[4]][j]),
            df.columns[5]: int(df[df.columns[5]][j]),
            df.columns[6]: int(df[df.columns[6]][j]),
            df.columns[7]: int(df[df.columns[7]][j]),
            df.columns[8]: int(df[df.columns[8]][j]),
            df.columns[9]: int(df[df.columns[9]][j]),
            df.columns[10]: int(df[df.columns[10]][j]),
            df.columns[11]: float(round(df[df.columns[11]][j], 2)),
            df.columns[12]: float(round(df[df.columns[12]][j], 2)),
        }
        dict_df.append(_)

    return dict_df


def getProdEquipement(date=None):
    if date is None:
        date = '2022-09-22'
    df = TableProduit(date=date)
    df = df.getEquipement()
    dict_df = []
    for j in range(df.shape[0]):
        _ = {
            df.columns[0]: float(round(df[df.columns[0]][j], 2)),
            df.columns[1]: float(round(df[df.columns[1]][j], 2)),
            df.columns[2]: float(round(df[df.columns[2]][j], 2)),
            df.columns[3]: df[df.columns[3]][j],
        }
        dict_df.append(_)
    return dict_df
