# PROJECT_ROOT='/media/xreco/jianxun/xGCN'
# ALL_DATA_ROOT='/media/xreco/DEV/xiran/data/social_and_user_item'
PROJECT_ROOT='/home/jialia/reco/xGCN'
ALL_DATA_ROOT='/home/jialia/reco'


ALL_DATASETS_ROOT=$ALL_DATA_ROOT'/datasets'

######################################
DATASET='taobao-1.6m'

DATA_ROOT=$ALL_DATASETS_ROOT'/instance_'$DATASET
# FILE_INPUT='/media/xreco/DEV/xiran/data/user_item_lightgcn/datasets/instance_taobao-1.6m/train_edges.txt'
FILE_INPUT="$DATA_ROOT/train_edges.txt"
FILE_OUTPUT="$DATA_ROOT/train.txt"

# python $PROJECT_ROOT'/'data/convert_edgeList_2_adj.py $FILE_INPUT $FILE_OUTPUT

# python $PROJECT_ROOT'/'data/handle_adj_graph_txt.py $PROJECT_ROOT \
#     --data_root $DATA_ROOT \
#     --dataset_type 'user-item' \
#     --dataset_name $DATASET \
#     --file_input $FILE_OUTPUT \

FILE_INPUT="$DATA_ROOT/val_pos_edges.txt"
FILE_OUTPUT="$DATA_ROOT/val.txt"
python $PROJECT_ROOT'/'data/convert_edgeList_2_adj.py $FILE_INPUT $FILE_OUTPUT

FILE_INPUT=$DATA_ROOT'/val.txt'
FILE_OUTPUT=$DATA_ROOT'/val.pkl'

python $PROJECT_ROOT'/'data/handle_adj_eval_set.py $PROJECT_ROOT \
    --data_root $DATA_ROOT \
    --dataset_type 'user-item' \
    --dataset_name $DATASET \
    --file_input $FILE_INPUT \
    --file_output $FILE_OUTPUT \


python $PROJECT_ROOT'/'data/sample_multi_pos_eval_set.py $PROJECT_ROOT \
    --file_input $DATA_ROOT'/val.pkl' \
    --file_output $DATA_ROOT'/val-1000.pkl' \
    --num_sample 1000 \

#################################

FILE_INPUT="$DATA_ROOT/test_pos_edges.txt"
FILE_OUTPUT="$DATA_ROOT/test.txt"
python $PROJECT_ROOT'/'data/convert_edgeList_2_adj.py $FILE_INPUT $FILE_OUTPUT

FILE_INPUT=$DATA_ROOT'/test.txt'
FILE_OUTPUT=$DATA_ROOT'/test.pkl'

python $PROJECT_ROOT'/'data/handle_adj_eval_set.py $PROJECT_ROOT \
    --data_root $DATA_ROOT \
    --dataset_type 'user-item' \
    --dataset_name $DATASET \
    --file_input $FILE_INPUT \
    --file_output $FILE_OUTPUT \


python $PROJECT_ROOT'/'data/sample_multi_pos_eval_set.py $PROJECT_ROOT \
    --file_input $DATA_ROOT'/test.pkl' \
    --file_output $DATA_ROOT'/test-1000.pkl' \
    --num_sample 1000 \



