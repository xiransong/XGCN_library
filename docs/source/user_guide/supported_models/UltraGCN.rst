.. _supported_models-UltraGCN:

UltraGCN
==============

-----------------
Introduction
-----------------

`\[paper\] <>`_

**Title:** UltraGCN: Ultra Simplification of Graph Convolutional Networks for Recommendation

**Authors:** Kelong Mao, Jieming Zhu, Xi Xiao, Biao Lu, Zhaowei Wang, Xiuqiang He

**Abstract:** With the recent success of graph convolutional networks (GCNs), they have been widely applied for recommendation, and achieved impressive performance gains. The core of GCNs lies in its message passing mechanism to aggregate neighborhood information. However, we observed that message passing largely slows down the convergence of GCNs during training, especially for large-scale recommender systems, which hinders their wide adoption. LightGCN makes an early attempt to simplify GCNs for collaborative filtering by omitting feature transformations and nonlinear activations. In this paper, we take one step further to propose an ultra-simplified formulation of GCNs (dubbed UltraGCN), which skips infinite layers of message passing for efficient recommendation. Instead of explicit message passing, UltraGCN resorts to directly approximate the limit of infinite-layer graph convolutions via a constraint loss. Meanwhile, UltraGCN allows for more appropriate edge weight assignments and flexible adjustment of the relative importances among different types of relationships. This finally yields a simple yet effective UltraGCN model, which is easy to implement and efficient to train. Experimental results on four benchmark datasets show that UltraGCN not only outperforms the state-of-the-art GCN models but also achieves more than 10x speedup over LightGCN.

-----------------
Running with XGCN
----------------------

run prepare_UltraGCN_data
---------------------------

Before training UltraGCN, we need to run the ``XGCN.model.UltraGCN.prepare_UltraGCN_data`` module to prepare the "item-item" information. 

**Configuration template for prepare_UltraGCN_data:**

.. code:: yaml

    # config/prepare_UltraGCN_data-config.yaml
    data_root: ""
    results_root: ""

    topk: 10

**Run prepare_UltraGCN_data from CMD:**

.. code:: bash
    
    all_data_root=""       # fill your own paths here
    config_file_root=""

    dataset=facebook

    data_root=$all_data_root/dataset/instance_$dataset
    results_root=$all_data_root/model_output/$dataset/UltraGCN/data

    python -m XGCN.model.UltraGCN.prepare_UltraGCN_data \
        --data_root $data_root --results_root $results_root \
        --topk 10 \


Run UltraGCN
---------------------------

**Configuration template for UltraGCN:**

.. code:: yaml

    # config/UltraGCN-config.yaml
    # Dataset/Results root
    data_root: ""
    results_root: ""

    # Trainer configuration
    epochs: 200
    use_validation_for_early_stop: 1
    val_freq: 1
    key_score_metric: r100
    convergence_threshold: 20
    val_method: ""
    val_batch_size: 256
    file_val_set: ""

    # Testing configuration
    test_method: ""
    test_batch_size: 256
    file_test_set: ""

    # DataLoader configuration
    Dataset_type: NodeListDataset
    num_workers: 1
    NodeListDataset_type: LinkDataset
    pos_sampler: ObservedEdges_Sampler
    neg_sampler: RandomNeg_Sampler
    BatchSampleIndicesGenerator_type: SampleIndicesWithReplacement
    train_batch_size: 2048
    str_num_total_samples: num_edges
    epoch_sample_ratio: 0.1

    # Model configuration
    model: UltraGCN
    seed: 1999

    file_ultra_constrain_mat: ""
    file_ii_topk_neighbors: ""
    file_ii_topk_similarity_scores: ""

    device: "cuda:0"
    emb_table_device: "cuda:0"

    emb_lr: 0.005
    emb_dim: 64
    emb_init_std: 0.0001
    use_sparse: 1
    freeze_emb: 0
    from_pretrained: 0
    file_pretrained_emb: ''

    num_neg: 128
    neg_weight: 128

    topk: 8
    lambda: 0.8
    gamma: 1.5
    L2_reg_weight: 0.0001


**Run UltraGCN from command line:**

.. code:: bash
    
    # script/examples/facebook/run_UltraGCN.sh
    # set to your own path:
    all_data_root='/home/sxr/code/XGCN_and_data/XGCN_data'
    config_file_root='/home/sxr/code/XGCN_and_data/XGCN_library/config'

    dataset=facebook
    model=UltraGCN
    seed=0

    data_root=$all_data_root/dataset/instance_$dataset
    results_root=$all_data_root/model_output/$dataset/$model/[seed$seed]
    ultragcn_data_root=$all_data_root/model_output/$dataset/UltraGCN/data

    # file_pretrained_emb=$all_data_root/model_output/$dataset/Node2vec/[seed$seed]/model/out_emb_table.pt

    python -m XGCN.main.run_model --seed $seed \
        --config_file $config_file_root/$model-config.yaml \
        --data_root $data_root --results_root $results_root \
        --val_method one_pos_k_neg \
        --file_val_set $data_root/val-one_pos_k_neg.pkl \
        --key_score_metric r20 \
        --test_method multi_pos_whole_graph \
        --file_test_set $data_root/test-multi_pos_whole_graph.pkl \
        --file_ultra_constrain_mat $ultragcn_data_root/constrain_mat.pkl \
        --file_ii_topk_neighbors $ultragcn_data_root/beta_score_topk/ii_topk_neighbors.np.pkl \
        --file_ii_topk_similarity_scores $ultragcn_data_root/beta_score_topk/ii_topk_similarity_scores.np.pkl \
        # --from_pretrained 1 --file_pretrained_emb $file_pretrained_emb \

