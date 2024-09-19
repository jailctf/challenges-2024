#!/usr/local/bin/node
const readline = require('node:readline');
const rl = readline.createInterface({input: process.stdin, output: process.stdout});
const {parseScript} = require('esprima');

rl.question('can you js without getattr? > ', (inp) => {
    // length filter
    if (inp.length > 480) {
        console.log('fails length filter');
        rl.close();
        return;
    }

    // char filter
    const banned = new Set("<.;,;.>:`[\x09\x0a\x0b\x0c\x0d]`upxq\"\\\x20");  // partially stolen from caasio ce from angstromctf 2024
    for (const char of inp) {
        const c = char.charCodeAt(0);
        if (c < 0x20 || c > 0x7e || banned.has(char)) {
            console.log("fails char filter (" + char + ')');
            rl.close()
            return;
        }
    }

    // tree filter
    let parsed = parseScript(inp);
    let visit = ((n) => {
        if (typeof n === 'string') {
            if (['VariableDeclaration', 'SpreadElement',
                 'NewExpression', 'CallExpression',  
                'Proxy', '__defineGetter__', '__proto__',
                'Property', 'MemberExpression', 'Property',
                'ArrayExpression', 'instanceof'].includes(n)) {
                console.log('fails tree filter');
                console.log(n); 
                throw new Error();
            };
        }
        if (n instanceof Object) {
            for (let k of Object.getOwnPropertyNames(n)) {
                visit(n[k]);
            }
        }
    });
    try {
        visit(parsed);
    } catch { 
        rl.close(); 
        return; 
    }

    // safety
    delete parsed;
    delete parseScript;
    delete debug;
    delete banned;
    delete visit;
    delete readline;
    delete fetch;
    delete Symbol;

    // send it
    let res = eval(inp);
    console.log(res)

    rl.close();
});
