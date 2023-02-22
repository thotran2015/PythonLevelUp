import pickle
import random
import re
import secrets
import smtplib
import ssl
import time
from collections import Counter


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


if __name__ == "__main__":
    # process_diceware_wordlist()
    print(f"Password:\n{generate_passwords()}")
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


