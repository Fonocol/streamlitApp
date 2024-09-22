import streamlit as st
import time

# Titre de l'application
st.title("🤖 Chat Bot")

# Initialisation de l'historique des messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Fonction pour générer une réponse simple
def generate_response(user_input):
    time.sleep(1)  # Simulation du délai de réponse
    if "bonjour" in user_input.lower():
        return "Salut ! Comment puis-je t'aider aujourd'hui ?"
    elif "comment ça va" in user_input.lower():
        return "Je vais bien, merci ! Et toi ?"
    elif "bye" in user_input.lower():
        return "Au revoir ! À la prochaine."
    else:
        return "Désolé, je ne comprends pas cette question."

# Interface utilisateur
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Vous :")
    submit_button = st.form_submit_button("Envoyer")

# Si l'utilisateur envoie un message
if submit_button and user_input:
    # Ajouter le message utilisateur à l'historique
    st.session_state['messages'].append({"role": "user", "message": user_input})

    # Générer la réponse du bot
    with st.spinner("Le bot écrit..."):
        bot_response = generate_response(user_input)

    # Ajouter la réponse du bot à l'historique
    st.session_state['messages'].append({"role": "bot", "message": bot_response})

# Afficher l'historique des messages
for chat in st.session_state['messages']:
    if chat['role'] == 'user':
        st.write(f"👤 **Vous**: {chat['message']}")
    else:
        st.write(f"🤖 **Bot**: {chat['message']}")
