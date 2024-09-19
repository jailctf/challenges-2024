nums = (1337,420,69,0o11111111,0xdead,0xbeef,0xcafe,0xdecade,int(b'jail'.hex(),16),0xdeadbeef,0x13371337,0x123456789,123456789,13371337,1099)

total = ""
for num in nums:
    with open(f"best/{num}.txt") as f:
        text = f.read().strip("\n")
        total += text
        total += ","
total = total[:-1]
print(len(total))
print(total)
with open("payload.txt", 'w') as f:
    f.write(total)

