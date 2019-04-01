import numpy as np
import argparse

class TaskBuilder:
    """ Builds and outputs math tasks """

    def __init__(self, level):
        self.level = level

    def buildtasks(self, num_tasks):
        tasks = []

        for row in range(num_tasks):
            first = np.random.randint(100)
            second = np.random.randint(50)

            left = '{} + {}'.format(first, second)
            tasks.append('{:<8} = ____'.format(left))

        return tasks

    def format_tasks(self, out_matrix):
        for row in out_matrix:
            for col in row:
                print(col + '    ', end='')
            print()
            print()


parser = argparse.ArgumentParser('Generate math tasks')
parser.add_argument('--title', default='Math tasks')
parser.add_argument('--nrows', type=int, default=20, help='Number of rows')
parser.add_argument('--ncols', type=int, default=3, help='Number of columns')
args = parser.parse_args()

title = args.title
num_rows = args.nrows
num_cols = args.ncols

num_tasks = num_rows * num_cols

np.random.seed(1)

builder = TaskBuilder(1)
tasks = builder.buildtasks(num_tasks)

out = np.array(tasks).reshape(int(len(tasks) / num_cols), num_cols)

print(title)
print()
print()
builder.format_tasks(out)

