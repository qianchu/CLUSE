en_txt=$1
ch_txt=$2
en_vocab_limit=$3
ch_vocab_limit=$4

python3 preprocess.py $en_txt $ch_txt $en_vocab_limit $ch_vocab_limit
python3 bi_make_sensplit_test.py
python3 make_sensplit_test_general.py en_vocab ratings.txt en_test.txt scws_en.txt
