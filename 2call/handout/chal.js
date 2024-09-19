#!/usr/local/bin/node
const readline = require('node:readline');
const rl = readline.createInterface({input: process.stdin, output: process.stdout});

console.log("2call 2call.");
rl.question('code > ', (answer) => {
    let parenCount = 0;
    for (let c of answer) {
        if ("()".includes(c)) {
            if (++parenCount > 2) {
                console.log("too many");
                rl.close();
                return;
            }
            continue;
        }
        if (!"![]+".includes(c)) {
            console.log("no not that");
            rl.close();
            return;
        }
    }

    eval(answer)();
    console.log('the code ran');
    rl.close();
});
