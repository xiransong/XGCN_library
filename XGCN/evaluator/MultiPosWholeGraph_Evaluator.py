from XGCN.dataloading.eval import MultiPosWholeGraph_EvalDataLoader
from XGCN.utils.metric import multi_pos_whole_graph_metrics
from XGCN.utils.utils import combine_dict_list_and_calc_mean

from tqdm import tqdm


class MultiPosWholeGraph_Evaluator:
    
    def __init__(self, model, file_eval_set, batch_size):
        self.model = model
        self.eval_dl = MultiPosWholeGraph_EvalDataLoader(
            file_eval_set, batch_size
        )
    
    def eval(self, desc='eval'):
        batch_results_list = []
        batch_results_weights = []
        num_samples = self.eval_dl.num_samples()
        
        if (hasattr(self.model, 'infer_out_emb_table')) and not (hasattr(self.model, 'out_emb_table') and self.model.out_emb_table is not None):
            self.model.infer_out_emb_table()
        
        for batch_data in tqdm(self.eval_dl, desc=desc):
            src, pos = batch_data
            num_batch_samples = len(src)
            
            all_target_score = self.model._eval_a_batch(
                batch_data, eval_type='whole_graph_multi_pos'
            )
            batch_results = multi_pos_whole_graph_metrics(pos, all_target_score)
            
            batch_results_list.append(batch_results)
            batch_results_weights.append(num_batch_samples / num_samples)
        
        results = combine_dict_list_and_calc_mean(batch_results_list, batch_results_weights)
        return results
