
for f in ./dependency/* 
do 
  echo $f
  python get_dependency.py $f Holmes_choices.TXT $f.out
done


