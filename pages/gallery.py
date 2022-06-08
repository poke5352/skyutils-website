import streamlit as st
import csv
import math
import pymongo
import pickle
import codecs
from config import DB_CONNECTION, URL


@st.cache(ttl=600, show_spinner=False)
def get_data(search_query):
    client = pymongo.MongoClient(DB_CONNECTION)
    db = client.hypixel
    data = []
    for item in db.items.find({"$text": {"$search": search_query}}).limit(75):
        data.append(item)
    return data


@st.cache(ttl=600, show_spinner=False)
def get_item(item_id):
    client = pymongo.MongoClient(DB_CONNECTION)
    db = client.hypixel
    x = db.items.find_one({"id": item_id})
    return x


def app():
    query_params = st.experimental_get_query_params()
    if 'item' in query_params:
        if query_params['item'][0] == "home":
            pass
        else:
            x = get_item(query_params['item'][0])
            if x is None:
                st.title("Item Not Found")
            else:
                st.title(x["name"])
                st.image(pickle.loads(x["image"]))
                st.caption("Lore:")
                lore = []
                for value in x["lore"]:
                    if value == []:
                        lore.append("")
                    else:
                        lore.append(value)
                st.json(lore)

    else:
        st.title("Hypixel Item Gallery")
        st.caption(
            "Images generated from poke535's image generation algorithm with [NEU Item REPO](https://github.com/NotEnoughUpdates/NotEnoughUpdates-REPO) as input.")
        search = st.text_input("Search for item:")
        st.markdown("""---""")
        if 'page_number' not in st.session_state:
            query_params = st.experimental_get_query_params()
            if query_params == {}:
                st.session_state['page_number'] = 1
            if 'page' in query_params:
                st.session_state['page_number'] = int(query_params['page'][0])
            else:
                st.session_state['page_number'] = 1

        per_page = 100*2
        col1, _, _, col2, _, _, col3 = st.columns([3, 1, 1, 3, 1, 1, 3])
        con1 = col1.container()
        con2 = col2.container()
        con3 = col3.container()
        if search == "":
            csvreader = csv.reader(open('data/item_data.csv', encoding='UTF8'))
            rows = list(csvreader)[((st.session_state.page_number-1)*per_page)                                   :(per_page+((st.session_state.page_number-1)*per_page))]
            page_selector = map(str, list(range(1, math.ceil(
                len(list(csv.reader(open('data/item_data.csv', encoding='UTF8'))))/per_page)+1)))
        else:
            data = get_data(search)
            rows = []
            for value in data:
                rows.append([value["name"], value["id"], codecs.encode(
                    value["image"], "base64").decode()])
            page_selector = [1]
        i = 1
        e = 1
        for row in rows:
            e = e + 1
            if e % 2 == 0:
                if i == 1:
                    con1.image(pickle.loads(codecs.decode(
                        row[2].encode(), "base64")), use_column_width=True)
                    con1.write(
                        "[" + row[0] + "](" + URL + "/gallery/" + row[1] + ")")
                    con1.markdown("""---""")
                    i = 2
                elif i == 2:
                    con2.image(pickle.loads(codecs.decode(
                        row[2].encode(), "base64")), use_column_width=True)
                    con2.write(
                       "[" + row[0] + "](" + URL + "/gallery/" + row[1] + ")")
                    con2.markdown("""---""")
                    i = 3
                elif i == 3:
                    con3.image(pickle.loads(codecs.decode(
                        row[2].encode(), "base64")), use_column_width=True)
                    con3.write(
                        "[" + row[0] + "](" + URL + "/gallery/" + row[1] + ")")
                    con3.markdown("""---""")
                    i = 1
        last = st.session_state['page_number']
        st.session_state['page_number'] = int(
            st.selectbox("Page", page_selector))
        if last != st.session_state.page_number:
            st.experimental_rerun()
