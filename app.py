import streamlit as st
from src.property import Property
from src.prompt import Prompt
from streamlit_tags import st_tags

st.set_page_config(page_title="Genimex", page_icon=":black_nib:", initial_sidebar_state="collapsed")
version = "0.0.1"
st.title('Genimex')
st.caption(f"Generative Immobilien Exposes, **v-{version}**")

"""
Genimex is a generative AI powered text redaction tool for Real Estate objects.

## :house: About the property

Feel free to fill as much information as you want. I will simply ignore the spaces you leave empty.
"""

property = Property()

with st.expander("**Overall property information**"):
    """
    Give me the basics.
    """
    property.general["type"] = st.selectbox("Property type", options=["Apartment", "Commercial", "Villa", "Penthouse", "Plot"])
    c1, c2, c3 = st.columns([0.5,0.25,0.25])
    property.general["living_space"] = c1.number_input("Living space (m²)", min_value=10, max_value=1000, value=None, step=1)
    property.general["plot_size"] = c2.number_input("Plot size (m²)", min_value=1, max_value=10000, value=None, step=1)
    property.general["terrace_space"] = c3.number_input("Terrace space (m²)", min_value=1, max_value=1000, value=None, step=1)



    c1, c2 = st.columns(2)
    property.general["rooms"] = c1.slider("Rooms", min_value=0, max_value=15, value=None, step=1)
    property.general["bathrooms"] = c2.slider("Bathrooms", min_value=0, max_value=10, value=None, step=1)

    property.general["current_state"] = c1.select_slider(
        "Current state",
        options=["Don't say", "Very bad", "Needs renovation", "Improvable", "Good", "Very good", "Brand new"],
        value= None,
    )
    property.general["segment"] = c2.select_slider(
        "Segment",
        options=["Don't say", "Low", "Medium-low", "Medium", "Medium-top", "Top", "Luxury", "Super luxury"],
        value= None,
    )

    c1, c2, c3 = st.columns(3)
    property.general["floor"] = c1.number_input("Floor (for apartments)", min_value=1, max_value=100, value=None, step=1)
    property.general["total_floors"] = c2.number_input("Floors (of the building)", min_value=1, max_value=100, value=None, step=1)
    property.general["levels"] = c3.multiselect("Levels (for houses)", options = ["-2", "-1", "Ground floor", "1", "2", "3", "4", "5"] )

    property.general["construction_year"] = c1.number_input("Construction year", min_value=1700, max_value=2030, value=None, step=1)
    property.general["renovation_year"] = c2.number_input("Renovation year", min_value=1700, max_value=2030, value=None, step=1)
    property.general["energy_certificate"] = c3.select_slider(
        "Energy certificate",
        options = ["Don't say", "H", "G", "F", "E", "D", "C", "B", "A", "A+"],
        value = None
        )

with st.expander("**Location**"):
    """
    Where are we talking about?
    """
    property.location["address"] = st.text_input("Address", value=None)
    property.location["neighbourhood"] = st.text_input(
        "Neighbourhood",
        help="Is the property located in a place with a remarkable name?",
        value=None
    )

    col1, col2 = st.columns(2)

    property.location["views"] = col1.multiselect(
        "Views",
        options = sorted(["Park", "Water", "Mountain", "City"]),
        help="Does it enjoy any particular views?",
    )
    property.location["orientation"] = col2.multiselect(
        "Orientation",
        options = ["North", "North-east", "East", "South-east", "South", "South-west", "West", "North-west", "360°"],
        help = "To which orientations do the windows face?"
    )
    property.location["close_to"] = st_tags(
        label='Enter close-by attractions:',
        text='Type and then press enter to add',
        suggestions=['airport', 'forest', 'center'],
        maxtags = 10
    )

with st.expander("**Equipment and facilities**"):
    """
    Now let's get into detail.
    """
    c1, c2 = st.columns(2)
    property.amenities["balconies"] = c1.slider("Balconies", min_value=0, max_value=10, value=None, step=1)
    property.amenities["parking_slots"] = c2.slider("Parking slots", min_value=0, value=None, max_value=10,step=1)

    equipment = st.multiselect(
        "What is it equiped with?",
        options = sorted(["Accesibility", "Basement", "Fireplace", "Lift", "Electric blinds", "Alarm", "Jacuzzi", "Floor to ceiling windows"])
    )
    more_equipment = st_tags(
        label='Enter other cool amenities of the house:',
        text='Type and then press enter to add',
        suggestions=['stalactites', 'fetish room'],
        maxtags=10
    )
    property.amenities["equipment"] = equipment + more_equipment

st.divider()
"""
## :black_nib: About my texts
You gotta tell how and what to write about.
"""
prompt = Prompt(property, model="gpt-4")

c1, c2 = st.columns(2)
prompt.paragraphs = c2.slider("How many paragraphs should each section have?", min_value=1, max_value=5, value=1, step=1)
prompt.sentences = c1.slider("How many approx. sentences should each paragraph have?", min_value=1, max_value=10, value=5, step=1)
prompt.voice_tone = c1.radio("Which voice tone should I use?", options = ["Relaxed", "Neutral", "Authoritative", "Excited"])
prompt.style = c2.radio("Which flavour?", options = ["Creative", "Simple", "Humorous", "Formal"])
with c1:
    prompt.use = st_tags(
            label='Any specific words you want me to **use**?',
            text='Type and then press enter to add',
            suggestions=['diplomatic', 'water'],
            maxtags=10
        )
with c2:
    prompt.avoid = st_tags(
        value=["boasts"],
        label='Any specific words you want me to **avoid**?',
        text='Type and then press enter to add',
        suggestions=['diplomatic', 'water'],
        maxtags=10
    )
st.divider()

"""
## :sparkles: Let's write!
"""
c1, c2 = st.columns(2)
if c1.button("Write summary section", use_container_width=True):
    prompt.gen_summary()
    st.write(prompt.launch_prompt("summary"))

if c2.button("Write location section", use_container_width=True):
    prompt.gen_location()
    st.write(prompt.launch_prompt("location"))



with st.sidebar:
    """
    # :bug: Current instance states 
    """
    with st.expander("Property"):
        if "property" in locals():
            st.write(vars(property))

    with st.expander("Prompt"):
        if "prompt" in locals():
            st.write(vars(prompt))