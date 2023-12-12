import pandas as pd


class SeisLin(object):
    def __init__(self):
        self.Attr = pd.DataFrame()
        self.Surveys = pd.DataFrame(columns=['NbrLines', 'NbrBundesLines'])
        self.K1 = pd.DataFrame()
        self.K2 = pd.DataFrame()
        self.K3 = pd.DataFrame()

        self.loadAttrSeisLine()
        self.StatSurvey()
        self.OCR_Kategorien()

    def loadAttrSeisLine(self):
        sheet_name = 'lyrreflexionseismik_2023__2dsei'
        xlsLines = pd.read_excel(path, sheet_name)
        self.Attr = xlsLines

    def nbrSurveysContaingBundLinien(self):
        LinienBund = self.Attr[self.Attr['Owner'].astype(str).str[:9] == 'swisstopo']
        n = len(pd.unique(LinienBund['Survey']))
        self.nSurveyWithBundesLinien = n

    def StatSurvey(self):
        print('-----------------------------')
        print('*** Statistik surveys ***')
        # Nbr survey total
        n = len(pd.unique(self.Attr['Survey']))
        self.nSurvey = n
        self.nLines = len(self.Attr['LineName'])
        print('Insgesamt sind es {} survey, fur ein Total von {} Linien'.format(n,  len(self.Attr['LineName'])))

        # Nbr lines pro survey
        n = self.Attr.groupby('Survey')['LineName'].nunique()
        self.Surveys['NbrLines'] = n

        # Nbr Survey with bundeslinien
        LinienBund = self.Attr[self.Attr['Owner'].astype(str).str[:9] == 'swisstopo']
        n = len(pd.unique(LinienBund['Survey']))
        self.nSurveyWithBundesLinien = n

        # Nbr Bundeslinien pro survey
        n = LinienBund.groupby('Survey')['LineName'].nunique()
        self.Surveys['NbrBundesLines'] = n

        self.nBundesLinien = n.sum()
        self.nBundesSurvey = len(n)
        print('Die Bundeslinien umfassen {} Linien aus {} surveys'.format(n.sum(), len(n)))
    def OCR_Kategorien(self):
        def stat_Kat(Obj,txtKat):
            # k1 = self.Attr[self.Attr['KAT_TEST'] == txtKat]
            k = self.Attr[self.Attr['PotRepro'] == txtKat]
            S = k.groupby('Survey')['LineName'].nunique()
            Obj['nbrLines'] = S

            # B1 = k1[k1['Datenherr']== 'Bund']
            B = k[k['Owner'].astype(str).str[:9] == 'swisstopo']

            BS = B.groupby('Survey')['LineName'].nunique()
            Obj['nbrBundesLines'] = BS

            print('{} hat {} surveys mit {} Linien, davon {} Bundeslinien'.format(txtKat, len(S), S.sum(), BS.sum()))

        stat_Kat(self.K1, 'Kat1')
        stat_Kat(self.K2, 'Kat2')
        stat_Kat(self.K3, 'Kat3')
