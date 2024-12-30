def into_alpha(x: int):
    return "" if x==0 else into_alpha((x-1)//26)+chr((x-1)%26+ord("A"))

print(into_alpha(948948509))