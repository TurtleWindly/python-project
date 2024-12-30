def clean_cccd(cccd):
    cccd = str(cccd)
    while (len(cccd) < 9) or (len(cccd) > 9 and len(cccd) < 12):
        cccd = "0" + cccd
    return cccd


test = "092348093"
print(clean_cccd(92932857))
print(len(clean_cccd(test)))
