def get_collection_of_words_coords_pages(collection_of_textract_responses):
    list_words, list_coordinates, list_pages = [], [], []
    for i in range(len(collection_of_textract_responses)):
        for block in collection_of_textract_responses[i]['Blocks']:
                if block["BlockType"] == "WORD":
                    for word in block["Text"].split():
                        list_words.append(word)
                        list_coordinates.append(block['Geometry']['BoundingBox'])
                        list_pages.append(block['Page'])
    return list_words, list_coordinates, list_pages

def get_collections_grouped_by_pages(list_words, list_coordinates, list_pages): 
    # Get the list with the whole information of the bounding boxes: (words, coordinates, pages)
    zip_list = list(zip(list_words, list_coordinates, list_pages))

    # Get the uniques pages
    unique_pages = list(set([z[2] for z in zip_list]))

    # Group the words and coordinates by pages
    grouped_words = [[list[0] for list in zip_list if list[2] == value] for value in unique_pages]
    grouped_coordinates = [[list[1] for list in zip_list if list[2] == value] for value in unique_pages]
    return grouped_words, grouped_coordinates