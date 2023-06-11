import openai
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="ChatBot")

# Sidebar contents
with st.sidebar:
    st.title('Diet Recommendation')

st.markdown("""
          <style>
          footer {visibility: hidden;}
          </style>""", unsafe_allow_html=True)

with st.sidebar:
    openAPIkey = st.text_input('Your OpenAI API KEY', type="password")

# Generate empty lists for generated and past.
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Please fill the following questions."]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# Questionnaire
with st.form(key='questionnaire'):
    user_AGE = st.text_input("What is your age?")
    user_TP = st.text_input("How long have you been trying to get pregnant?")
    user_MW = st.text_input("What week of your menstrual cycle will this be for?")
    user_PI = st.text_input("Do you have PCOS/Insulin resistance? (Yes/No)")
    user_E = st.text_input("Do you have Endometriosis? (Yes/No)")
    user_H = st.text_input("Do have Hasimotos? (Yes/No)")
    user_AO = st.text_input("Do your basal body temperatures stay above 98 after ovulation? (Yes/No)")
    user_BO = st.text_input("Are your basal body temperatures above 97.6 before ovulation (on average)? (Yes/No)")
    user_MS = st.text_input("How many days of menstrual bleeding do you have? (3 or less, 4, more than 4)")
    user_DR = st.text_input("Do you have any dietary restrictions or aversions?")
    submit_button = st.form_submit_button(label='Submit')

# Response output
def generate_response():
    #openai.api_key = "sk"
    openai.api_key = openAPIkey
    role = f"""
     Act as if you are a registered dietitian who specializes in nutrition for fertility. 
     you are a famous healthy cooking chef known for your simple, yet delicious and creative meals that taste amazing. 
     Flavor is important.
    Create a weekly menu plan, recipes, and shopping lists for a woman who is struggling to get pregnant. 
    The recipes should use all organic and or grass-fed ingredients where possible and whole foods. Include the macros for each meal along with the recipes.
    The menu plan should include three meals plus two snacks daily. Each daily menu should include 1600 calories, 30 G of fiber and 100 g of protein.
    Make sure the protein comes from a wide variety of sources. Breakfast will be the same every single day which is congee and I will provide the recipe for you.
    Also the first snack of the day will also be the same which will be grass-fed beef bone broth one cup, they can purchase this or make it.
    When You create the menus, double the recipe and count the leftovers as lunch for the following day.
    The goal is to make it very easy for the customer to significantly improve the quality of their diet. 
    write an intro telling why its chosen these foods, like because you have PCOS we chose low glycemic foods and 
    since you have Endometriosis we also added low FODMAP foods etc/
    Make sure to consider affordability as an important metric while you're choosing the recipes. 
    The user is {user_AGE} years old and has been trying to get pregnant for {user_TP}.
    The user is in week {user_MW} of their menstrual cycle.
    The user has PCOS/Insulin resistance: {user_PI}. if yes, add to prompt make all recipes have a low glycemic index
    The user has Endometriosis: {user_E}. If yes, make all recipes low fodmap.
    The user has Hasimotos: {user_H}. If yes, make all recipes low fodmap.
    The user's basal body temperatures stay above 98 after ovulation: {user_AO}. If no, add more warming foods if week 3 or 4 or the menstrual cycle. use the principals of Chinese herbal medicine food therapy to choose these warming foods.
    The user's basal body temperatures are above 97.6 before ovulation (on average): {user_BO}. If yes, add more cooling foods if week 1 or 2 or the menstrual cycle. Use the principles of Chinese herbal medicine food therapy to choose these cooling foods.
    The user has {user_MS} days of menstrual bleeding. If 3 or less, add more blood building and iron rich foods using the principles of Chinese medicine food therapy.
    The user's dietary restrictions or aversions are: {user_DR}. If the customer lists any restrictions or aversions remove them from the menu plans.
    """
    prompt = "Generate Diet Plan"
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

with response_container:
