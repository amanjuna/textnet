'''
main.py

Serves as main entry point into project
'''
from __future__ import print_function, absolute_import

import sys

def main():
    if len(sys.argv) != 3:
        raise RuntimeException("Usage: python main.py [textname] [algorithm]")
    textname = sys.argv[1]
    algname = sys.argv[2]

    print("\nLoading embeddings and data")
    data = load_data(textname)

    print("\nConstructing graph for specified text using specified algorithm")
    net = construct_network(data)

    print("\nPerforming network analysis")
    analyze_net(net)


if __name__ == '__main__':
    main()
