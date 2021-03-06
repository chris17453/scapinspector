import sys
import json
import untangle

def merge_dict(d1,d2):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    if d2 != {}:
        match=False
        for d2k, d2v in d2.iteritems():
            for d1k, d1v in d1.iteritems():
                if d1v == d2v:
                    match=True
                    break
            if False == match:
                #print (dest_item +" "+d2[dest_item])
                d1.update(d2k,d1v)
    return d1

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def merge_types(items,namespace):
    master=[]
    if None == items:
        return []
    for item in items:
        found=False
        for m,mitem in enumerate(master):
            #print (m,mitem)
            if mitem["name"] == item["name"]:
                temp_attrib=[]
                for a in mitem["attributes"]:
                    temp_attrib.append(a)
                for a in item["attributes"]:
                    temp_attrib.append(a)
                master[m]["attributes"]=f5(temp_attrib)
                found=True
                break
        if True!=found:
                master.append(item)
    return master


def f5(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def type_obj(item,namespace):
    attributes=[]
    for attrib in item._attributes:
        attributes.append(attrib)

    index=item._name.find('_')
    
    name=item._name[index+1:]
    ns=item._name[:index]
    if ns not in namespace:
        name=item._name
        ns=""

    return {'name':name,'attributes':attributes,'namespace':ns}

def get_tag_and_namespace(text,namespace):
    index=text.find('_')
    
    name=text[index+1:]
    ns=text[:index]
    if ns not in namespace:
        name=text
        ns=""
    return {'name':name,'namespace':ns}

def print_tree_tab(depth=0):
    pad=""
    if 0!= depth:
        for _ in range(depth):
            pad+="-"
    pad+="|"
    print(pad,depth)

def nodes(element,path,namespace,depth=0,debug=None):
    if None != debug:
        print_tree_tab(depth)
        
    elements=[]
    index=path.find('/')
    if -1 == index:
        name=path
        sub_path=None
    else:
        name=path[:index]
        sub_path=path[path.find('/')+1:]
    
    #search children
    for item in element.get_elements():
        tag=get_tag_and_namespace(item._name,namespace)
        #print("--",tag['name'],name)    
        if name == tag['name']:
            if None != debug:
                print("Found: ",name)    
            if None != sub_path:
                results=nodes(item,sub_path,namespace,depth+1,debug)
                for result in results:
                    elements.append(result)
            else:
                elements.append(item)
    # if this is the end, return a single element or an array based on array depth
    if depth==0 and len(elements)==1:
        return elements[0]
    if depth==0 and len(elements)==0:
        return []
    # not the end. return all results
    return elements

def node_values(root,path,namespace):
    results = nodes(root,path,namespace)
    if None == results:
        return None
    else:
        return results.cdata

def get_node_by_attribute(attribute_name,attribute_value,root,namespace):
    for node in root.get_elements():
        #print ("Looking for ",attribute_name,attribute_value)
        if None !=node[attribute_name]:
            #print ("found attribute",attribute_name)
            #print ("found attribute",attribute_name,"need",attribute_value,"have",node[attribute_name])
            if node[attribute_name] == attribute_value:
                #print ("see attribute",attribute_value)
                #print(attribute_name,node)
                return node
        results=get_node_by_attribute(attribute_name,attribute_value,node,namespace)
        if None!=results:
            return results
    return None


def get_id_or_ref(node,root,namespace):
    if None != node['id']:
        #print (" id found",node['id'])
        return  node['id']
    if None != node['idref']:
        ref_id = node['idref']
        #
        # print ("ref id found",ref_id)
        node=get_node_by_attribute('id',ref_id,root,namespace)
        if None !=node:
            return node.cdata
        return node
    print ("nothing found",ref_id)

