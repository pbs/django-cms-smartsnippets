import re

PATTERN_LOAD = [r'(\{% load .*)', r'(.*%\})']
PATTERN_FIND_ALL_FILTER_MATCHES = [r'\<img.+src.*=.*[",\'].*(\{\{.*\|)', r'(:"\d*[x,X]\d*[",\'].*\}\})']
PATTERN_REPLACE_FILTER = [r'(\{\{.*\|)', r'(:"\d*[x,X]\d*".*\}\})']


def regex_replace(content, old, new, image_fields):
    pattern = re.compile(old.join(PATTERN_LOAD))
    new_content = pattern.sub(r'\1%s\2' % new, content)

    filter_replace_pattern = re.compile(old.join(PATTERN_REPLACE_FILTER))
    all_matches = re.findall(old.join(PATTERN_FIND_ALL_FILTER_MATCHES), content)
    replace_pairs = []
    for m in all_matches:
        variable_part = m[0]
        var_name = get_var_name(variable_part)
        if var_name in image_fields:
            replaced_m = filter_replace_pattern.sub(r'\1%s\2' % new, old.join(m))
            replace_pairs.append((old.join(m), replaced_m))

    for pair in replace_pairs:
        new_content = new_content.replace(pair[0], pair[1])
    return new_content



def get_var_name(variable_part):
    pattern = re.compile("{{(?P<field>.*)\|")
    return re.match(pattern, variable_part).groupdict().get('field', '').strip()
