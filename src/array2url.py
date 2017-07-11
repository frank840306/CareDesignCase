def array2url(a):
	url_arg = "?hospital=example_31_14"
	for index in range(len(a)):
		if a[index]!=0 :
			url_arg += "&f"+str(index)+"="+str(a[index])
	return url_arg