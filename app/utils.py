import pandas as pd

def load_data(path):
    df = pd.read_csv(path, sep=',')
    return df.to_dict(orient='records')

def prepare_text(doc):
    return f"{doc['exercise_name']} , {doc['type_of_activity']}, {doc['type_of_equipment']} , {doc['body_part']} , {doc['type']} , {doc['muscle_groups_activated']} , {doc['instructions']}"
