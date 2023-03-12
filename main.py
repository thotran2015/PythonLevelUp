import os.path
import pickle
import random
import re
import secrets
import smtplib
import ssl
import time
import urllib.parse
import zipfile
from collections import Counter, defaultdict
import requests



def is_palindrome(string):
    p1, p2 = 0, len(string) - 1
    while p1 < p2:
        if not string[p1].isalpha():
            p1 += 1
            continue
        if not string[p2].isalpha():
            p2 -= 1
            continue
        if string[p1].lower() != string[p2].lower():
            return False
        p1 += 1
        p2 -= 1
    return True


def sort_words(words_str):
    sorted_str = sorted(words_str.split(" "), key=str.casefold)
    return " ".join(sorted_str)


def find_all_indices(num_list, target):
    sol = []

    def recurse(nums, tar, indices=[]):
        for i in range(len(nums)):
            if isinstance(nums[i], int):
                if nums[i] == target:
                    indices.append(i)
                    sol.append(indices[::])
                    indices.pop()
            elif isinstance(nums[i], list):
                indices.append(i)
                recurse(nums[i], tar, indices)
                indices.pop()
    recurse(num_list, target)
    return sol


def waiting_game():
    input("Enter to start waiting game")
    s = time.time()
    input("Enter again after 4 seconds")
    dur = time.time()-s
    error = dur - 4
    if error == 0:
        print("Perfect! 4 secs")
    elif error < 0:
        print(f"You are {abs(error)} under")
    else:
        print(f"You are {abs(error)} over")


def save_object(obj, filepath):
    with open(filepath, "wb") as file:
        pickle.dump(obj, file)


def retrieve_object(filepath):
    with open(filepath, "rb") as file:
        return pickle.load(file)


def schedule_function(event_time, func, *args, **kwargs):
    while time.time() < event_time:
        continue
    return func(*args, **kwargs)


def send_email():
    sender_email = input("Enter sender gmail:")
    password = input("Enter sender password:")
    recipient_email = input("Enter recipient email:")
    msg = input("Enter your message:")

    # Create a Secure Socket Layer (SSL) context to use SSL protocol with default setting
    context = ssl.create_default_context()
    # Requires connection to port 578 to use SMTP with Transport Layer Security (TLS) protocol
    starttls_port = 587  # for TLS
    ssl_port = 465  # SSL
    # Connect to gmail server using Simple Mail Transfer Protocol (SMTP)
    with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=context) as server:
        # Login into sender gmail account in order to send email
        server.login(sender_email, password)
        # Send email
        server.sendmail(sender_email, recipient_email, msg)


def simulate_dice(*args, sims=int(1e6)):
    print("Number of simulations:", sims)
    freq = {}
    for i in range(sims):
        side_sum = 0
        for die in args:
            side = random.randint(1, die)
            side_sum += side
        freq[side_sum] = freq.get(side_sum, 0) + 1

    print("Outcome Probabilities")
    for side_sum in sorted(freq):
        print(f"{side_sum}\t{freq[side_sum]/sims*100:0.2f}%")


def write_to_file(filepath):
    with open(filepath, "w") as file:
        file.write("Hello!\n This is testing text for unique word counting.\n I hope this is a good test case.")


def count_unique_words(filepath, top_n=10):
    """
    Find word count of text and top n words
    """
    with open(filepath, "r") as file:
        text = file.read()
        words = re.findall(r"[A-Za-z0-9'-]+", text)
        print(f"Word count of {filepath}: {len(words)}")
        print(f"Top {top_n} frequent words:")
        word_count = Counter([w.upper() for w in words])
        for w in word_count.most_common(top_n):
            print(f"{w[0]}\t{w[1]}")


def process_diceware_wordlist():
    coded_words = {}
    with open("diceware_wordlist.txt", "r") as file:
        words = re.findall(r"([1-6]+\t.+\n)", file.read())
        for w in words:
            num_word = w.strip("\n").split("\t")
            coded_words[num_word[0]] = num_word[1]

    print(f"{len(coded_words)} Diceware words")
    print(coded_words)
    if coded_words:
        save_object(coded_words, "passcode_words.pickle")


def generate_passwords(word_count=6):
    secret_vocab = retrieve_object("passcode_words.pickle")
    code_len = 5  # each code has 5 digits and is mapped to a word in secret_vocab
    passwords = []
    for i in range(word_count):
        code = ""
        # Generate a 5-digit code
        for _ in range(code_len):
            # each digit in code is 1 - 6 like sides of a die
            code += str(secrets.randbelow(6) + 1)
        passwords.append(secret_vocab.get(code))
    return " ".join(passwords)


def merge_csv(input_filepaths: list, output_filepath):
    """
    Merge comma separated values (CSV)
    1. read each input file
    2. each input file, read the row and get field to val dict for each row
        translate data row to data dict
    3. store all data dict for all input files
    4. collect all the headers' fields that encounter in the input files
    5. loop through all the fields and the data dict and reconstruct a csv in one file
    """
    data_list = []
    out_header = []
    for filepath in input_filepaths:
        # process one file at the time
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines()
            header = lines[0].strip("\n").split(",")
            print(header)
            for line in lines[1:]:
                values = line.strip("\n").split(",")
                field_to_val_dict = {header[i]: values[i] for i in range(min(len(header), len(values)))}
                data_list.append(field_to_val_dict)
            out_header.extend(field for field in header if field not in out_header)

    with open(output_filepath, "w", encoding="utf-8") as file:
        first_line = ",".join(out_header) + "\n"
        lines = [first_line]
        for row_data_dict in data_list:
            row_data = ",".join([row_data_dict.get(field, "") for field in out_header]) + "\n"
            lines.append(row_data)
        file.writelines(lines)


def solve_sudoku(puzzle, cur=0, nrow=9, ncol=9):
    if cur >= nrow * ncol:
        return True
    r, c = divmod(cur, ncol)
    row_vals = puzzle[r]
    col_vals = [puzzle[r][c] for r in range(nrow)]
    sqr_offset_r, sqr_offset_c = r-(r % 3), c-(c % 3)
    sqr_vals = [puzzle[i][j] for i in range(sqr_offset_r, sqr_offset_r + 3)
                for j in range(sqr_offset_c, sqr_offset_c+3)]

    if puzzle[r][c] == 0:
        for i in range(1, 10):
            # i not i this row, col or 3x3 area
            if i not in row_vals and i not in col_vals and i not in sqr_vals:
                puzzle[r][c] = i
                is_solved = solve_sudoku(puzzle, cur+1)
                if is_solved:
                    return True
                else:
                    puzzle[r][c] = 0
        else:
            return False
    else:
        return solve_sudoku(puzzle, cur+1)


def zip_archive(dirpath, filetypes, zip_filename):
    desired_filepaths = []

    def get_filepaths(dir_path):
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isfile(item_path):
                _, ext = os.path.splitext(item)
                if ext.lower() in filetypes:
                    desired_filepaths.append(item_path)

            if os.path.isdir(item_path):
                get_filepaths(item_path)

    get_filepaths(dirpath)
    print(f"file paths to zip {desired_filepaths}")

    zip_filepath = os.path.join(os.path.dirname(dirpath), zip_filename)
    with zipfile.ZipFile(zip_filepath, mode='w') as myzip:
        for path in desired_filepaths:
            relpath = os.path.relpath(path, dirpath)
            print(f"path and rel path {path} and {relpath}")
            myzip.write(path, arcname=relpath)


<<<<<<< HEAD
def is_downloadable(file_url):
    with requests.get(file_url, allow_redirects=True) as r:
        content_len = int(r.headers.get("content-length", 0))
        return content_len > 0


def create_dir(dirpath):
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)


def download(file_url, out_dir):
    if is_downloadable(file_url):
        create_dir(out_dir)
        out_filepath = os.path.join(out_dir, os.path.basename(file_url))
        if os.path.isfile(out_filepath):
            filepath, ext = os.path.splitext(out_filepath)
            out_filepath = filepath + str(time.time()) + ext

        with requests.get(file_url, allow_redirects=True) as r:
            with open(out_filepath, "wb") as file:
                file.write(r.content)
                print(f"Successfully downloaded {file_url} to {out_filepath}")
                return True
    else:
        print(f"Unable to download: {file_url}")
        return False


def download_sequential_files(url, output_dir):
    url_parser = urllib.parse.urlparse(url)
    filepath = str(url_parser.path)

    create_dir(output_dir)
    # Download the first file given
    is_downloaded = download(url, output_dir)
    if not is_downloaded:
        return

    filepath_parts = filepath.split("/")
    print(f"Filepath: {filepath}\nFilepath parts: {filepath_parts}")
    is_sequence_downloaded = False
    for i in range(len(filepath_parts)-1, -1, -1):
        part = filepath_parts[i]

        if not part:  # path part is empty or None
            continue
        if is_sequence_downloaded:  # a sequence of files is downloaded
            break

        # any number in each part in the filepath can be part of the sequence
        for n in re.finditer(r"[0-9]+", part):
            s, e = n.span()
            num = int(part[s:e])
            while is_downloaded:
                next_num = str(num + 1).zfill(e-s)
                new_part = part[:s] + next_num + part[e:]
                new_path = "/".join(filepath_parts[:i] + [new_part] + filepath_parts[i+1:])
                print(f"New filepath: {new_path}")
                new_url = urllib.parse.urljoin(url, new_path)
                print(f"New url to download: {new_url}")
                is_downloaded = download(new_url, output_dir)
                if is_downloaded:
                    num += 1
            else:
                is_sequence_downloaded = True
                break

def search_number_set(nums, target_set):
    seen = dict()
    target_counter = Counter(target_set)
    target_n = len(target_set)
    for i, n in enumerate(nums):
        seen[n] = seen.get(n, 0) + 1
        if i >= target_n-1:
            if i > target_n-1:
                seen[nums[i-target_n]] -= 1
                if seen[nums[i-target_n]] <= 0:
                    seen.pop(nums[i-target_n])
            if target_counter == seen:
                return True

    return False


if __name__ == "__main__":
    res = search_number_set([5, 3, 0, 0, 7, 0, 0, 0, 0], {0, 0, 7})
    print(res)

    # test_url = 'https://699340.youcanlearnit.net/image001.jpg'
    # download_sequential_files(test_url, "./images")
    # dir_to_zip = "../PythonLevelUp"
    # zip_archive(dir_to_zip, [".csv", ".pickle", ".txt"], "PythonLevelUp.zip")

    # pussle = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
    #           [6, 0, 0, 1, 9, 5, 0, 0, 0],
    #           [0, 9, 8, 0, 0, 0, 0, 6, 0],
    #           [8, 0, 0, 0, 6, 0, 0, 0, 3],
    #           [4, 0, 0, 8, 0, 3, 0, 0, 1],
    #           [7, 0, 0, 0, 2, 0, 0, 0, 6],
    #           [0, 6, 0, 0, 0, 0, 2, 8, 0],
    #           [0, 0, 0, 4, 1, 9, 0, 0, 5],
    #           [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    # expected = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
    #          [6, 7, 2, 1, 9, 5, 3, 4, 8],
    #          [1, 9, 8, 3, 4, 2, 5, 6, 7],
    #          [8, 5, 9, 7, 6, 1, 4, 2, 3],
    #          [4, 2, 6, 8, 5, 3, 7, 9, 1],
    #          [7, 1, 3, 9, 2, 4, 8, 5, 6],
    #          [9, 6, 1, 5, 3, 7, 2, 8, 4],
    #          [2, 8, 7, 4, 1, 9, 6, 3, 5],
    #          [3, 4, 5, 2, 8, 6, 1, 7, 9]]
    # solve_sudoku(pussle)
    # print("Result is expected? ", pussle == expected)
    # print("\n".join([str(r) for r in pussle]))

    # merge_csv(["csv1.csv", "csv2.csv"], "merged_csv.csv")
    # process_diceware_wordlist()
    # print(f"Password:\n{generate_passwords()}")
    # filepath = "shakespeare.txt"
    # count_unique_words(filepath)
    # simulate_dice(4, 6, 6)
    # test_dict = {1: 2, 2: 3, 3: 4}
    # save_object(test_dict, "obj.pickle")
    # print(retrieve_object("obj.pickle"))
    # string_ = "Go "
    # print(is_palindrome(string_))
    # sort_str = "ORANGE banana apple"
    # print("GONE U".casefold())
    # print(sort_words(sort_str))
    # example = [[[1, 2, 3], 2, [1, 3]], [1, 2, 3]]
    # print(find_all_indices(example, 3))
    # waiting_game()
    # schedule_function(time.time() + 3, print, "Howdy!", "How are you?")
    # send_email()


