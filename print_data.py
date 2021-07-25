#!/usr/bin/env python3
# coding=utf-8


ch0='⬜'
ch1='⬛'

def print_data(data):
    for row in data:
        print(''.join([ch0 if elt == 0 else ch1 for elt in row]))


def print_animation(dataflow):
    for data in dataflow:
        # wait for enter key to be pressed
        #input("press enter:")
        print('\n\n')
        print_data(data)

if __name__ == '__main__':
    data=[[0,1,1,1,],[1,1,1,0],[0,0,0,1],[0,1,0,1]]
    print_data(data)
    print('\n')
    print_animation((data[0:i] for i in (3, 4)))
