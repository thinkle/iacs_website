#resource_id = '0B-fhMzqaF6ywUTdNbVdmNGVmdG8'
#front_html = '0B-fhMzqaF6ywb1dKalJaTkthUWM'
import gdata.docs, gdata.docs.client, gdata

client = gdata.docs.client.DocsClient()
client.ClientLogin('website@innovationcharter.org','apply, innovate!',None)

def update_resource_from_file (resource_id, filename, mimetype='text/html'):
    resource = client.get_resource_by_id(resource_id)
    obj = gdata.MediaSource()
    obj.setFile(filename,mimetype)
    return client.UpdateResource(resource,media=obj)

if __name__ == '__main__':
    update_resource_from_file(front_html,'front.html')
