all_data_root=$1
config_file_root=$2

dataset=livejournal
model=GAMLP
seed=0

data_root=$all_data_root/dataset/instance_$dataset
results_root=$all_data_root/model_output/$dataset/$model/[seed$seed]

file_pretrained_emb=$all_data_root/model_output/$dataset/Node2vec/[seed$seed]/out_emb_table.pt

python -m XGCN.main.run_model --seed $seed \
    --config_file $config_file_root/$model-config.yaml \
    --data_root $data_root --results_root $results_root \
    --val_method one_pos_whole_graph --file_val_set $data_root/val_edges.pkl \
    --test_method multi_pos_whole_graph --file_test_set $data_root/test_set.pkl \
    --file_pretrained_emb $file_pretrained_emb \
    --GAMLP_type GAMLP_JK \
    --num_gcn_layers 2 \
    --hidden 512 \
    --n_layers_1 2 --n_layers_2 2 \
    --pre_process 0 --residual 0 --bns 0 \
