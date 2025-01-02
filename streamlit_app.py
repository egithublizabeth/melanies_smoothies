# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session #used for Streamlit in Snowflake SiS
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

#used for Streamlit not in Snowflake SniS
cnx = st.connection("snowflake")
session = cnx.session()

#add a name box for smoothie orders
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

#session = get_active_session() #used for Streamlit in Snowflake SiS
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#UNCOMMENT below if you want to see the dataframe
#st.dataframe(data=my_dataframe, use_container_width=True)

#choose 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """', '"""+ name_on_order +"""')"""
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
