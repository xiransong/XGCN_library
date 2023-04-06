from XGCN.utils.utils import wc_count
from XGCN.data import csr

import numpy as np
from tqdm import tqdm


def load_txt_edges(filename):
    E = np.loadtxt(fname=filename, dtype=np.int32)
    E_src = E[:, 0]
    E_dst = E[:, 1]
    return E_src, E_dst


def load_txt_adj_as_edges(filename):
    num_lines = wc_count(filename)
    src_list = []
    dst_list = []
    with open(filename, 'r') as f:
        for _ in tqdm(range(num_lines)):
            line = np.loadtxt(f, dtype=np.int32, max_rows=1)
            if len(line) < 2:
                continue
            dst = line[1:]
            src = np.full(len(dst), line[0], dtype=np.int32)
            
            src_list.append(src)
            dst_list.append(dst)
    E_src = np.concatenate(src_list, dtype=np.int32)
    E_dst = np.concatenate(dst_list, dtype=np.int32)
    return E_src, E_dst


def load_txt_adj_as_csr(filename):
    E_src, E_dst = load_txt_adj_as_edges(filename)
    indptr, indices = csr.from_edges_to_csr(E_src, E_dst)
    return indptr, indices


def from_txt_adj_to_adj_eval_set(filename):
    src = []
    pos_list = []
    with open(filename, 'r') as f:
        while True:
            x = np.loadtxt(f, max_rows=1, dtype=np.int32, ndmin=1)
            if len(x) == 0:
                break
            if len(x) == 1:
                continue
            src.append(x[0])
            pos_list.append(x[1:])
    print("(<-- don't mind if any UserWarning pops up)")
    src = np.array(src, dtype=np.int32)
    eval_set = {'src': src, 'pos_list': pos_list}
    return eval_set


def save_id_mapping_as_txt(id_mapping):
    raise NotImplementedError


def save_graph_as_txt_edges(g):
    raise NotImplementedError


def save_graph_as_txt_adj(g):
    raise NotImplementedError


def save_emb_as_txt(emb_table):
    raise NotImplementedError
