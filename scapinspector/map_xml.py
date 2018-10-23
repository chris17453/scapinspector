from . import profile_core

def parse(parent,namespace):
    """Recursively parse an xml tree, and map each tag and all possible attrributes"""
    elements=[]
    if None is namespace:
        namespace={}
    #elements.append(type_obj(parent))
    for child in parent.get_elements():
        for attrib_name in child._attributes:
            if "xmlns:" in attrib_name:
                namespace[attrib_name[6:]]=child[attrib_name]
          
        elements.append(profile_core.type_obj(child,namespace))
        results= parse(child,namespace)
        
        for k,v in results['namespace'].items():
            namespace[k]=v

        if len(results['elements']) > 0:
            for el in results['elements']:
                 elements.append(el)
            elements=profile_core.merge_types(elements,namespace)
    return {'elements':elements,'namespace':namespace}
