def func1(arg1, arg2, **kwargs):
    print("I am func1 ", arg1, arg2)


def func2(arg21, arg22, **kwargs):
    print(" I am func2", arg21, arg22)


FUNC_MAP = {
    "func1": func1,
    "func2": func2
}

some_arguments = {"arg1": 1, "arg2": 2, "arg21": 3, "arg22": 4}
FUNC_MAP["func1"](**some_arguments)
FUNC_MAP["func2"](**some_arguments)

# run this file now yeah, got it ?
sir samajh toh aaya kaise kiya
pr aisa hua kaise?
I mean maine kbhi aisa kuch nii pda

Its easy.

Think of the functions like a reference, now you already know that we have two types of arguments,

keyword and positional,

now lets say we have a dict of some arguments..

some_arguments = {"arg1": 1, "arg2": 2, "arg21": 3, "arg22": 4}
^ this one

and we know the function name as well eg. func1, func2..

then if we unpack this dictionary with the function's reference it would be passed like this

func1(arg1=1, arg2=2, arg21=3, arg22=4) # func1 only consumes arg1 and arg2 so we need something to capture the rest of the arguments
func2(arg1=1, arg2=2, arg21=3, arg22=4)# func2 only consumes arg21 and arg22 so we need something to capture the rest of the arguments

# thats why we put **kwargs 

makes sense ? there ?


yes sir, yes sir totally
mere liye new tha yeh toh isiliye nii smjha tha main
but sir not lets say that yeh dono functions yha nii hote
toh yha pr 
FUNC_MAP = {
    "func1": func1,
    "func2": func2
}
func1 not defined aata naa??


yeah definitely

Okay just to give you a hint about where did I adopt this idea from.

go to urls.py
siarn any ony e

any urls.py
yes sir I am there in jira folder urls.py