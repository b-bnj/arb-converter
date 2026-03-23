# ARB Converter
A simple tool to move Flutter .arb files into CSVs for translators and merge them back without breaking your metadata.

## Instructions
1. Run the script: python main.py. This creates a workspace folder.
2. Input: Drop your .arb files into workspace/arbs_in.
3. Extract: Choose Option 1 in the menu to generate CSVs in workspace/csvs_out.
4. Translate: Give the CSVs to your translator. They only need to fill in the 3rd column.
5. Merge: Put the translated CSVs back into workspace/csvs_out and choose Option 2.
6. Output: Your new .arb files will be in workspace/arbs_out.

## Technical
- Python Version: Built and tested on Python 3.12.0. Should work fine on any modern Python 3.x version since it only uses the standard library.
- No Dependencies: No pip install required.
- Fallback logic: If a translation is left empty, the script just uses the original source text.

## Quick Note
If the workspace gets cluttered or a new batch is starting, just delete the entire workspace folder. The script will regenerate a clean one next time it runs. Just make sure the finished translations are moved out first, as I am not responsible for lost work.

## License
MIT. Do whatever you want with it.
