import os
import sys
import platform
import traceback
from datetime import datetime, timezone


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def parse_library(library):
    category = {
        "png": [],
        "jpg": [],
        "room": [],
        "htr": [],
        "meta": [],
        "other": [],
        "not image": []
    }

    for word in library.split("\\"):
        if is_ascii(word) and len(word) > 10:
            if "https://" in word:
                purified = "https://" + word.replace("\\", "").replace("|", "").split("https://")[1]
                if "?" in purified:
                    purified = purified.split("?")[0]

                for extension in [".htr", ".meta", ".room"]:
                    if extension in purified:
                        purified = purified.split(extension)[0] + extension

                link_dict = {"link": purified, "hex": None, "date": None, "category": None}

                if any(ext in purified for ext in category):
                    extension = purified.split(".")[-1]
                    link_dict = {"link": purified, "hex": None, "date": None, "category": extension}
                else:
                    if any(domain in purified for domain in ("img.rec.net", "ns.epicquest.live")):
                        link_dict = {"link": purified, "hex": None, "date": None, "category": "other"}
                    else:
                        link_dict = {"link": purified, "hex": None, "date": None, "category": "not image"}

            else:
                if not link_dict:
                    continue

                purified = word.replace("\\", "")[3:]

                if "GMT" in purified:
                    link_dict['date'] = purified
                else:
                    link_dict['hex'] = purified

                if link_dict['date']:
                    category[link_dict['category']].append(link_dict)

    return category


def option_menu(location_info=""):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Radium Cache Tool")
    print("Dir:", location_info)
    print("1. Parse and Export")
    print("2. Delete Library")
    print("3. Exit")

    while True:
        option = input("Option > ")

        try:
            option = int(option)
        except ValueError:
            option = ""
            continue

        if option in (1, 2, 3):
            break

    return option


def find_library():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_library = os.path.join(script_dir, "Library")
    if os.path.isfile(local_library):
        location = local_library
    elif "userprofile" in os.environ:
        location = os.environ["userprofile"] + r"\AppData\LocalLow\Against Gravity\Rec Room\Library"
        if not os.path.isfile(location):
            return ""
    else:
        return ""

    return location


def log_error(msg):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(script_dir, "radium_error.log")
        with open(log_path, "a") as f:
            f.write(f"[{datetime.now()}] {msg}\n")
    except:
        pass

def main():
    location = find_library()

    max_attempts = 3
    attempts = 0
    while not location:
        attempts += 1
        input(
            f"Couldn't find 'Library' file. Please try duplicating it in this script's directory and press enter. "
            f"Attempts: {attempts}/{max_attempts}")

        location = find_library()

        if location:
            break

        if attempts >= max_attempts:
            print("Try again when the library file is available!")
            input("Press Enter to close...")
            sys.exit()

    option = option_menu(location)

    if option == 1:
        try:
            with open(location, "rb") as lib:
                library = str(lib.read())

            parsed = parse_library(library)

            export = "Radium Cache Output\n[URL / Cache Date]\n"

            export += "\n=== SUMMARY ===\n"
            for key in parsed:
                export += f"  {key}: {len(parsed[key])} items\n"
            export += "\n"

            for key in parsed:
                def parse_gmt_to_local(date_str):
                    if not date_str:
                        return datetime.min
                    dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
                    dt = dt.replace(tzinfo=timezone.utc).astimezone()
                    return dt

                sorted_items = sorted(
                    parsed[key],
                    key=lambda x: parse_gmt_to_local(x['date']),
                    reverse=True
                )
                export += f"\nEXTENSION - {key} (Amount: {len(sorted_items)})\n\n"
                for item in sorted_items:
                    local_date = parse_gmt_to_local(item['date'])
                    if local_date != datetime.min:
                        formatted_date = local_date.strftime('%a, %d %b %Y %H:%M:%S %Z')
                    else:
                        formatted_date = item['date'] or 'Unknown'
                    export += f"{item['link']} ({formatted_date})\n"

            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_name = "RadiumCacheOutput.txt"
            file_path = os.path.join(script_dir, file_name)

            if os.path.exists(file_path):
                os.remove(file_path)

            with open(file_path, "w") as output:
                output.write(export)

            print(f"Exported to {file_path}")
            os.startfile(file_path)
        except Exception as e:
            print(f"Error: {e}")
            log_error(traceback.format_exc())

        input("Press Enter to continue...")
        main()
    elif option == 2:
        try:
            if os.path.exists(location):
                os.remove(location)
                print("Library deleted.")
            else:
                print("The library does not exist!")
        except Exception as e:
            print(f"Error: {e}")
            log_error(traceback.format_exc())

        input("Press Enter to continue...")
        main()
    else:
        print("Exiting!")


if __name__ == "__main__":
    error_occurred = False
    try:
        main()
    except Exception as e:
        error_occurred = True
        log_error(traceback.format_exc())
        print(f"Critical error: {e}")
    if error_occurred:
        input("Press Enter to close...")
