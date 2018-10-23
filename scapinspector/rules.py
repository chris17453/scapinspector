from . import profile_core

def get_by_id(id,root,namespaces):
    node=profile_core.get_node_by_attribute('id',id,root,namespaces)
    if None==node:
        return None
    rule={}
    title              = profile_core.node_values(node,"title"       ,namespaces)
    description        = profile_core.node_values(node,"description" ,namespaces)
    rule['id']         = id
    rule['title']      = title
    rule['description']= description
    return rule


def get_at_this_level(root,namespaces):
    # TODO manage for reference
    nodes=root.get_elements()
    if None==nodes:
        return []
    rules_list=[]
    for node in nodes:
        tag=profile_core.get_tag_and_namespace(node._name,namespaces)

        if tag['name'] == 'Rule':
            rule={}
            node_id            = node['id']
            if None == node_id:
                node_id=node['ref_id']
            if None == node_id:
                node_id=None

            title              = profile_core.node_values(node,"title"       ,namespaces)
            description        = profile_core.node_values(node,"description" ,namespaces)
            rule['id']         = node_id
            rule['title']      = title
            rule['description']= description
            rules_list.append(rule)
    return rules_list