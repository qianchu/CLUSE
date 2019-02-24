en_txt=$1
ch_txt=$2
en_vocab_limit=$3
ch_vocab_limit=$4

echo python3 convert2tra.py $ch_txt
python convert2tra.py $ch_txt
echo python3 tokenize_english.py $en_txt
python tokenize_english.py $en_txt
echo python3 preprocess.py $en_txt ch_tra.txt $en_vocab_limit $ch_vocab_limit
python preprocess.py $en_txt ch_tra.txt $en_vocab_limit $ch_vocab_limit
echo python3 bi_make_sensplit_test.py
python bi_make_sensplit_test.py
echo python3 make_sensplit_test_general.py en_vocab ratings.txt en_test.txt scws_en.txt
python make_sensplit_test_general.py en_vocab ratings.txt en_test.txt scws_en.txt
