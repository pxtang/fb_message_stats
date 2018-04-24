import argparse
import json
import statistics
from datetime import datetime as dt
from textwrap import dedent

import matplotlib.pyplot as plt

NONMESSAGE_TYPES = ["photos", "videos", "sticker", "share", "gifs", "files", "audio_files", "plan", "empty", ]


# Begin helper functions

# NOT typesafe. :D
def intersect(a, b):
    return [val for val in a if val in b]


# Thanks Stack Overflow & John La Rooy!
# http://bit.ly/2HlXZwE
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


# End helper functions


def get_text_stats(type, counts, total_len):
    mean_counts = statistics.mean(counts)
    return dedent("""\
    {0}:
    Total {0}: {1}
    Mean: {2:0.3f}
    Median: {3}
    Mode: {4}
    Std dev: {5:0.3f}
    """.format(
        type,
        int(mean_counts * total_len),
        mean_counts,
        statistics.median(counts),
        statistics.mode(counts),
        statistics.pstdev(counts),
    ))


def get_lengths(data):
    raw_messages = []
    media_counts = dict((k, 0) for k in NONMESSAGE_TYPES)

    for d in data["messages"]:
        if "content" in d:
            raw_messages.append(d["content"])
        else:
            media_type = intersect(d.keys(), NONMESSAGE_TYPES)
            if len(media_type) == 0:
                media_counts["empty"] += 1
            else:
                media_counts[media_type[0]] += 1

    char_lengths = list(map(lambda m: len(m), raw_messages))
    word_counts = list(map(lambda m: len(m.split(' ')), raw_messages))
    total_len = len(raw_messages)

    print(dedent("""\
    Message statistics:
    Total text messages: {0}
    """.format(len(raw_messages),
               )))
    print(get_text_stats("Characters", char_lengths, total_len))
    print(get_text_stats("Words", word_counts, total_len))

    print("Other types: {0}".format(media_counts))


def plot_history(data):
    ts = sorted(map(lambda d: dt.fromtimestamp(d["timestamp"]), data["messages"]))
    start = ts[0]
    end = ts[-1]
    print("Talking from: {}".format(start.strftime('%Y-%m-%d %H:%M:%S')))
    print("To: {}".format(end.strftime('%Y-%m-%d %H:%M:%S')))
    print("Length: {}".format(end - start))

    # TODO properly categorize months
    plt.hist(ts, bins=(diff_month(end, start)))  # TODO allow optional options for this in cli
    plt.show()


def get_data(filename):
    with open(filename, "r") as file:
        json_file = json.loads(file.read())
        return json_file


def thread_finder(name, json_file):
    all_threads = json_file["messages"]
    for thread in all_threads:
        if "participants" in thread and \
                len(thread["participants"]) == 1 and \
                thread["participants"][0] == name:
            return thread

    print("No 1:1 threads found for {}!".format(name))
    exit()


def parse_args():
    parser = argparse.ArgumentParser(description="Get message statistics")
    parser.add_argument('-file')  # TODO make this optional
    parser.add_argument('-stat')
    parser.add_argument('-name')  # TODO group chats but let's be honest I won't get around to this ever
    # TODO add a help thing in here.

    args = parser.parse_args()
    return args


action_dispatch = {
    "lengths": get_lengths,
    "history": plot_history,
}


def main():
    args = parse_args()
    data = get_data(args.file)
    thread = thread_finder(args.name, data)
    action_dispatch[args.stat](thread)


main()
