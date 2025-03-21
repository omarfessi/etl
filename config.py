file_path = "Base Défauts.xlsx"
sheet_name = "Base"
columns_renaming_mapping = {
    "Date": "date",
    "Matricule Controleur": "matricule_controleur",
    "Nom Controleur": "nom_controleur",
    "Matricule Op": "matricule_operateur",
    "Nom Opérateur": "nom_operateur",
    "Groupe": "groupe",
    "Machine": "machine",
    "Code faute": "code_faute",
    "Description de faute": "description_faute",
    "Nr de fil": "nr_fil",
    "Détecter par": "detecte_par",
    "Série": "serie",
    "Nb de faute": "nb_faute",
}
dtype_dict = {
    "Date": "datetime64[ns]",
    "Matricule Controleur": "float64",
    "Nom Controleur": "string",
    "Matricule Op": "float64",
    "Nom Opérateur": "string",
    "Groupe": "string",
    "Machine": "float64",
    "Code faute": "float64",
    "Description de faute": "string",
    "Nr de fil": "string",
    "Détecter par": "string",
    "Série": "string",
    "Nb de faute": "float64",
}
