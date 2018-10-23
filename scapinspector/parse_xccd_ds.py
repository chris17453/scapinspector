import os
import sys
import json
import untangle
from . import map_xml
from . import benchmarks
from . import profile_core
from . import load
from . import db_scap

# this function loads an SCAP datastream file
# the file may contain many parts, multiple benchmarks, 
# profiles, definitions, dictionaries and other components
# It then parses it for relivant info needed for the UI 
def parse_datastream(xccdf_data_stream_file):
    print ("Parsing:",xccdf_data_stream_file)
    with open(xccdf_data_stream_file, 'r') as ds:
        data=ds.read()
    try:
        result_meta = untangle.parse(data)
    except Exception as err:
        sys.exit("There is an issue the data stream:{} ".format(err))
    package=map_xml.parse(result_meta,{})
    namespaces=package['namespace']
    parsed_data=benchmarks.get(result_meta,namespaces,xccdf_data_stream_file)
    return parsed_data



if __name__ == "__main__":
    global s
    directory="/usr/share/xml/scap/ssg/content/"
    session=db_scap.init_session()
    if None == session: 
        print ("Init DB failed")
        exit(1)

    directory = os.fsencode(directory)

    print("Dir:",directory)
    for file in os.listdir(directory):
        print("File:",file)
        filename = os.fsdecode(file)
        if filename.endswith("-ds.xml"): 
            data=parse_datastream(directory+file)
            load.into_database(data,session)
            continue
        else:
            continue    
    

    session.commit()
    session.close()
