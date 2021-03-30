import pandas as pd
import numpy as np


class PartyHard:

    """
    Class that will transform and return valid party data from 2019 Spanish elections
    """

    def __init__(self, file):
        self.df_party = pd.read_excel(file)
        self._clean()

    def _clean(self):
        # Little trick with Numpy to concatenate multiple slices and generate a list of the index I want to remove
        # from the df_party data set.
        delete_columns_index = np.r_[3:11, 17:len(self.df_party.columns):2]

        # Remove columns
        self.df_party = self.df_party.drop(index=self.df_party.index[[0, 1, 2, 57, 58]], columns=self.df_party.iloc[:, delete_columns_index])

        # Delete long party name. Will be cleansed afterwards
        self.df_party.columns = self.df_party.iloc[0]

        # New names for data columns
        new_names_list = []
        index_name_dict = {
            0: "Community",
            1: "ProvinceCode",
            2: "Province",
            3: "Votes",
            4: "Valid",
            5: "PartyVotes",
            6: "Blank",
            7: "Null"
        }

        # Rewire/rename columns
        for index, column_name in enumerate(self.df_party.columns):
            if not isinstance(column_name, str):
                if np.isnan(column_name):
                    new_names_list.append(index_name_dict[index])
                    continue
            new_names_list.append(column_name)
        self.df_party.columns = new_names_list

        # Remove row after headers have been named
        self.df_party = self.df_party.drop(self.df_party.index[:2])

        # Reset row index
        self.df_party = self.df_party.reset_index(drop=True)

        # Normalize names
        self.df_party.rename(columns={"PODEMOS-IU": "PODEMOS",
                                      "ERC-SOBIRANISTES": "ERC",
                                      "Cs": "CIUDADANOS",
                                      "JxCAT-JUNTS": "JUNTS",
                                      "ECP-GUANYEM EL CANVI": "ENCOMUPODEM",
                                      "EAJ-PNV": "PNV",
                                      "EH Bildu": "BILDU",
                                      "MÁS PAÍS-EQUO": "MASPAISEQUO",
                                      "CUP-PR": "CUP",
                                      "PODEMOS-EU": "PODEMOSEU",
                                      "CCa-PNC-NC": "CCaPNCNC",
                                      "NA+": "NASUMA",
                                      "MÉS COMPROMÍS": "MESCOMPROMIS",
                                      "¡TERUEL EXISTE!": "TERUELEXISTE",
                                      "MÁS PAÍS": "MASPAIS",
                                      "RECORTES CERO-GV": "RECORTES0",
                                      "PUM+J": "PUMJ",
                                      "M PAÍS-CHA-EQUO": "MASPAISCHA",
                                      "MÉS-ESQUERRA": "MES",
                                      "AxSÍ": "ANDALUCIAPORSI",
                                      "AVANT ADELANTE LOS VERDES": "AVANTADELANTE",
                                      "I.Fem": "IFEM",
                                      "UIG-SOM-CUIDES": "UIGSOMCUIDES",
                                      "SOMOS REGIÓN": "SOMOSREGION",
                                      "AHORA CANARIAS": "AHORACANARIAS",
                                      "EXTREMADURA UNIDA": "EXTREMADURAUNIDA",
                                      "P-LIB": "PLIB",
                                      "UNIDOS SÍ-ACPS-Def": "UNIDOSSI",
                                      "FE de las JONS": "FALANGE",
                                      "UNIÓN REGIONALISTA": "UREGIONALISTA",
                                      "C 21": "C21",
                                      }, inplace=True)

    def getCleanedData(self):
        return self.df_party
