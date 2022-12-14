import pickle
import requests
import os
import os.path as pth

# from app.service.file_handle import append_data_2_pkl_file

from service.retrieval.crawler.collection_info_crawler import *
from service.retrieval.crawler.item_info_crawler import *
from service.retrieval.crawler.crawler_process import *
from service.retrieval.crawler.item_extractor import *

from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()

# Update storage
ITEMS_STORAGE = ENV.get("ITEMS_STORAGE")
COLLECTIONS_STORAGE = ENV.get("COLLECTIONS_STORAGE")
COLLECTIONS_TO_UPDATE = ENV.get("COLLECTIONS_TO_UPDATE")


def update_collection_info():
    """
        Update information from collection_to_update list
    """
    collections_list = read_crawler_file(COLLECTIONS_TO_UPDATE)
    for collection_id in collections_list.values():
        get_collection_info(collection_id)


def update_record():
    storage_list = read_crawler_file(COLLECTIONS_STORAGE)
    update_list = read_crawler_file(COLLECTIONS_TO_UPDATE)
    final_list = {}
    for k in update_list.keys():
        final_list[str(int(k) + len(storage_list))] = update_list[k]
    append_crawler_file(COLLECTIONS_STORAGE, final_list)
    write_crawler_file(COLLECTIONS_TO_UPDATE, {})


def crawl(num_of_collections):
    print('-------------------------------')
    print('GET COLLECTION ID')
    get_collections_id(num_of_collections)
    print('-------------------------------')
    print('COLLECTION ID TO WAITING')
    update_collections_id()
    print('-------------------------------')
    print('GET ITEM ID')
    update_collection_info()
    print('-------------------------------')
    print('GET EXTRACTED IMAGE')
    extract_all()
    print('-------------------------------')
    print('COLLECTION ID TO CURRENT')
    update_record()
