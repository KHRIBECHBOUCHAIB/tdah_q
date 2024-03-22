import streamlit as st
import pandas as pd
import os

# Function to handle the questionnaire form
def questionnaire_form():
    with st.form("questionnaire_form"):
        # Informations about the evaluator
        nom_evaluateur = st.text_input("Nom de l'évaluateur")
        prenom_evaluateur = st.text_input("Prénom de l'évaluateur")

        # Information about the child
        nom_enfant = st.text_input("Nom de l'enfant")
        prenom_enfant = st.text_input("Prénom de l'enfant")
        age_enfant = st.number_input("Âge de l'enfant", min_value=6, max_value=16, step=1)
        relation_evaluateur_enfant = st.selectbox("Relation de l'évaluateur avec l'enfant", options=["Parent", "Tuteur", "Enseignant", "Professionnel de santé", "Autre"])

        # Evaluation criteria
        criteres = [
            "Organisation du matériel (ex. matériel rangé sur la table)",
            "Concentration sur tâches exigeantes (ex. reste sur une activité sans se distraire)",
            "Application des instructions (ex. suit une directive sans rappel)",
            "Réactivité modérée aux distractions externes (ex. ignore les bruits alentours lors d'une tâche)",
            "Fluidité dans les transitions (ex. change d'activité sans délai)",
            "Capacité à rester calme (ex. reste assis pendant une histoire)",
            "Gestion des mouvements et manipulations (ex. ne met pas d'objets à la bouche)",
            "Régulation des prises de parole (ex. parle à des moments appropriés)",
            "Adaptation sociale et émotionnelle (ex. joue sans exclure les autres)",
            "Engagement dans les jeux collectifs (ex. suit les règles du jeu)"
        ]

        # Generate evaluation options for each criterion
        evaluations = {critere: st.radio(critere, options=["Très insuffisant", "Insuffisant", "Satisfaisant", "Très satisfaisant"], key=critere) for critere in criteres}

        # Submit button
        submitted = st.form_submit_button("Soumettre")
        if submitted:
            return {
                "nom_evaluateur": nom_evaluateur,
                "prenom_evaluateur": prenom_evaluateur,
                "nom_enfant": nom_enfant,
                "prenom_enfant": prenom_enfant,
                "aelation_evaluateur_enfant": relation_evaluateur_enfant,
                **evaluations
            }
        
def apply_custom_css():
    st.markdown("""
    <style>
    /* Change the background color of the sidebar */
    .css-1d391kg { background-color: #f0f2f6; }
    
    /* Change the font style and color of the title and text */
    h1, .stText { font-family: Arial, sans-serif; color: #333; }
    
    /* Style the form */
    .stForm {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 20px;
    }

    /* Style the submit button */
    .stButton>button {
        border: 2px solid #4CAF50;
        border-radius: 20px;
        color: white;
        background-color: #4CAF50;
        padding: 10px 24px;
        cursor: pointer;
        font-size: 18px;
    }

    /* Style the submit button on hover */
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to save responses to a CSV file
def save_responses_to_csv(response, csv_file):
    data_df = pd.DataFrame([response])
    
    header = not os.path.exists(csv_file)
    data_df.to_csv(csv_file, mode='a', header=header, index=False)

def main():

    apply_custom_css()  # Apply the custom CSS
   # Définir le chemin relatif ou absolu vers l'image
    logo_path = 'images/logo.jpg'  
    # Afficher le logo de la clinique
    st.image(logo_path, use_column_width=True)
    st.title("Questionnaire sur le TDAH pour enfant")
    st.write("Veuillez remplir le questionnaire suivant pour évaluer les comportements.")
    # Define the directory and name of the CSV file
    csv_dir = 'data'  # Adjust the path according to your needs
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    csv_file = os.path.join(csv_dir, 'evaluations_comportementales.csv')

    response = questionnaire_form()
    if response:
        save_responses_to_csv(response, csv_file)
        st.success("Merci d'avoir rempli le questionnaire. Vos réponses ont été enregistrées.")
        
        # Allow user to download the CSV file
        with open(csv_file, "rb") as file:
            st.download_button(label="Télécharger les réponses", data=file, file_name=os.path.basename(csv_file), mime="text/csv")

if __name__ == "__main__":
    main()
