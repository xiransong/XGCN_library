from .propagation_scale import GBP_propagation

from XGCN.model.base import BaseEmbeddingModel
from XGCN.model.module import init_emb_table, dot_product, bpr_loss
from XGCN.data import io, csr

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import os.path as osp
from tqdm import tqdm


class GBP(BaseEmbeddingModel):
    
    def __init__(self, config):
        super().__init__(config)
        self.device = self.config['device']

        assert self.config['from_pretrained'] and self.config['freeze_emb']
        self.base_emb_table = init_emb_table(config, self.info['num_nodes'])
        self.base_emb_table = self.base_emb_table.weight
        self.out_emb_table = torch.empty(self.base_emb_table.shape, dtype=torch.float32)
        
        data_root = self.config['data_root']
        print("# load graph")
        if 'indptr' in self.data:
            indptr = self.data['indptr']
            indices = self.data['indices']
        else:
            data_root = config['data_root']
            indptr = io.load_pickle(osp.join(data_root, 'indptr.pkl'))
            indices = io.load_pickle(osp.join(data_root, 'indices.pkl'))
            self.data['indptr'] = indptr
            self.data['indices'] = indices
        indptr, indices = csr.get_undirected(indptr, indices)
        
        alpha = self.config['alpha']  # 0.1
        w = np.array([(alpha*(1 - alpha))**l for l in range(self.config['walk_length'] + 1)])
        abs_mean = self.base_emb_table.abs().mean().item()
        print("# GBP propagation...")
        self.base_emb_table = GBP_propagation(
            indptr, indices, self.base_emb_table.cpu(),
            L=self.config['walk_length'], # 4
            w=w, 
            r=0.5, 
            rmax=abs_mean * self.config['rmax_ratio'], # 1e-2
            nr=8,
        ).to(self.device)
        
        self.mlp = torch.nn.Sequential(
            *eval(self.config['dnn_arch'])
        ).to(self.device)
        
        self.optimizers = {}
        self.optimizers['gnn-Adam'] = torch.optim.Adam(
            [{'params': self.mlp.parameters(), 'lr': self.config['dnn_lr']}]
        )
    
    def get_output_emb(self, nids):
        return self.mlp(self.base_emb_table[nids])
        
    def forward_and_backward(self, batch_data):
        ((src, pos, neg), ) = batch_data
        
        src_emb = self.get_output_emb(src)
        pos_emb = self.get_output_emb(pos)
        neg_emb = self.get_output_emb(neg)
        
        pos_score = dot_product(src_emb, pos_emb)
        neg_score = dot_product(src_emb, neg_emb)
        
        loss_fn_type = self.config['loss_fn']
        if loss_fn_type == 'bpr':
            loss = bpr_loss(pos_score, neg_score)
        elif loss_fn_type == 'bce':
            pos_loss = F.binary_cross_entropy_with_logits(
                pos_score, 
                torch.ones(pos_score.shape).to(self.device),
            ).mean()
            neg_loss = F.binary_cross_entropy_with_logits(
                neg_score, 
                torch.zeros(neg_score.shape).to(self.device),
            ).mean()
            
            loss = pos_loss + neg_loss
        else:
            assert 0
            
        rw = self.config['L2_reg_weight']
        if rw > 0:
            L2_reg_loss = 1/2 * (1 / len(src)) * (
                (src_emb**2).sum() + (pos_emb**2).sum() + (neg_emb**2).sum()
            )
            loss += rw * L2_reg_loss
        
        self._backward(loss)
        
        return loss.item()
    
    def on_epoch_begin(self):
        self.mlp.train()
    
    @torch.no_grad()
    def infer_out_emb_table(self):
        self.mlp.eval()
        dl = torch.utils.data.DataLoader(dataset=torch.arange(self.info['num_nodes']), 
                                         batch_size=8192)
        for nids in tqdm(dl, desc="infer all output embs"):
            self.out_emb_table[nids] = self.get_output_emb(nids).cpu()

        if self.graph_type == 'user-item':
            self.target_emb_table = self.out_emb_table[self.info['num_users'] : ]
        else:
            self.target_emb_table = self.out_emb_table
    
    def save(self, root=None):
        if root is None:
            root = self.model_root
        self._save_optimizers(root)
        self._save_out_emb_table(root)
        torch.save(self.mlp.state_dict(), osp.join(root, 'mlp-state_dict.pt'))
    
    def load(self, root=None):
        if root is None:
            root = self.model_root
        self._load_optimizers(root)
        self._load_out_emb_table(root)
        self.mlp.load_state_dict(
            torch.load(osp.join(root, 'mlp-state_dict.pt'))
        )
