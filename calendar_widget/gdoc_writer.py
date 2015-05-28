from pydrive.auth import GoogleAuth
import pydrive.drive, pydrive.files

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = pydrive.drive.GoogleDrive(gauth)

def update_resource_from_file (resource_id, filename, mimetype='text/html'):
    f = drive.CreateFile({'id':resource_id})
    f.SetContentFile(filename)
    f.Upload()
    
def get_last_modified (resource_id):
    f = drive.CreateFile({'id':resource_id})
    f.UpdateMetadata()
    f.FetchMetadata()
    dtstring = f.metadata['modifiedDate']
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
    

