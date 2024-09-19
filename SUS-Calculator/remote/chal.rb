#!/usr/local/bin/ruby
class Calc
  def self.+ left, right
    left = left.to_i if left.is_a? String
    right = right.to_i if right.is_a? String

    return left + right
  end

  def self.- left, right
    left = left.to_i if left.is_a? String
    right = right.to_i if right.is_a? String

    return left - right
  end

  def self.* left, right
    left = left.to_i if left.is_a? String
    right = right.to_i if right.is_a? String

    return left * right
  end

  def self./ left, right
    left = left.to_i if left.is_a? String
    right = right.to_i if right.is_a? String

    return left / right
  end

  def self.% left, right
    left = left.to_i if left.is_a? String
    right = right.to_i if right.is_a? String

    return left % right
  end
end

STDOUT.sync = true
puts <<~HEADER
  SUS Calculator (Super Ultra Safe Calculator)
  I heard using eval for these calculator apps is bad, so I made sure to avoid it
  Good luck doing anything malicious here >:)

HEADER

loop do
  print "> "
  cmd = gets.chomp.split

  if cmd.size != 3
    puts "Usage: num (+|-|*|/|%) num"
    next
  end

  left, op, right = cmd
  puts Calc.send(op.to_sym, left, right)
end
