import random
import streamlit as st

st.set_page_config(page_title="TVM Bot", page_icon="🤖")

# ---------------------------------------------------------------------------
# Knowledge base (same logic as the console version, tvm_bot.py)
# ---------------------------------------------------------------------------
intents = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "whats up", "what's up"],
        "responses": ["Hello! I'm TVM Bot 🤖", "Hey there! How can I help you today?", "Hi! Good to see you."],
    },
    "how_are_you": {
        "keywords": ["how are you", "hows it going", "how's it going"],
        "responses": ["I'm doing great, thanks for asking!", "All good here, just running on rules today!"],
    },
    "bot_identity": {
        "keywords": ["what is your name", "what's your name", "who are you"],
        "responses": ["I'm TVM Bot, nice to meet you!"],
    },
    "bot_creator": {
        "keywords": ["who made you", "who created you", "who built you"],
        "responses": ["I was built by Tim Visual as part of the DecodeLabs AI training."],
    },
    "capabilities": {
        "keywords": ["what can you do", "what do you do", "help"],
        "responses": ["I can chat using some basic rules — try greetings, jokes, or asking who made me."],
    },
    "joke": {
        "keywords": ["joke", "make me laugh", "something funny"],
        "responses": ["Why do programmers prefer dark mode? Because light attracts bugs!", "Why did the function break up with the loop? It felt used."],
        "followup": ("joke_again", "Want another one?"),
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "appreciate it"],
        "responses": ["You're welcome!", "Anytime!"],
    },
    "wellbeing_positive": {
        "keywords": ["i am good", "i'm good", "i am fine", "i'm fine", "i am great", "i'm great"],
        "responses": ["Glad to hear that!", "That's great!"],
    },
    "wellbeing_negative": {
        "keywords": ["i am sad", "i'm sad", "i am tired", "i'm tired", "not okay"],
        "responses": ["Sorry to hear that."],
        "followup": ("talk_about_it", "Want to talk about what's bothering you?"),
    },
    "compliment": {
        "keywords": ["you are smart", "you're smart", "good bot", "you're cool"],
        "responses": ["Aw, thank you!", "You're too kind!"],
    },
}

exit_words = ["bye", "goodbye", "exit", "quit", "see you"]
yes_words = ["yes", "yeah", "yep", "sure", "ok", "okay"]
no_words = ["no", "nope", "not really", "nah"]

# ---------------------------------------------------------------------------
# Session state — Streamlit reruns the whole script on every interaction,
# so conversation state (history, name, pending follow-up) has to live here
# instead of in plain local variables like the console version used.
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm TVM Bot 🤖. Type 'bye' anytime to end the chat."}
    ]
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "pending" not in st.session_state:
    st.session_state.pending = None
if "ended" not in st.session_state:
    st.session_state.ended = False


def get_response(raw_input_text: str) -> str:
    """Same control flow as the console bot's main loop, returning a reply
    instead of printing one."""
    clean_input = raw_input_text.lower().strip()

    if clean_input in exit_words:
        st.session_state.ended = True
        name_part = f", {st.session_state.user_name}" if st.session_state.user_name else ""
        return f"Goodbye{name_part}! 👋"

    if clean_input.startswith("my name is"):
        name_part = raw_input_text.strip()[len("my name is"):].strip()
        if name_part:
            st.session_state.user_name = name_part.title()
            return f"Nice to meet you, {st.session_state.user_name}!"
        return "Didn't catch that — try again?"

    if st.session_state.pending == "joke_again":
        st.session_state.pending = None
        if clean_input in yes_words:
            st.session_state.pending = "joke_again"
            return random.choice(intents["joke"]["responses"])
        if clean_input in no_words:
            return "No worries, let me know if you change your mind!"
        # falls through to normal intent matching below, same as the console version

    if st.session_state.pending == "talk_about_it":
        st.session_state.pending = None
        if clean_input in yes_words:
            return "I'm listening — go ahead."
        if clean_input in no_words:
            return "That's okay. I'm here if you change your mind."
        # falls through to normal intent matching below

    for intent in intents.values():
        if any(keyword in clean_input for keyword in intent["keywords"]):
            reply = random.choice(intent["responses"])
            if "followup" in intent:
                pending_key, followup_question = intent["followup"]
                st.session_state.pending = pending_key
                reply = f"{reply}\n\n{followup_question}"
            return reply

    return "I don't understand that yet."


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("🤖 TVM Bot")
st.caption("A rule-based chatbot — DecodeLabs AI Training, Project 1")

with st.sidebar:
    st.subheader("About")
    st.write(
        "TVM Bot matches your message against a dictionary of intents "
        "(keyword → response), with a couple of multi-turn follow-ups "
        "and simple name memory. No external AI model — every reply "
        "comes from a fixed rule."
    )
    if st.button("Restart conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm TVM Bot 🤖. Type 'bye' anytime to end the chat."}
        ]
        st.session_state.user_name = None
        st.session_state.pending = None
        st.session_state.ended = False
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.ended:
    st.chat_input("Chat ended — click Restart in the sidebar to chat again", disabled=True)
else:
    user_input = st.chat_input("Type a message...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        reply = get_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
