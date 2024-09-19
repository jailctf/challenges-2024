#!/usr/local/bin/ruby

AST = RubyVM::AbstractSyntaxTree

$banned_opcodes = [
    :CALL, :FCALL, :OPCALL, :QCALL, :VCALL, :DXSTR, :XSTR, :ALIAS, :VALIAS
]

def check(ast)
    if $banned_opcodes.include?(ast.type)
        puts "Banned opcode: #{ast.type}"
        exit 1
    end
    ast.children.map do |node|
        if node.is_a?(AST::Node)
            check(node)
        end
    end
end

STDOUT.sync = true
print "Input your very sanitized code: "
code = gets

ast = AST.parse(code)
check(ast)

eval code