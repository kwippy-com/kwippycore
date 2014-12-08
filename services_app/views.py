from kwippyproject.kwippy.models import *
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse

dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)

def rpc_handler(request):
    response = HttpResponse()
    if len(request.POST):
	response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
    else:
	response.write("<b>This is an XML-RPC Service.</b><br>")
	response.write("You need to invoke it using an XML-RPC Client!<br>")
	response.write("The following methods are available:<ul>")
	methods = dispatcher.system_listMethods()
	for method in methods:
			sig = dispatcher.system_methodSignature(method)
			# this just reads your docblock, so fill it in!
			help =  dispatcher.system_methodHelp(method)
			response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))
	response.write("</ul>")
	response['Content-length'] = str(len(response.content))
	return response
    
def multiply(a, b):
    return a*b

dispatcher.register_function(multiply, 'multiply')
