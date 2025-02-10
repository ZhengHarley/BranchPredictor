#!/usr/bin/env python3

#
#  .d8888b.  888b     d888 8888888b.  8888888888 888b    888          d8888   .d8888b.   d888
# d88P  Y88b 8888b   d8888 888   Y88b 888        8888b   888         d8P888  d88P  Y88b d8888
# 888    888 88888b.d88888 888    888 888        88888b  888        d8P 888       .d88P   888
# 888        888Y88888P888 888   d88P 8888888    888Y88b 888       d8P  888      8888"    888
# 888        888 Y888P 888 8888888P"  888        888 Y88b888      d88   888       "Y8b.   888
# 888    888 888  Y8P  888 888        888        888  Y88888      8888888888 888    888   888
# Y88b  d88P 888   "   888 888        888        888   Y8888            888  Y88b  d88P   888
#  "Y8888P"  888       888 888        8888888888 888    Y888            888   "Y8888P"  8888888
#
#                        Branch Sweep Project | Sampson & Devic 2025

import importlib
import argparse
import json
import pprint
import typing
import os

from predictors import AbstractBasePredictor, Predict


def get_predictor(predictor_module_name) -> typing.Type[AbstractBasePredictor]:
    pred_module = importlib.import_module(f'predictors.{predictor_module_name}')
    pred_class = getattr(pred_module, predictor_module_name)
    return pred_class


def test_predictor_single_trace(predictor: AbstractBasePredictor, trace: str, reset=True) -> typing.Dict:
    if reset:
        predictor.reset()

    results = {
        'trace': trace,
        'total_predictions': 0,
        'correct_predicts': 0,
        'correct_takes': 0,
        'correct_not_takes': 0,
        'incorrect_predicts': 0,
        'incorrect_takes': 0,
        'incorrect_not_takes': 0,
        'opcode_histogram': dict()
    }

    with open(trace, 'r') as fp:
        for line in fp.readlines():
            if not line.strip():
                continue

            # parse the trace file
            opcode, pc, target, taken = line.split(',')
            pc = int(pc, 16)
            target = int(target, 16)
            taken = taken.strip()
            if taken != '0' and taken != '1':
                raise ValueError('result type not valid')
            taken_result = Predict.TAKEN if taken == '1' else Predict.NOT_TAKEN

            results['total_predictions'] += 1
            if opcode not in results['opcode_histogram']:
                results['opcode_histogram'][opcode] = [0, 0]
            results['opcode_histogram'][opcode][0] += 1

            # test the predictor
            pred_result = predictor.predict(opcode, pc, target)

            # update the predictor
            predictor.update(opcode, pc, target, taken_result)

            # check the result
            if pred_result == taken_result:  # correct prediction
                results['correct_predicts'] += 1
                results['opcode_histogram'][opcode][1] += 1
                if taken_result == Predict.TAKEN:  # correct taken prediction
                    results['correct_takes'] += 1
                if taken_result == Predict.NOT_TAKEN:  # correct not taken prediction
                    results['correct_not_takes'] += 1
            else:  # incorrect prediction
                results['incorrect_predicts'] += 1
                if taken_result == Predict.TAKEN:  # incorrect taken prediction
                    results['incorrect_takes'] += 1
                if taken_result == Predict.NOT_TAKEN:  # incorrect not taken prediction
                    results['incorrect_not_takes'] += 1

    return results


def test_predictor_all_traces(predictor: AbstractBasePredictor, trace_dir: str = 'traces', reset=True) -> typing.Dict:
    combo_results = dict()
    for trace_file in os.listdir(trace_dir):
        trace_loc = os.path.join(trace_dir, trace_file)
        combo_results[trace_loc] = test_predictor_single_trace(predictor, trace_loc, reset)
    return combo_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Branch Prediction Design Space Exploration and Evaluation script. Results outputted are standard "
                    "branch statistics such as the number of correctly predicted branches, broken down by whether the "
                    "prediction was a taken or not taken result. Same for incorrect predictions. Also outputs a "
                    "histogram of opcodes with the first number being the number of opcodes encountered, with the "
                    "second number being the number of this type of opcode being correctly predicted (whether taken or "
                    "not)."
    )
    parser.add_argument(
        'predictor',
        help="the name of the predictor to use. Use --list-predictors for available predictors",
        nargs='?'
    )
    parser.add_argument(
        "--list-predictors",
        help="list all available predictors and exit",
        action="store_true"
    )
    parser.add_argument(
        "-o", "--output",
        help="save output into a file"
    )
    parser.add_argument(
        "-f", "--format",
        help="whether output should be in CSV or JSON format",
        choices=['csv', 'json'],
        default='json'
    )
    parser.add_argument(
        "-t", "--trace",
        help="run the specified trace(s). if omitted, run all available traces",
        action='append',  # python < 3.8, compatible with all future however
        # action='extend',  # python >= 3.8
        nargs='*'
    )
    parser.add_argument(
        "--predictor-args",
        help="space-seperated key=word arguments to send to the predictor's constructor",
        nargs=argparse.REMAINDER
    )

    parsed = parser.parse_args()

    try:
        pkwargs = dict()
        for arg in (parsed.predictor_args or []):
            if "=" not in arg:
                raise ValueError(f"Invalid argument '{arg}'. Arguments must be in the format key=value.")
            key, value = arg.split("=", 1)
            pkwargs[key] = eval(value)
    except ValueError as e:
        print(e)
        exit(1)

    if parsed.list_predictors:
        print("Available predictors:")
        for predictor in os.listdir('predictors'):
            if predictor.startswith('_'):
                continue
            print(f'\t{predictor.replace(".py", "")}')
        exit()

    if not parsed.predictor:
        print(f'{parser.prog}: error: the following arguments are required: predictor')
        exit(1)

    predictor_class = get_predictor(parsed.predictor)
    predictor_object = predictor_class(**pkwargs)

    flattened_traces = [item for sublist in (parsed.trace or []) for item in sublist]
    # flattened_traces = parsed.trace  # if >=py3.8 array is flattened when in extend mode
    if flattened_traces:
        result = dict()
        for parsed_trace_file in flattened_traces:
            result[parsed_trace_file] = test_predictor_single_trace(predictor_object, parsed_trace_file)
    else:
        result = test_predictor_all_traces(predictor_object)

    result['_meta'] = {
        'predictor': predictor_object.name(),
        'kwargs': pkwargs
    }

    if parsed.output:
        with open(parsed.output, 'w') as of:
            if parsed.format == 'json':
                json.dump(result, of, indent=2)
            elif parsed.format == 'csv':
                meta = result['_meta']
                del result['_meta']
                of.write(','.join([
                    'predictor',
                    'args',
                    'trace',
                    'total_predictions',
                    'correct_predicts',
                    'correct_takes',
                    'correct_not_takes',
                    'incorrect_predicts',
                    'incorrect_takes',
                    'incorrect_not_takes',
                    'opcode_histogram.beq.total_predictions',
                    'opcode_histogram.beq.correct_predicts',
                    'opcode_histogram.bne.total_predictions',
                    'opcode_histogram.bne.correct_predicts',
                    'opcode_histogram.blt.total_predictions',
                    'opcode_histogram.blt.correct_predicts',
                    'opcode_histogram.bltu.total_predictions',
                    'opcode_histogram.bltu.correct_predicts',
                    'opcode_histogram.bge.total_predictions',
                    'opcode_histogram.bge.correct_predicts',
                    'opcode_histogram.bgeu.total_predictions',
                    'opcode_histogram.bgeu.correct_predicts',
                    'opcode_histogram.beqz.total_predictions',
                    'opcode_histogram.beqz.correct_predicts',
                    'opcode_histogram.bnez.total_predictions',
                    'opcode_histogram.bnez.correct_predicts',
                ]))
                of.write('\n')
                for trace in result:
                    of.write(','.join([
                        meta['predictor'],
                        ' '.join([f"{k}={v}" for k, v in meta['kwargs'].items()]),
                        str(result[trace]['trace']),
                        str(result[trace]['total_predictions']),
                        str(result[trace]['correct_predicts']),
                        str(result[trace]['correct_takes']),
                        str(result[trace]['correct_not_takes']),
                        str(result[trace]['incorrect_predicts']),
                        str(result[trace]['incorrect_takes']),
                        str(result[trace]['incorrect_not_takes']),
                        str(result[trace]['opcode_histogram'].get('beq', [0, 0])[0]),
                        str(result[trace]['opcode_histogram'].get('beq', [0, 0])[1]),
                        str(result[trace]['opcode_histogram'].get('bne', [0, 0])[0]),
                        str(result[trace]['opcode_histogram'].get('bne', [0, 0])[1]),
                        str(result[trace]['opcode_histogram'].get('blt', [0, 0])[0]),
                        str(result[trace]['opcode_histogram'].get('blt', [0, 0])[1]),
                        str(result[trace]['opcode_histogram'].get('bltu', [0, 0])[0]),
                        str(result[trace]['opcode_histogram'].get('bltu', [0, 0])[1]),
                        str(result[trace]['opcode_histogram'].get('bge', [0, 0])[0]),
                        str(result[trace]['opcode_histogram'].get('bge', [0, 0])[1]),
                        str(result[trace]['opcode_histogram'].get('bgeu', [0, 0])[0]),
                        str(result[trace]['opcode_histogram'].get('bgeu', [0, 0])[1]),
                        str(result[trace]['opcode_histogram'].get('beqz', [0, 0])[0]),
                        str(result[trace]['opcode_histogram'].get('beqz', [0, 0])[1]),
                        str(result[trace]['opcode_histogram'].get('bnez', [0, 0])[0]),
                        str(result[trace]['opcode_histogram'].get('bnez', [0, 0])[1]),
                    ]))
                    of.write('\n')
    else:
        if parsed.format == 'json':
            pprint.pprint(result, indent=2)
        else:
            meta = result['_meta']
            del result['_meta']
            print(','.join([
                'predictor',
                'args',
                'trace',
                'total_predictions',
                'correct_predicts',
                'correct_takes',
                'correct_not_takes',
                'incorrect_predicts',
                'incorrect_takes',
                'incorrect_not_takes',
                'opcode_histogram.beq.total_predictions',
                'opcode_histogram.beq.correct_predicts',
                'opcode_histogram.bne.total_predictions',
                'opcode_histogram.bne.correct_predicts',
                'opcode_histogram.blt.total_predictions',
                'opcode_histogram.blt.correct_predicts',
                'opcode_histogram.bltu.total_predictions',
                'opcode_histogram.bltu.correct_predicts',
                'opcode_histogram.bge.total_predictions',
                'opcode_histogram.bge.correct_predicts',
                'opcode_histogram.bgeu.total_predictions',
                'opcode_histogram.bgeu.correct_predicts',
                'opcode_histogram.beqz.total_predictions',
                'opcode_histogram.beqz.correct_predicts',
                'opcode_histogram.bnez.total_predictions',
                'opcode_histogram.bnez.correct_predicts',
            ]))
            for trace in result:
                print(','.join([
                    meta['predictor'],
                    ' '.join([f"{k}={v}" for k, v in meta['kwargs'].items()]),
                    str(result[trace]['trace']),
                    str(result[trace]['total_predictions']),
                    str(result[trace]['correct_predicts']),
                    str(result[trace]['correct_takes']),
                    str(result[trace]['correct_not_takes']),
                    str(result[trace]['incorrect_predicts']),
                    str(result[trace]['incorrect_takes']),
                    str(result[trace]['incorrect_not_takes']),
                    str(result[trace]['opcode_histogram'].get('beq', [0, 0])[0]),
                    str(result[trace]['opcode_histogram'].get('beq', [0, 0])[1]),
                    str(result[trace]['opcode_histogram'].get('bne', [0, 0])[0]),
                    str(result[trace]['opcode_histogram'].get('bne', [0, 0])[1]),
                    str(result[trace]['opcode_histogram'].get('blt', [0, 0])[0]),
                    str(result[trace]['opcode_histogram'].get('blt', [0, 0])[1]),
                    str(result[trace]['opcode_histogram'].get('bltu', [0, 0])[0]),
                    str(result[trace]['opcode_histogram'].get('bltu', [0, 0])[1]),
                    str(result[trace]['opcode_histogram'].get('bge', [0, 0])[0]),
                    str(result[trace]['opcode_histogram'].get('bge', [0, 0])[1]),
                    str(result[trace]['opcode_histogram'].get('bgeu', [0, 0])[0]),
                    str(result[trace]['opcode_histogram'].get('bgeu', [0, 0])[1]),
                    str(result[trace]['opcode_histogram'].get('beqz', [0, 0])[0]),
                    str(result[trace]['opcode_histogram'].get('beqz', [0, 0])[1]),
                    str(result[trace]['opcode_histogram'].get('bnez', [0, 0])[0]),
                    str(result[trace]['opcode_histogram'].get('bnez', [0, 0])[1]),
                ]))
