import argparse
import datetime
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np


class TaskType(Enum):
    multi = auto()
    add = auto()


@dataclass
class Task:
    task: str

    def __str__(self):
        self.task = self.task
        return self.task


class TaskGenerator:

    def gettask(self) -> Task:
        pass

    def print_row(self, left: str):
        return '{:<8} = ____'.format(left)


class AddTaskGenerator(TaskGenerator):

    def gettask(self) -> Task:
        first = np.random.randint(20)
        second = np.random.randint(20)
        return self.print_row(f'{first} + {second}')


class MultiTaskGenerator(TaskGenerator):

    def gettask(self) -> Task:
        first = np.random.randint(1, 12)
        second = np.random.randint(1, 12)
        return self.print_row(f'{first} * {second}')


@dataclass
class TaskBuilder:
    """ Builds and outputs math tasks """
    task_generator: TaskGenerator

    def buildtasks(self, num_tasks: int):
        tasks: list[str] = []

        for row in range(num_tasks):
            task: Task = self.task_generator.gettask()
            tasks.append(str(task))

        return tasks


class OutFormat(Enum):
    raw = auto()
    md = auto()


class Writer:

    def write_header(self, title: str):
        pass

    def format_tasks(self):
        pass


class RawWriter(Writer):

    def write_header(self, title: str):
        date = datetime.date.today()
        print(f"{title} {date.isoformat()}")
        print()
        print()

    def format_tasks(self, out_matrix):
        for row in out_matrix:
            for col in row:
                print(col + '    ', end='')
            print()
            print()


class MdWriter(Writer):

    def write_header(self, title: str):
        date = datetime.date.today()
        date = datetime.date.today()
        print(f"# {title} ")
        print()
        print(f"Datum: {date.isoformat()}")
        print()

    def format_tasks(self, out_matrix):
        for _ in out_matrix[0]:
            print("| ", end="")
        print("|")
        for _ in out_matrix[0]:
            print("|-", end="")
        print("|")
        for row in out_matrix:
            for col in row:
                print(f"|{col}", end='')
            print("|")
        print("")


def get_task_generator(task_type: TaskType):
    if task_type == TaskType.add:
        return AddTaskGenerator()
    elif task_type == TaskType.multi:
        return MultiTaskGenerator()
    else:
        raise ValueError(f'Invalid task type: {task_type}')


def get_writer(out_format: OutFormat):
    if out_format == OutFormat.raw:
        return RawWriter()
    elif out_format == OutFormat.md:
        return MdWriter()
    else:
        raise ValueError(f"Invalid format: {out_format}")


def main():
    parser = argparse.ArgumentParser('Generate math tasks')
    parser.add_argument('--title', default='Math tasks')
    parser.add_argument('--nrows', type=int, default=20, help='Number of rows')
    parser.add_argument(
        '--ncols',
        type=int,
        default=3,
        help='Number of columns'
    )
    parser.add_argument('--tasktype', type=lambda x: TaskType[x])
    parser.add_argument(
        '--format',
        type=lambda x: OutFormat[x],
        default=OutFormat.raw
    )
    args = parser.parse_args()

    np.random.seed(1)

    num_rows = args.nrows
    num_cols = args.ncols
    num_tasks = num_rows * num_cols

    builder = TaskBuilder(task_generator=get_task_generator(args.tasktype))
    tasks: list[str] = builder.buildtasks(num_tasks)
    out = np.array(tasks).reshape(int(len(tasks) / num_cols), num_cols)

    writer = get_writer(args.format)
    writer.write_header(args.title)
    writer.format_tasks(out)


if __name__ == '__main__':
    main()
