import argparse
import time

import onnxruntime

import graphparser.tf_adaptor as tf_adaptor
import graphparser.torch_adaptor as torch_adaptor

from interp.interp_module import load_onnx_from_file
from interp.interp_utils import AbstractionInitConfig


stime = time.time()
def prompt(msg):
    print(f'[{time.time() - stime:.3f}s] ' + msg)

parser = argparse.ArgumentParser()
parser.add_argument('modelpath', type=str, help='model architecture file path')

if __name__ == '__main__':
    args = parser.parse_args()

    model = load_onnx_from_file(args.modelpath)
    prompt('model initialized')

    res = model.analyze(model.gen_abstraction_heuristics())
    prompt('analysis done')
    if len(res) == 0:
        print('No numerical bug')
    else:
        print(f'{len(res)} possible numerical bug(s)')
        for k, v in res.items():
            print(f'- On tensor {k} triggered by operator {v[1]}:')
            for item in v[0]:
                print(str(item))

