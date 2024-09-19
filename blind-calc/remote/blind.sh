echo -n "Enter math > "
read -p "" math
eval res=$(("$math"))
echo $res
