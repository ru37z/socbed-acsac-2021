import argparse
import json
import os
from statistics import mean

import matplotlib.pyplot as plot
import pandas
import seaborn


def main():
    args = parse_args()
    types_all = {}
    types_dell = {}
    types_mac = {}
    filesnames_dell = ['host1_default/' + f for f in os.listdir(os.path.join(args.dir, 'host1_default'))]
    filesnames_mac = ['host2_default/' + f for f in os.listdir(os.path.join(args.dir, 'host2_default'))]
    for filename in filesnames_dell + filesnames_mac:
        path = os.path.join(args.dir, filename)
        if 'winlogbeat_' in path and path.endswith('.jsonl'):
            types = {}
            with open(path, 'r') as f:
                for line in f:
                    event = json.loads(line)
                    id = event['winlog']['event_id']
                    provider = event['winlog']['provider_name']
                    type_ = provider + ' ID ' + str(id)
                    types[type_] = types.get(type_, 0) + 1
            for type_ in types:
                occurrences = types_all.get(type_, [])
                occurrences.append(types[type_])
                types_all[type_] = occurrences
                if 'host1_' in path:
                    occurrences = types_dell.get(type_, [])
                    occurrences.append(types[type_])
                    types_dell[type_] = occurrences
                elif 'host2_' in path:
                    occurrences = types_mac.get(type_, [])
                    occurrences.append(types[type_])
                    types_mac[type_] = occurrences
                else:
                    print('ERROR: Non-matching file!')

    print('Total number of types: ' + str(len(types_all)))

    labels_dell = []
    labels_mac = []
    values_dell = []
    values_mac = []
    i = 1
    for type_ in sorted(types_all, key=lambda item: sum(types_all[item]), reverse=True):
        print(
            str(i) + ' & ' +
            type_.split(' ID ')[0] + ' & ' +
            type_.split(' ID ')[1] + ' & ' +
            str(mean(types_dell[type_]) + mean(types_mac[type_])) + ' \\\\')
        labels_dell.extend(len(types_dell[type_]) * [str(i)])
        labels_mac.extend(len(types_mac[type_]) * [str(i)])
        values_dell.extend(types_dell[type_])
        values_mac.extend(types_mac[type_])
        i += 1
        if i > 20:
            break

    labels = pandas.Series(labels_dell + labels_mac)
    values = pandas.Series(values_dell + values_mac)
    hues = pandas.Series(len(values_dell) * ['Host 1'] + len(values_mac) * ['Host 2'])
    df_dell = pandas.concat([values, labels, hues], keys=['values', 'labels', 'host'])

    plot.figure(num=1, figsize=(5.9, 3))

    seaborn.set_theme(style="whitegrid")
    seaborn.boxplot(data=df_dell, x='labels', y='values', hue='host', palette=['#b2abd2', '#fdb863'])

    plot.xlabel('Windows event types (sorted by total occurrences)')
    plot.ylabel('events per iteration (n=10)')
    plot.yscale('log')
    plot.legend(loc='upper right')
    plot.subplots_adjust(bottom=0.17)

    plot.savefig('Events.pdf')
    plot.show()


def parse_args():
    parser = argparse.ArgumentParser(description='Create boxplot from Windows events')
    parser.add_argument('dir', help='directory containing JSONL event files')
    return parser.parse_args()


if __name__ == '__main__':
    main()
