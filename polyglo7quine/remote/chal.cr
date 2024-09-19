require "base64"
require "lib_c"
require "file_utils"

# basic but prevents just running `strings` on binary if dumped
def decode_flag
    enc = {{ "jail{i_have_to_bake_it_into_the_app}".chars.map{|x| x.ord ^ 0xB3} }}
    enc.map{|c| (c ^ 0xB3).chr }.join
end

def print_header
    puts \
    "=" * 50 + "\n" \
    "|           Welcome to Polyglo7quine!            |\n" \
    "|" + " " * 48 + "|\n" \
    "| The goal is simple, write a polyglot program   |\n" \
    "| that prints its own source code in the         |\n" \
    "| following 7 languages:                         |\n" \
    "| " + "-" * 46 + " |\n" \
    "|   C | C++ | Ruby | Perl | Lua | Python | PHP   |\n" \
    "| " + "-" * 46 + " |\n" \
    "| Nothing too crazy... Good luck!                |\n" + \
    "=" * 50 + "\n\n"
end

def run_process_with_timeout(
  command : String,
  args = nil,
  env : Process::Env = nil,
  clear_env : Bool = false,
  shell : Bool = false,
  input : Process::Stdio = Process::Redirect::Close,
  output : Process::Stdio = Process::Redirect::Close,
  error : Process::Stdio = Process::Redirect::Close,
  chdir : Path | String | Nil = nil,
  timeout : Time::Span = 2.seconds
) : Nil
  process_chan = Channel(Int32).new
  process = Process.new(command, args, env, clear_env, shell, input, output, error, chdir)

  spawn do
    process_chan.send(process.wait.exit_status)
  end

  spawn do
    sleep timeout
    process_chan.close
  end

  begin
    exit_status = process_chan.receive

    if exit_status != 0
      process.close
      raise IO::Error.new("Error when calling process")
    end
  rescue ex : Channel::ClosedError
    process.terminate if process.exists?
    process.close
    raise IO::TimeoutError.new("Process timed out")
  rescue ex
    process.terminate if process.exists?
    process.close
    raise Exception.new("Unknown Error")
  end
end

def runner(command : String, language : String, code : String, via_stdin : Bool)
  output = IO::Memory.new
  input = via_stdin ? IO::Memory.new(code) : Process::Redirect::Close

  begin
    run_process_with_timeout(command, input: input, output: output, timeout: 2.seconds)

    if output.bytesize != code.size || LibC.memcmp(output.buffer, code.to_unsafe, output.bytesize) != 0
      puts "#{language} quine check failed"
      return false
    end

    return true
  rescue ex : IO::Error
    puts "Failed to run #{language} code"
    return false
  rescue ex : IO::TimeoutError
    puts "#{language} code timed out"
    return false
  rescue ex
    puts "Unknown error"
    return false
  end
end

def main
  print_header()
  print "Base64 encoded code > "
  input : String = gets || ""
  
  begin
    code : String = Base64.decode_string(input)
  rescue
    puts "Failed to decode Base64 input"
    return 1
  end

  if code.size <= 5
    puts "Code length must be greater than 5"
    return 1
  end

  temp_dir = File.tempname("chal", "")
  Dir.mkdir(temp_dir)

  result = Dir.cd(temp_dir) do
    prg = File.tempfile("program") do |file|
      file.print(code)
    end

    rand_filename_c = File.join(temp_dir, File.tempname("c", "", dir: ""))
    rand_filename_cpp = File.join(temp_dir, File.tempname("cpp", "", dir: ""))

    gcc_ret = Process.run("/usr/bin/gcc", ["-B/usr/bin", "-x", "c", "-o", rand_filename_c, prg.path])
    unless gcc_ret.success?
      puts "Failed to compile C code"
      break 1
    end

    gpp_ret = Process.run("/usr/bin/g++", ["-B/usr/bin", "-x", "c++", "-o", rand_filename_cpp, prg.path])
    unless gpp_ret.success?
      puts "Failed to compile C++ code"
      break 1
    end

    delete_c_files = Proc(Bool).new do
      begin
        File.delete(rand_filename_c)
        File.delete(rand_filename_cpp)
        true
      rescue
        puts "Failed to delete temp files"
        false
      end
    end

    if (
         runner(rand_filename_c, "C", code, false) &&
         runner(rand_filename_cpp, "C++", code, false) &&
         delete_c_files.call &&
         runner("/usr/bin/perl", "perl", code, true) &&
         runner("/usr/bin/ruby", "ruby", code, true) &&
         runner("/usr/bin/lua", "lua", code, true) &&
         runner("/usr/bin/python3", "python", code, true) &&
         runner("/usr/bin/php", "php", code, true)
       )
      puts "You win! #{decode_flag}"
      break 0
    else
      puts "You lose!"
      break 1
    end
  end

  FileUtils.rm_rf(temp_dir)
  return result
end

STDOUT.sync = true
exit(main)
