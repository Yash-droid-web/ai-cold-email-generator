import streamlit as st
import anthropic

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Cold Email Generator",
    page_icon="✉️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Card-style containers */
    .card {
        background: #1a1d27;
        border: 1px solid #2d3147;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Section headers */
    .section-title {
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #7c83a8;
        margin-bottom: 0.5rem;
    }

    /* Output email box */
    .email-output {
        background: #12151f;
        border: 1px solid #3d4266;
        border-radius: 10px;
        padding: 1.5rem;
        font-family: 'Georgia', serif;
        font-size: 0.95rem;
        line-height: 1.8;
        color: #e2e8f0;
        white-space: pre-wrap;
    }

    /* Badge pills for tone */
    div[data-testid="stHorizontalBlock"] .stButton button {
        border-radius: 20px;
        font-size: 0.8rem;
        padding: 0.3rem 1rem;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border: none;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.05em;
        padding: 0.6rem 2rem;
        width: 100%;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        transform: translateY(-1px);
    }

    /* Input fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: #12151f !important;
        border: 1px solid #2d3147 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }
    textarea { min-height: 90px !important; }

    /* Hide Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## ✉️ AI Cold Email Generator")
st.markdown(
    "<span style='color:#7c83a8;font-size:0.9rem'>"
    "Craft personalised cold emails in seconds using AI.</span>",
    unsafe_allow_html=True,
)
st.divider()

# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-title">About the Recipient</p>', unsafe_allow_html=True)
    recipient_name    = st.text_input("Recipient Name", placeholder="e.g. Sarah Johnson")
    company_name      = st.text_input("Company / Organisation", placeholder="e.g. Stripe")
    recipient_role    = st.text_input("Their Job Title", placeholder="e.g. Head of Engineering")
    company_context   = st.text_area(
        "What does their company do? (optional)",
        placeholder="e.g. Stripe builds payment infrastructure for the internet…",
        height=90,
    )

with col2:
    st.markdown('<p class="section-title">About You</p>', unsafe_allow_html=True)
    sender_name       = st.text_input("Your Name", placeholder="e.g. Alex Smith")
    sender_role       = st.text_input("Your Role / Background", placeholder="e.g. Full-Stack Developer")
    goal              = st.text_area(
        "What is the goal of this email?",
        placeholder="e.g. I want to get a 30-min call to discuss a freelance opportunity…",
        height=90,
    )
    value_prop        = st.text_area(
        "Your value proposition (optional)",
        placeholder="e.g. I've built 3 payment integrations and cut checkout drop-off by 20%…",
        height=90,
    )

st.markdown("---")

# ── Tone & Length ─────────────────────────────────────────────────────────────
tcol1, tcol2 = st.columns(2)

with tcol1:
    st.markdown('<p class="section-title">Email Tone</p>', unsafe_allow_html=True)
    tone = st.selectbox(
        "Tone",
        ["Professional", "Conversational & Friendly", "Bold & Direct", "Warm & Empathetic"],
        label_visibility="collapsed",
    )

with tcol2:
    st.markdown('<p class="section-title">Email Length</p>', unsafe_allow_html=True)
    length = st.selectbox(
        "Length",
        ["Short (3–4 sentences)", "Medium (1–2 short paragraphs)", "Detailed (3+ paragraphs)"],
        label_visibility="collapsed",
    )

# ── Generate button ───────────────────────────────────────────────────────────
st.markdown("")
generate = st.button("✨  Generate Email", type="primary", use_container_width=True)

# ── Output ────────────────────────────────────────────────────────────────────
if generate:
    if not recipient_name or not company_name or not goal or not sender_name:
        st.warning("Please fill in at least: Recipient Name, Company, Your Name, and Goal.")
    else:
        prompt = f"""
You are an expert cold email copywriter. Write a cold email based on the details below.

RECIPIENT:
- Name: {recipient_name}
- Company: {company_name}
- Role: {recipient_role or 'Not specified'}
- Company context: {company_context or 'Not provided'}

SENDER:
- Name: {sender_name}
- Role / Background: {sender_role or 'Not specified'}
- Value proposition: {value_prop or 'Not provided'}

EMAIL GOAL: {goal}

TONE: {tone}
LENGTH: {length}

Rules:
- Write ONLY the email body (include Subject line at the top as "Subject: ...")
- Do NOT add any commentary before or after the email
- Be specific — avoid generic fluff
- End with a clear, low-friction call-to-action
- Keep it human and natural, not robotic
"""
        with st.spinner("Writing your email…"):
            try:
                client   = anthropic.Anthropic()
                response = client.messages.create(
                    model      = "claude-sonnet-4-20250514",
                    max_tokens = 800,
                    messages   = [{"role": "user", "content": prompt}],
                )
                email_text = response.content[0].text

                st.success("Email generated!")
                st.markdown('<p class="section-title" style="margin-top:1rem">Your Email</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="email-output">{email_text}</div>', unsafe_allow_html=True)

                st.markdown("")
                st.download_button(
                    label     = "⬇️  Download as .txt",
                    data      = email_text,
                    file_name = "cold_email.txt",
                    mime      = "text/plain",
                )

            except anthropic.AuthenticationError:
                st.error("❌ Invalid API key. Please check your ANTHROPIC_API_KEY environment variable.")
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
