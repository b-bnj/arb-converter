def extract_translations(arb_data: dict) -> tuple:
    """
    Separates an ARB dictionary into translation strings and metadata.
    Returns a tuple: (translations_list, metadata_dict)
    """
    translations = []
    metadata = {}

    for key, value in arb_data.items():
        if key.startswith('@'):
            metadata[key] = value
        else:
            translations.append((key, value, ""))

    return translations, metadata

def merge_translations(csv_rows: list, base_metadata: dict) -> dict:
    """
    Recombines translated CSV rows with the original metadata into a new ARB dictionary.
    Falls back to the source text if the translation column is left empty.
    """
    merged_arb = {}
    
    for row in csv_rows:
        if len(row) >= 3:
            key = row[0]
            source_text = row[1]
            translation = row[2]
            
            final_value = translation if translation.strip() != "" else source_text
            merged_arb[key] = final_value
            
        elif len(row) == 2:
            key, value = row[0], row[1]
            merged_arb[key] = value

    for meta_key, meta_value in base_metadata.items():
        merged_arb[meta_key] = meta_value

    return merged_arb