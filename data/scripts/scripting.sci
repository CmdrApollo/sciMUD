// types are strings, bools, and numbers, lists and dictionaries too i guess
// dict keys must be strings, values of any type

// lists are 1 indexed

mylist = |10, 10, 10|

mylist = |
    10
    10
    10
|

mydict = |"A" = 65, "B" = 66, "C" = 67|

mydict = |
    "A" = 65
    "B" = 66
    "C" = 67
|

if "A" is in mydict then
    Debug "A is " + "A" from mydict
end

Say ""
Project ""

Project "Hello, " + Target

Debug "Hello, world!"

whatever = "value"
whatever = 3.1
whatever = true

is not
is in

if "Bob" is in Players then
    
end

if Target is in Players then
    
end

value = 3
if value is true then
    
end

x = not whatever

if whatever then
    ...
else
    ...
end

if x is 5 and y is 3 then
    ...
end

unless x is 5 then
    ...
end

if x is not 5 then
    ...
end

while whatever do
    ...
end

for i from 0 to 10 do
    ...
end

routine name with param1, param2 or true do
    if param1 is 0 then
        return 0
    end

    return (call name param1 - 1, true) + 1
end

x = call name 5

// +, -, *, /, %, ^, <, >,

unless x < 5 then
    
end

// fizzbuzz

routine fizzbuzz | n or 100 do
    if n % 15 is 0 then
        Say "FizzBuzz"
    otherwise if n % 3 is 0 then
        Say "Fizz"
    otherwise if n % 5 is 0 then
        Say "Buzz"
    otherwise
        Say n
    end

    call fizzbuzz n - 1
end

call fizzbuzz