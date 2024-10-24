import streamlit as st
import streamlit.components.v1 as components
from mistralai import Mistral

# Fonction pour générer une réponse à partir de l'API Mistral
def generate_response(user_input):
    model = "mistral-large-latest"
    
    # Initialiser le client Mistral avec la clé API
    client = Mistral(api_key=st.secrets["mistral_key"])

    # Appel à l'API pour générer une réponse
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "assistant",
                "content": "A chaque que tu vas répondre à une question réponds avec des punchlines en français",
            },
            {
                "role": "user",
                "content": user_input,
            },
        ]
    )
    return chat_response.choices[0].message.content

# Titre de l'application
st.title("Chatbot avec Streamlit")
st.write("Bienvenue sur l'interface de chatbot. Posez-moi des questions !")

# Initialisation de l'historique des conversations
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Formulaire d'entrée utilisateur
with st.form(key='chat_form', clear_on_submit=True):
    # Modification du placeholder avec un texte plus amusant
    user_input = st.text_input("Vous :", key="input", placeholder="Pose-moi une question et je réponds avec style !")
    submit_button = st.form_submit_button(label='Envoyer')

if submit_button and user_input:
    # Ajout d'un spinner pour indiquer que le bot réfléchit
    with st.spinner('Le bot réfléchit...'):
        response = generate_response(user_input)
    
    # Ajout de l'entrée utilisateur et de la réponse à l'historique
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Limitation de l'historique à 10 messages pour éviter une accumulation infinie
if len(st.session_state.chat_history) > 10:
    st.session_state.chat_history.pop(0)

# Affichage de l'historique des échanges avec avatars et styles
for sender, message in st.session_state.chat_history:
    if sender == "Vous":
        # Ajout d'un avatar pour l'utilisateur et affichage des messages dans une boîte
        st.image("user_icon.png", width=30)  # Remplacer par un chemin vers une icône utilisateur
        st.markdown(f'<div style="border:1px solid #ccc; padding:10px;">**{sender}:** {message}</div>', unsafe_allow_html=True)
    else:
        # Ajout d'un avatar pour le bot et affichage des messages dans une boîte
        st.image("bot_icon.png", width=30)  # Remplacer par un chemin vers une icône bot
        st.markdown(f'<div style="border:1px solid #f0f0f0; background-color:#f9f9f9; padding:10px;">*{sender}:* {message}</div>', unsafe_allow_html=True)

# Ajout d'un bouton pour réinitialiser l'historique
if st.button('Réinitialiser'):
    st.session_state.chat_history = []
