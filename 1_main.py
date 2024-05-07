# app URL
# https://rpg-random-names.streamlit.app/
from functions import *
import streamlit as st
import os

directory_path = "names/"
nations = [str(file)[:-4] for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

# Define the available nations


# Sidebar layout
st.sidebar.title("Options")
selected_nations = st.sidebar.multiselect("Select Nations", nations)
ngram_order = st.sidebar.slider("Randomness - lower means more random", 2, 5, 3)
# num_names = st.sidebar.slider("Number of Names", 1, 100, 10)
name_exist_flag = st.sidebar.checkbox("Only Non-existing Names", False)
opt1 = "Default"
opt2 = "List"
opt3 = "Table"
display_style = st.sidebar.radio("Display style", [opt1, opt2, opt3])


# Main content
st.title("RPG Name Generator App")
generate_button = st.button("Generate Names")

# IF at least one nation is selected, generate names
if selected_nations and generate_button:
    names = load_names(selected_nations)
    df, starts = prepare_ngrams(names, ngram_order)
    generated_names = generate_names_markov_chain(df, starts, names, ngram_order, 36, name_exist_flag, return_list=True)

    st.subheader("Generated Names:")
    # st.write(pd.DataFrame(generated_names))
    # generated_names # w streamlit można pisać jak w jpt - to się nazywa magic command
    # st.write(generated_names)

    if display_style == opt1:
        text_column1, text_column2, text_column3 = st.columns((1, 1, 1))
        with text_column1:
            for a in generated_names[::6]:
                st.markdown(f"***:orange[{a}]***")
            st.markdown(f"###")
            for a in generated_names[1::6]:
                st.markdown(f"***:orange[{a}]***")
        with text_column2:
            for a in generated_names[2::6]:
                st.markdown(f"***:orange[{a}]***")
            st.markdown(f"###")
            for a in generated_names[3::6]:
                st.markdown(f"***:orange[{a}]***")
        with text_column3:
            for a in generated_names[4::6]:
                st.markdown(f"***:orange[{a}]***")
            st.markdown(f"###")
            for a in generated_names[5::6]:
                st.markdown(f"***:orange[{a}]***")
    if display_style == opt2:
        st.write(generated_names)
    if display_style == opt3:
        st.dataframe(pd.DataFrame(np.array_split(np.array(generated_names), 3)).T,
                     height=500,
                     width=500)

else:
    st.info("Please select at least one nation.")
