import requests

url = "https://storage.googleapis.com/yuga-171020.appspot.com/swift.txt"
querystring = {'GoogleAccessId':'storageadmin@yuga-171020.iam.gserviceaccount.com', 'Expires':'1503755879', 'Signature':'tlcHVRwbvMSxaIB6oO/TDXRDczXGFSE6ZXHmZbtCUMhjpos36/1KdKV7Lbmm7XtKsq42SFNksUIZLplyAMpkG8aMBuydeoJd+kvebLxK2k+AX8Xr2VVf5Aq/vVJrPGGYGD0iEN+bY264NIFbyJnlm0pthCVGtB5YqZJadCFDwPFWqi04312Jzzen1CXDY+saY0BabmXaZeCzINz7kV+aq0AJoS8taW0uqboYc1o4gCA6OPAswMr1E840a+II4HqkeOWcv7PiHEPdw/sgH3PR+TkGmjTAd9f8H6zJIFaT8DLbtsl7t3iAUM7Fvdtc9pGQt6KT0qUm9z3XfPEjP8OsTA=='}
payload = "Hello World!"
headers = {'Content-MD5': '7Qdih1MuhjZehB6Sv8UNjA==', 'Content-Type':'text/plain'}

response = requests.request("PUT", url, data=payload, headers=headers, params=querystring)

print(response.text)