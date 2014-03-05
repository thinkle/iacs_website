#resource_id = '0B-fhMzqaF6ywUTdNbVdmNGVmdG8'
front_html = '0B-fhMzqaF6ywb1dKalJaTkthUWM'
import gdata.docs, gdata.docs.client, gdata
import pytz, datetime

pw = file('pw','r').read()
client = gdata.docs.client.DocsClient()
client.ClientLogin('website@innovationcharter.org',pw,None)

def update_resource_from_file (resource_id, filename, mimetype='text/html'):
    resource = client.get_resource_by_id(resource_id)
    obj = gdata.MediaSource()
    obj.setFile(filename,mimetype)
    return client.UpdateResource(resource,media=obj)

def get_last_modified (resource_id):
    resource = client.get_resource_by_id(resource_id)
    dtstring = resource.updated.text
    return datetime.datetime.strptime(
        dtstring,
        '%Y-%m-%dT%H:%M:%S.%fZ'
        )

def updated_within_last (resource_id, minutes):
    '''Check if the file has been updated within the last X number of minutes
    '''
    dt = get_last_modified(resource_id)
    delta = datetime.datetime.utcnow() - dt
    dminutes = (delta.total_seconds() / 60)
    return dminutes <= minutes


if __name__ == '__main__':
    #update_resource_from_file(front_html,'front.html')
    print 'blarg'
    
