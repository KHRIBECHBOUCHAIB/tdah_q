import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
        age_enfant = st.number_input("Âge de l'enfant", min_value=0, max_value=100, step=1)
        genre_enfant = st.radio("Genre de l'enfant", options=['Femme', 'Homme', 'Autre', 'Préfère ne pas dire'])

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
                "age_enfant": age_enfant,
                "genre_enfant": genre_enfant,
                "evaluations": evaluations
            }

# Function to save responses to a CSV file
def save_responses_to_csv(response, csv_file):
    evaluations = response.pop('evaluations')
    personal_info = response
    
    all_data = {**personal_info, **evaluations}
    data_df = pd.DataFrame([all_data])
    
    header = not os.path.exists(csv_file)
    data_df.to_csv(csv_file, mode='a', header=header, index=False)

# Function for downloading the CSV file
def download_csv_file(csv_file):
    with open(csv_file, "rb") as file:
        st.download_button(label="Télécharger les réponses", data=file, file_name=os.path.basename(csv_file), mime="text/csv")

# Function to display evaluation chart
def display_evaluation_chart(evaluations):
    eval_counts = pd.Series(list(evaluations.values())).value_counts().reindex(["Très insuffisant", "Insuffisant", "Satisfaisant", "Très satisfaisant"], fill_value=0)
    
    # Création du diagramme circulaire
    fig, ax = plt.subplots()
    ax.pie(eval_counts, labels=eval_counts.index, autopct='%1.1f%%', startangle=90, colors=['red', 'orange', 'yellow', 'green'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Répartition des Évaluations')
    st.pyplot(fig)


def main():
    st.title('Thermomètre comportemental')
    st.write("Veuillez remplir le questionnaire suivant pour évaluer les comportements.")

    # Définir le répertoire et le nom du fichier CSV
    csv_dir = 'C:/Users/khrib/OneDrive/Bureau/stage_clinicog/adhd_question'
    csv_file = os.path.join(csv_dir, 'evaluations_comportementales.csv')

    # Initialisation ou récupération de l'état de la soumission du formulaire
    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False

    form_response = questionnaire_form()
    if form_response:
        save_responses_to_csv(form_response, csv_file)
        st.session_state['submitted'] = True
        st.write("Merci d'avoir rempli le questionnaire. Vos réponses ont été enregistrées.")
    
    # Option pour l'utilisateur de visualiser les données
    if st.session_state['submitted']:
        if st.button("Afficher les données soumises"):
            try:
                df = pd.read_csv(csv_file)
                st.dataframe(df)
                download_csv_file(csv_file)
            except Exception as e:
                st.error("Erreur lors de la lecture du fichier CSV. Assurez-vous qu'il est formaté correctement.")
                st.error(f"Détails de l'erreur : {e}")
        
        if st.button("Afficher la répartition des évaluations"):
            try:
                # Supposons que 'evaluations' est toujours dans form_response grâce à la soumission
                # Ceci est juste pour la démonstration; ajustez selon la logique de votre application
                display_evaluation_chart(form_response["evaluations"])
            except Exception as e:
                st.error("Impossible d'afficher la répartition des évaluations.")
                st.error(f"Détails de l'erreur : {e}")

if __name__ == "__main__":
    main()