import streamlit as st
import pymongo
import git
import shutil
import os
import stat
import json
import pickle
import csv
import codecs
import item_genV2 as item_gen
from config import DB_CONNECTION
from bson.binary import Binary


def on_rm_error(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
    except:
        pass


def remove_color_codes(name):
    split = name.split("&")
    name = ""
    for value in split:
        name = name + value[1:]
    return name


def app():
    st.title("Admin Panel")
    st.text("Pull NEU item library:")
    repo_pull = st.button("Pull Repo")

    st.text("Delete NEU item library:")
    repo_delete = st.button("Delete Repo")

    st.text("Process items")
    repo_process = st.button("Process Repo")

    st.text("Create CSV for gallery")
    csv_create = st.button("Create CSV")

    st.text("Index Hypixel Item Library")
    index = st.button("Index")

    if repo_pull:
        with st.spinner('Downloading NEU Repo'):
            directory = os.path.dirname(os.path.realpath(__file__))
            shutil.rmtree(directory + "/item_lore", onerror=on_rm_error)
            os.mkdir(directory + "/item_lore")
            git.Git(directory + "/item_lore").clone(
                "https://github.com/NotEnoughUpdates/NotEnoughUpdates-REPO.git")

    if repo_delete:
        with st.spinner('Deleting NEU Repo'):
            directory = os.path.dirname(os.path.realpath(__file__))
            shutil.rmtree(directory + "/item_lore", onerror=on_rm_error)

    if repo_process:
        with st.spinner('Processing NEU Repo'):
            directory = os.path.dirname(os.path.realpath(__file__))
            petnums = json.load(open(
                directory + "/item_lore/NotEnoughUpdates-REPO/constants/petnums.json", encoding="utf8"))

            i = 0

            client = pymongo.MongoClient(DB_CONNECTION)
            db = client.hypixel
            db.items.drop()
            number_of_items = str(
                len(os.listdir(directory + "/item_lore/NotEnoughUpdates-REPO/items")))

            progress = st.empty()
            progress.info("Starting Image Generation for "
                          + number_of_items + " items.")

            for filename in os.listdir(directory + "/item_lore/NotEnoughUpdates-REPO/items"):
                i = i + 1

                f = os.path.join(
                    directory + "/item_lore/NotEnoughUpdates-REPO/items", filename)

                progress.info("Starting Image Generation for " + number_of_items
                              + " items.\n" + "Item Number " + str(i) + "/" + number_of_items)

                with open(f, encoding="utf8") as current_file:
                    data = json.load(current_file)
                    name = data["internalname"]
                    display_name = data["displayname"].replace("§", "&")
                    lore = data["lore"]
                    if ";" in name:
                        if data["itemid"] == "minecraft:skull":
                            pet_rarity = lore[-1][4:]
                            try:
                                pet_data = petnums[name[:-2]
                                                   ][pet_rarity]["100"]
                            except:
                                pet_data = petnums[name[:-2]
                                                   ]["LEGENDARY"]["100"]
                            lore2 = [display_name.format(LVL="100")]
                            original_name = display_name.format(LVL="100")
                            for value in pet_data["statNums"]:
                                if not str(pet_data["statNums"][value])[0] == "-":
                                    pet_data["statNums"][value] = "+" + \
                                        str(pet_data["statNums"][value])
                            for line in lore:
                                try:
                                    line = line.format(*pet_data["otherNums"])
                                except:
                                    pass
                                try:
                                    line = line.format(**pet_data["statNums"])
                                except:
                                    pass

                                lore2.append(line.replace("§", "&"))
                        else:
                            lore2 = [display_name]
                            original_name = lore[0].replace("§", "&")
                            for line in lore:
                                lore2.append(line.replace("§", "&"))
                    else:
                        # Lore Processing
                        lore2 = [display_name]
                        for line in lore:
                            lore2.append(line.replace("§", "&"))
                        original_name = display_name
                    original_name = remove_color_codes(original_name)
                    img = item_gen.render(lore2)
                    db.items.insert_one(
                        {'name': original_name, 'id': name, 'lore': lore2, 'image': Binary(pickle.dumps(img))})

    if csv_create:
        with st.spinner('Writing CSV'):
            client = pymongo.MongoClient(DB_CONNECTION)
            db = client.hypixel
            items = list(db.items.find())
            try:
                os.remove("data/item_data.csv")
            except:
                pass
            f = open('data/item_data.csv', 'w', encoding='UTF8')
            writer = csv.writer(f)
            for value in items:
                writer.writerow([value["name"], value["id"], codecs.encode(
                    value["image"], "base64").decode()])
    if index:
        with st.spinner('Indexing'):
            client = pymongo.MongoClient(DB_CONNECTION)
            db = client.hypixel
            db.items.drop_indexes()
            db.items.create_index([('name', 'text')], name='item-search')
