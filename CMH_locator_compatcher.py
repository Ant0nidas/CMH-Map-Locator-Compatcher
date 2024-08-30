import os
import re
import difflib

def display_welcome_message():
    ascii_art = """&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&% *   ,,*&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&(@. *&&&&&&&&&&&         &&&&&&&&&&&&&&&%%%%&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&      &%&&&&&&&&&&&&         @&&&&&&&&&&&%.       &&&&&&&&&&&&&&
&&&&&&&&&&&&&&&,..     &&&&&&&&&&&&&&&     #%&&&&&&&&&&&&@        &&&&&&&&&&&&&&
&&&&&&&&&&&&&&&.       &&&&&&&&&&&@&&@@&&@@@@@@&&&&&&&&&&@        &&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&@*  ,&&&&&&&&&&&                 (%&&&&&&&#.    ./&&&&&&&&&&&&&&
&&&&&&&&&&&&&&**********#@&&&&%*                 .&&&&&&%**********#@&&&&&&&&&&&
&&&&&&&&&&&.               @&&%*                  &&&&.               @&&&&&&&&&
&&&&&&&&&&&&@@@@@@@@@@@@@@&&&&&&@@@@@@@@@@@@@@@@@&&&&&&@@@@@@@@@@@@@@&@&&&&&&&&&
&&&&&&&&%%%%%%%%%%%%%%%%%%&%%&%%%%%%%%%%%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&&
&&&&&&&&&&&&&&&&&&(      /&&@/   ,&&&&&&&&&&&&.  .&&&/   #&&&&&&*   /%&&&&&&&&&&
&&&&&&&&&&&&&&(  ,@%%@* *&&&&&     &&&&&&&&&     @&&&#   @&&&&&%*   @&&&&&&&&&&&
&&&&&&&&&&&&&(  .%&&&&&&&&&&&&      .&&&&&#  #   &&&&%   &&&&&&%/   @&&&&&&&&&&&
&&&&&&&&&&&&&   *%&&&&&&&&&&&#  &&    &&%* .%@   &&&&%              &&&&&&&&&&&&
&&&&&&&&&&&&&    &&&&&&&&&&&%*  &&&    /  #%&&   @&&&#   &&&&&&%*   @&&&&&&&&&&&
&&&&&&&&&&&&&&    &%&&%&% @&&   &&&&/    &&&&#   @&&%/   @&&&&&%,   @&&&&&&&&&&&
&&&&&&&&&&&&&&&*      .%%&&&/  (&&&&&&  &&&&&*   .@&&   ,&&&&&&&   ,#&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"""
    print(ascii_art)
    print("\nWelcome to the CMH Map Locator Compatcher for Crusader Kings 3\nGitHub repository: https://github.com/Ant0nidas/CK3-Map-Locator-Compatcher\nJoin CMH on Discord: https://discord.gg/GuDjt9YQ\nPlease answer the prompts to continue:\n")

def get_user_input(prompt):
    """Prompt the user for input."""
    return input(prompt).strip().strip('"')

def list_files_with_suffix(directory, suffix):
    """List files in the directory that end with a specific suffix."""
    return [f for f in os.listdir(directory) if f.endswith(suffix)]

def choose_file_from_list(file_list):
    """Prompt the user to choose a file from the provided list."""
    for index, filename in enumerate(file_list, start=1):
        print(f"{index}: {filename}")
    choice = input("Please choose a file by entering the corresponding number: ")
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(file_list):
            return file_list[choice_index]
        else:
            print("Invalid selection. Please restart the script and try again.")
            exit()
    except ValueError:
        print("Invalid input. Please restart the script and try again.")
        exit()

def read_handplaced_locators(filepath):
    """Read the handplaced locators from the MA handplaced locators list.txt file."""
    with open(filepath, 'r') as file:
        locators = file.read().splitlines()
    return locators

def extract_id_blocks(filepath, locators):
    """Extract the ID blocks corresponding to the locators from the special_building_locators.txt file."""
    with open(filepath, 'r') as file:
        content = file.read()

    id_blocks = {}
    for locator in locators:
        pattern = re.compile(rf"(\t\t{{\n\t\t\tid={locator}\n\t\t\tposition=.*?\n\t\t}})", re.DOTALL)
        match = pattern.search(content)
        if match:
            id_blocks[locator] = match.group(1)
    
    return id_blocks

def compare_and_extract_id_blocks(mod_filepath, base_filepath):
    """Compare two locator files and extract ID blocks that differ."""
    print("Grabbing ID's. This may take a while...")
    
    with open(mod_filepath, 'r') as mod_file, open(base_filepath, 'r') as base_file:
        mod_content = mod_file.read()
        base_content = base_file.read()

    mod_ids = re.findall(r"(\t\t{\n\t\t\tid=\d+\n\t\t\tposition=.*?\n\t\t})", mod_content, re.DOTALL)
    base_ids = re.findall(r"(\t\t{\n\t\t\tid=\d+\n\t\t\tposition=.*?\n\t\t})", base_content, re.DOTALL)

    id_blocks = {}
    for mod_id_block in mod_ids:
        mod_id = re.search(r"id=(\d+)", mod_id_block).group(1)
        for base_id_block in base_ids:
            base_id = re.search(r"id=(\d+)", base_id_block).group(1)
            if mod_id == base_id and mod_id_block != base_id_block:
                id_blocks[mod_id] = mod_id_block
                break

    print("Successfully grabbed ID's.")
    return id_blocks

def replace_id_blocks(base_filepath, id_blocks, output_filepath):
    """Replace the matching ID blocks in the base special_building_locators.txt and create a new file."""
    with open(base_filepath, 'r') as file:
        content = file.read()

    for locator, block in id_blocks.items():
        pattern = re.compile(rf"(\t\t{{\n\t\t\tid={locator}\n\t\t\tposition=.*?\n\t\t}})", re.DOTALL)
        content = pattern.sub(block, content)

    with open(output_filepath, 'w') as file:
        file.write(content)
    
    print(f"New file '{output_filepath}' created with updated ID blocks.")

def main():
    display_welcome_message()

    # Step 1: Choose the method of ID grabbing
    method = get_user_input("Choose the method of ID grabbing:\n1: Provide path to file containing the IDs (recommended)\n2: Automatically identify mismatching IDs from your mod's locator file compared to the base game (NOTE: this may cause disruptions with base game models if your locators are not updated)\nEnter 1 or 2: ")

    if method == "1":
        # Method 1: Provide path to file containing the IDs
        locators_list_path = get_user_input("Please enter the path to the .txt file containing the ID locators list (for example: \"C:\\Users\\CMH\\Downloads\\MA handplaced locators list.txt\"): ")
        if not os.path.exists(locators_list_path):
            print(f"The locators list file '{locators_list_path}' does not exist.")
            return

        ids_folder_path = get_user_input("Enter the path to your mod folder containing the locator files where we'll grab the ID's (ends with \\gfx\\map\\map_object_data): ")
        if not os.path.isdir(ids_folder_path):
            print(f"The directory '{ids_folder_path}' does not exist.")
            return

        # List files in the folder that end with "_locators.txt"
        id_files = list_files_with_suffix(ids_folder_path, "_locators.txt")
        if not id_files:
            print(f"No files ending with '_locators.txt' found in '{ids_folder_path}'.")
            return
        
        print("Files found in the folder:")
        id_file_name = choose_file_from_list(id_files)
        ids_file_full_path = os.path.join(ids_folder_path, id_file_name)

        locators = read_handplaced_locators(locators_list_path)
        id_blocks = extract_id_blocks(ids_file_full_path, locators)

    elif method == "2":
        # Method 2: Automatically identify mismatching IDs
        ids_folder_path = get_user_input("Enter the path to your mod folder containing the locator files where we'll grab the ID's (ends with \\gfx\\map\\map_object_data): ")
        if not os.path.isdir(ids_folder_path):
            print(f"The directory '{ids_folder_path}' does not exist.")
            return

        # List files in the folder that end with "_locators.txt"
        id_files = list_files_with_suffix(ids_folder_path, "_locators.txt")
        if not id_files:
            print(f"No files ending with '_locators.txt' found in '{ids_folder_path}'.")
            return
        
        print("Files found in the folder:")
        id_file_name = choose_file_from_list(id_files)
        mod_file_full_path = os.path.join(ids_folder_path, id_file_name)

        steam_path = get_user_input("Enter the path to your Steam installation (for example: C:\\Program Files (x86)\\Steam): ")
        base_folder_path = os.path.join(steam_path, "steamapps", "common", "Crusader Kings III", "game", "gfx", "map", "map_object_data")

        base_file_full_path = os.path.join(base_folder_path, id_file_name)
        if not os.path.exists(base_file_full_path):
            # List files in the base folder that end with "_locators.txt"
            base_files = list_files_with_suffix(base_folder_path, "_locators.txt")
            if not base_files:
                print(f"No files ending with '_locators.txt' found in '{base_folder_path}'.")
                return

            print("Files found in the base folder:")
            base_file_name = choose_file_from_list(base_files)
            base_file_full_path = os.path.join(base_folder_path, base_file_name)

        id_blocks = compare_and_extract_id_blocks(mod_file_full_path, base_file_full_path)

    else:
        print("Invalid selection. Please restart the script and choose a valid option.")
        return

    # Step 2: Get the path to the folder containing the base locator file for compatching
    base_folder_path = get_user_input("Enter the path to the other mod's folder containing the locator file to compatch (ends with \\gfx\\map\\map_object_data): ")
    if not os.path.isdir(base_folder_path):
        print(f"The directory '{base_folder_path}' does not exist.")
        return

    # Check if a file with the same name as the ID file exists in the base folder
    base_file_full_path = os.path.join(base_folder_path, id_file_name)
    if not os.path.exists(base_file_full_path):
        # List files in the folder that end with "_locators.txt"
        base_files = list_files_with_suffix(base_folder_path, "_locators.txt")
        if not base_files:
            print(f"No files ending with '_locators.txt' found in '{base_folder_path}'.")
            return

        print("Files found in the base folder:")
        base_file_name = choose_file_from_list(base_files)
        base_file_full_path = os.path.join(base_folder_path, base_file_name)

    # Step 3: Replace blocks and create the new file
    output_file = os.path.join(os.getcwd(), "special_building_locators.txt")

    try:
        replace_id_blocks(base_file_full_path, id_blocks, output_file)
        print("Process completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
