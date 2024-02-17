from parser.init_parser import init_parser

def init_java_parser():
    return init_parser('java')

def check_method_annotations(code, start_line, end_line):
    parser = init_java_parser()
    tree = parser.parse(bytes(code, 'utf8'))

    root_node = tree.root_node
    annotation_nodes = find_nodes_by_type(root_node, 'annotation')

    api_ignore = any('@ApiIgnore' in node.text.decode('utf8') for node in annotation_nodes)
    if api_ignore:
        return True, "Method is ignored by @ApiIgnore."

    api_operation = next((node for node in annotation_nodes if '@ApiOperation' in node.text.decode('utf8')), None)
    if not api_operation:
        return False, "Missing @ApiOperation annotation."
    
    api_operation_content = api_operation.text.decode('utf8')
    if 'httpMethod' not in api_operation_content:
        return False, "Missing httpMethod in @ApiOperation annotation."
    if 'value' not in api_operation_content:
        return False, "Missing value in @ApiOperation annotation."

    param_nodes = find_nodes_by_type(root_node, 'formal_parameter')
    for param_node in param_nodes:
        param_annotations = find_nodes_by_type(param_node, 'annotation')
        has_request_body = any('@RequestBody' in node.text.decode('utf8') for node in param_annotations)
        if not has_request_body:
            api_param = next((node for node in param_annotations if '@ApiParam' in node.text.decode('utf8')), None)
            if not api_param:
                return False, "Missing @ApiParam annotation for parameter."
            
            api_param_content = api_param.text.decode('utf8')
            missing_fields = [field for field in ["name", "value", "defaultValue", "required", "example"] if field not in api_param_content]
            if missing_fields:
                return False, f"Missing fields in @ApiParam annotation for parameter: {', '.join(missing_fields)}"
            
    return True, "Swagger annotations are compliant."

def find_nodes_by_type(root_node, node_type):
    nodes = []
    def collect_nodes(node):
        if node.type == node_type:
            nodes.append(node)
        for child in node.children:
            collect_nodes(child)
    collect_nodes(root_node)
    return nodes