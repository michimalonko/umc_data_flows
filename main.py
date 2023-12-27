import urllib.request
import pandas as pd
from tabula import read_pdf
# extract all the tables in the PDF file

path = " https://sipubv1.api.coordinador.cl/api/v1/cmg_files/anuales/2024/BA01T0002SE105T0002.tsv?user_key=f3cdad2758436a0a2c2c1fec92853de7"
path_barras = "https://api-infotecnica.coordinador.cl/v1/instalaciones/barras/reporte/?ordering=id"

def read_resolucion_exenta(path):
    abc = read_pdf(path)


def update_reporte_barras(path_barras):
    urllib.request.urlretrieve(path_barras, "reporte_barras.xlsx")


def crear_diccionario_barras():
    df = pd.read_excel("reporte_barras.xlsx", skiprows=6, usecols=["Nombre", "Nemotecnico"])
    return dict(df.values)


def diccionario_precio_estabilizado():
    df = pd.read_excel("reporte_barras.xlsx", skiprows=6, usecols=["Nemotecnico", ""])
    return dict(df.values)


def downloead_costos_marginales(año, barra_mnemo):
    path = f"https://sipubv1.api.coordinador.cl/api/v1/cmg_files/anuales/{año}/{barra_mnemo}.tsv?user_key="
    urllib.request.urlretrieve(path, "barra.tsv")


def diccionario_mnemotecnico_nombre(df):
    diccionario_barras = crear_diccionario_barras()
    barras = []

    for barra in df.index:
        if f"BA S/E {barra} 220kV BP1" in diccionario_barras:
            barras.append((diccionario_barras[f"BA S/E {barra} 220kV BP1"], barra))
        elif f"BA S/E {barra} 220KV BP1" in diccionario_barras:
            barras.append((diccionario_barras[f"BA S/E {barra} 220KV BP1"], barra))
        elif f"BA S/E {barra} 220KV BP1-1" in diccionario_barras:
            barras.append((diccionario_barras[f"BA S/E {barra} 220KV BP1-1"], barra))
        else:
            print(f"{barra} no encontrada")

    df = pd.DataFrame(barras, columns=["mnemotecnico", "nombre"])
    df.to_excel("diccionario_mnemo_nombre.xlsx", index=False)
    return dict(barras)


def read_resolucion_pe(path):
    df = pd.read_excel(path, sheet_name="Tabla 8", skiprows=8, header=None, usecols="F:M")
    df.columns = ["Barra", "Tension"] + [i for i in range(1, 7)]
    df = df.set_index("Barra")
    return df

def read_resolucion_pncp(path):
    pass

def update_input():
    diccionario_barras = crear_diccionario_barras()
    transform_file()


def valor_horario(hora, valores):
    if hora > 24:
        return valores[6]
    return valores[((hora - 1) // 4) + 1]


def transform_file():
    df_barra = pd.read_csv(f'barra.tsv', sep='\t', header=0)
    mnemotecnico = df_barra.iloc[1]["barra_referencia_mnemotecnico"]
    df_resolucion_pe = read_resolucion_pe("PE-reportes/1S_2023.xlsx")
    diccionario_mnemo_nombre = diccionario_mnemotecnico_nombre(df_resolucion_pe)
    df_resolucion_pncp = read_resolucion_pncp("PNCP-resoluciones")
    pe_barra = df_resolucion_pe.loc[diccionario_mnemo_nombre[mnemotecnico]]
    df_barra["PE_pesos"] = df_barra["hora"].apply(lambda x: valor_horario(x, pe_barra))


# update_input()
# print(crear_diccionario_barras())
#transform_file()
read_resolucion_exenta("resolucion_exenta_81.pdf")