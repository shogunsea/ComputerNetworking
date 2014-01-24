require "uri"

require 'debugger'

tester = "Secret flags may be hidden on any page on Fakebook, and their relative location on each page may be different. Each secret flag is a 64 character long sequences of random alphanumerics. All secret flags will appear in the following format (which makes them easy to identify):
<h2 class='secret_flag' style=\"color:red\">FLAG: 64-characters-of-random-alphanumerics</h2>
×
Important!
"

p tester

split = tester.match(%r{<h2.*<\/h2>})
p '!!'
puts split
#debugger

#make sure matched string has secret_flag class:
if split.to_s.include? 'secret_flag'
  puts b =split.to_s.match(/FLAG.*</)
  # debugger
  puts b.to_s[6..-2]
end
a = URI.extract("text here http://foo.example.org/bla and here mailto:test@example.com and here also.")
debugger
# flag =

p  'sss' 